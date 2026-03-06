"""Subagent manager for background task execution."""

import asyncio
import json
import uuid
from pathlib import Path
from typing import Any

from loguru import logger

from nanobot.agent.tools.filesystem import EditFileTool, ListDirTool, ReadFileTool, WriteFileTool
from nanobot.agent.tools.registry import ToolRegistry
from nanobot.agent.tools.shell import ExecTool
from nanobot.agent.tools.web import WebFetchTool, WebSearchTool
from nanobot.bus.events import InboundMessage
from nanobot.bus.queue import MessageBus
from nanobot.config.schema import ExecToolConfig
from nanobot.providers.base import LLMProvider


class SubagentManager:
    """Manages background subagent execution."""

    def __init__(
        self,
        provider: LLMProvider,
        workspace: Path,
        bus: MessageBus,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        reasoning_effort: str | None = None,
        brave_api_key: str | None = None,
        exa_api_key: str | None = None,
        web_proxy: str | None = None,
        exec_config: "ExecToolConfig | None" = None,
        restrict_to_workspace: bool = False,
    ):
        from nanobot.config.schema import ExecToolConfig

        self.provider = provider
        self.workspace = workspace
        self.bus = bus
        self.model = model or provider.get_default_model()
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.reasoning_effort = reasoning_effort
        self.brave_api_key = brave_api_key
        self.exa_api_key = exa_api_key
        self.web_proxy = web_proxy
        self.exec_config = exec_config or ExecToolConfig()
        self.restrict_to_workspace = restrict_to_workspace
        self._running_tasks: dict[str, asyncio.Task[None]] = {}
        self._session_tasks: dict[str, set[str]] = {}  # session_key -> {task_id, ...}
        self._event_queues: list[asyncio.Queue[dict[str, object]]] = []

    def subscribe_events(self) -> asyncio.Queue[dict[str, object]]:
        """Create and return a new event queue for SSE clients."""
        q: asyncio.Queue[dict[str, object]] = asyncio.Queue(maxsize=100)
        self._event_queues.append(q)
        return q

    def unsubscribe_events(self, q: asyncio.Queue[dict[str, object]]) -> None:
        """Remove an event queue when SSE client disconnects."""
        self._event_queues = [eq for eq in self._event_queues if eq is not q]

    def _broadcast_event(self, event: dict[str, object]) -> None:
        """Non-blocking broadcast to all SSE subscribers."""
        import time

        event.setdefault("timestamp", time.time())
        dead: list[asyncio.Queue[dict[str, object]]] = []
        for q in self._event_queues:
            try:
                q.put_nowait(event)
            except asyncio.QueueFull:
                dead.append(q)
        for q in dead:
            self._event_queues = [eq for eq in self._event_queues if eq is not q]

    async def spawn(
        self,
        task: str,
        label: str | None = None,
        origin_channel: str = "cli",
        origin_chat_id: str = "direct",
        session_key: str | None = None,
        max_iterations: int | None = None,
        model: str | None = None,
        workspace: str | None = None,
    ) -> str:
        """Spawn a subagent to execute a task in the background.

        Args:
            max_iterations: Override default iteration limit (15). Use higher
                values (e.g. 30) for complex writing or multi-step tasks.
            model: Override the default LLM model for this subagent.
            workspace: Override the working directory for this subagent.
                Relative paths in file tools resolve against this directory.
                If omitted, uses the default workspace (~/.nanobot/workspace/).
        """
        task_id = str(uuid.uuid4())[:8]
        display_label = label or task[:30] + ("..." if len(task) > 30 else "")
        origin = {"channel": origin_channel, "chat_id": origin_chat_id}

        bg_task = asyncio.create_task(
            self._run_subagent(
                task_id,
                task,
                display_label,
                origin,
                max_iterations=max_iterations,
                model=model,
                workspace=workspace,
            )
        )
        self._running_tasks[task_id] = bg_task
        if session_key:
            self._session_tasks.setdefault(session_key, set()).add(task_id)

        def _cleanup(_: asyncio.Task) -> None:
            self._running_tasks.pop(task_id, None)
            if session_key and (ids := self._session_tasks.get(session_key)):
                ids.discard(task_id)
                if not ids:
                    del self._session_tasks[session_key]

        bg_task.add_done_callback(_cleanup)

        logger.info(
            "Spawned subagent [{}]: {} (model={}, max_iter={})",
            task_id,
            display_label,
            model or self.model,
            max_iterations or 15,
        )
        return f"Subagent [{display_label}] started (id: {task_id}). I'll notify you when it completes."

    async def _run_subagent(
        self,
        task_id: str,
        task: str,
        label: str,
        origin: dict[str, str],
        max_iterations: int | None = None,
        model: str | None = None,
        workspace: str | None = None,
    ) -> None:
        """Execute the subagent task and announce the result."""
        logger.info("Subagent [{}] starting task: {}", task_id, label)
        self._broadcast_event({"type": "start", "task_id": task_id, "label": label})
        effective_model = model or self.model
        effective_max_iter = max_iterations or 15
        effective_workspace = (
            Path(workspace).expanduser().resolve() if workspace else self.workspace
        )

        try:
            tools = ToolRegistry()
            allowed_dir = effective_workspace if self.restrict_to_workspace else None
            tools.register(ReadFileTool(workspace=effective_workspace, allowed_dir=allowed_dir))
            tools.register(WriteFileTool(workspace=effective_workspace, allowed_dir=allowed_dir))
            tools.register(EditFileTool(workspace=effective_workspace, allowed_dir=allowed_dir))
            tools.register(ListDirTool(workspace=effective_workspace, allowed_dir=allowed_dir))
            tools.register(
                ExecTool(
                    working_dir=str(effective_workspace),
                    timeout=self.exec_config.timeout,
                    restrict_to_workspace=self.restrict_to_workspace,
                    path_append=self.exec_config.path_append,
                )
            )
            tools.register(
                WebSearchTool(
                    api_key=self.brave_api_key, exa_api_key=self.exa_api_key, proxy=self.web_proxy
                )
            )
            tools.register(WebFetchTool(proxy=self.web_proxy))

            system_prompt = self._build_subagent_prompt(effective_workspace)
            messages: list[dict[str, Any]] = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": task},
            ]

            # Run agent loop (limited iterations)
            iteration = 0
            final_result: str | None = None

            while iteration < effective_max_iter:
                iteration += 1

                response = await self.provider.chat(
                    messages=messages,
                    tools=tools.get_definitions(),
                    model=effective_model,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    reasoning_effort=self.reasoning_effort,
                )

                if response.has_tool_calls:
                    # Add assistant message with tool calls
                    tool_call_dicts = [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.name,
                                "arguments": json.dumps(tc.arguments, ensure_ascii=False),
                            },
                        }
                        for tc in response.tool_calls
                    ]
                    messages.append(
                        {
                            "role": "assistant",
                            "content": response.content or "",
                            "tool_calls": tool_call_dicts,
                        }
                    )

                    # Execute tools
                    for tool_call in response.tool_calls:
                        args_str = json.dumps(tool_call.arguments, ensure_ascii=False)
                        logger.debug(
                            "Subagent [{}] executing: {} with arguments: {}",
                            task_id,
                            tool_call.name,
                            args_str,
                        )
                        self._broadcast_event(
                            {
                                "type": "tool_call",
                                "task_id": task_id,
                                "tool": tool_call.name,
                                "args_preview": args_str[:200],
                            }
                        )
                        result = await tools.execute(tool_call.name, tool_call.arguments)
                        self._broadcast_event(
                            {
                                "type": "tool_result",
                                "task_id": task_id,
                                "tool": tool_call.name,
                                "result_preview": result[:200],
                            }
                        )
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "name": tool_call.name,
                                "content": result,
                            }
                        )
                else:
                    final_result = response.content
                    self._broadcast_event(
                        {
                            "type": "thinking",
                            "task_id": task_id,
                            "content_preview": (response.content or "")[:200],
                        }
                    )
                    break

            if final_result is None:
                final_result = "Task completed but no final response was generated."

            logger.info("Subagent [{}] completed successfully", task_id)
            self._broadcast_event(
                {
                    "type": "complete",
                    "task_id": task_id,
                    "label": label,
                    "status": "ok",
                    "result_preview": final_result[:300],
                }
            )
            await self._announce_result(task_id, label, task, final_result, origin, "ok")

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            logger.error("Subagent [{}] failed: {}", task_id, e)
            self._broadcast_event(
                {
                    "type": "complete",
                    "task_id": task_id,
                    "label": label,
                    "status": "error",
                    "result_preview": error_msg[:300],
                }
            )
            await self._announce_result(task_id, label, task, error_msg, origin, "error")

    async def _announce_result(
        self,
        task_id: str,
        label: str,
        task: str,
        result: str,
        origin: dict[str, str],
        status: str,
    ) -> None:
        """Announce the subagent result to the main agent via the message bus."""
        status_text = "completed successfully" if status == "ok" else "failed"

        announce_content = f"""[Subagent '{label}' {status_text}]

Task: {task}

Result:
{result}

Summarize this naturally for the user. Keep it brief (1-2 sentences). Do not mention technical details like "subagent" or task IDs."""

        # Inject as system message to trigger main agent
        msg = InboundMessage(
            channel="system",
            sender_id="subagent",
            chat_id=f"{origin['channel']}:{origin['chat_id']}",
            content=announce_content,
        )

        await self.bus.publish_inbound(msg)
        logger.debug(
            "Subagent [{}] announced result to {}:{}", task_id, origin["channel"], origin["chat_id"]
        )

    def _build_subagent_prompt(self, workspace: Path | None = None) -> str:
        """Build a focused system prompt for the subagent."""
        from nanobot.agent.context import ContextBuilder
        from nanobot.agent.skills import SkillsLoader

        effective_workspace = workspace or self.workspace
        time_ctx = ContextBuilder._build_runtime_context(None, None)
        parts = [
            f"""# Subagent

{time_ctx}

You are a subagent spawned by the main agent to complete a specific task.
Stay focused on the assigned task. Your final response will be reported back to the main agent.

## Workspace
{effective_workspace}"""
        ]

        skills_summary = SkillsLoader(effective_workspace).build_skills_summary()
        if skills_summary:
            parts.append(
                f"## Skills\n\nRead SKILL.md with read_file to use a skill.\n\n{skills_summary}"
            )

        return "\n\n".join(parts)

    async def cancel_by_session(self, session_key: str) -> int:
        """Cancel all subagents for the given session. Returns count cancelled."""
        tasks = [
            self._running_tasks[tid]
            for tid in self._session_tasks.get(session_key, [])
            if tid in self._running_tasks and not self._running_tasks[tid].done()
        ]
        for t in tasks:
            t.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        return len(tasks)

    def get_running_count(self) -> int:
        """Return the number of currently running subagents."""
        return len(self._running_tasks)
