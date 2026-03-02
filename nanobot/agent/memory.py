"""Memory system for persistent agent memory."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import TYPE_CHECKING

from loguru import logger

from nanobot.utils.helpers import ensure_dir

if TYPE_CHECKING:
    from nanobot.agent.mem0_memory import Mem0Store
    from nanobot.config.schema import Mem0Config
    from nanobot.providers.base import LLMProvider
    from nanobot.session.manager import Session


_SAVE_MEMORY_TOOL = [
    {
        "type": "function",
        "function": {
            "name": "save_memory",
            "description": "Save the memory consolidation result to persistent storage.",
            "parameters": {
                "type": "object",
                "properties": {
                    "history_entry": {
                        "type": "string",
                        "description": "A paragraph (2-5 sentences) summarizing key events/decisions/topics. "
                        "Start with [YYYY-MM-DD HH:MM]. Include detail useful for grep search.",
                    },
                    "memory_update": {
                        "type": "string",
                        "description": "Full updated long-term memory as markdown. Include all existing "
                        "facts plus new ones. Return unchanged if nothing new.",
                    },
                },
                "required": ["history_entry", "memory_update"],
            },
        },
    }
]


_STOP_WORDS = frozenset(
    "a an the is are was were be been being have has had do does did will would shall "
    "should can could may might must need to of in on at by for with from as into about "
    "between through after before above below up down out off over under again then once "
    "and but or nor not no so if when how what which who whom this that these those it "
    "its he she they we you i me my your his her our their them him us am just also very "
    "too much many more most some any all each every both few other another such than "
    "here there where why because since while during only own same than please thanks "
    "hi hello hey yes yeah ok okay sure right well oh hey know think get got like want "
    "make let see use try tell say go come take look help find give work call ask try "
    "really still even already yet always never sometimes anything something nothing "
    "does don't didn't can't won't couldn't wouldn't shouldn't isn't aren't wasn't "
    "haven't hasn't hadn't don doesn did wouldn couldn shouldn isn aren wasn".split()
)

_ENTRY_SPLIT_RE = re.compile(r"\n\n(?=\[[\d]{4}-)")


class MemoryStore:
    """Two-layer memory: MEMORY.md (long-term facts) + HISTORY.md (grep-searchable log)."""

    def __init__(self, workspace: Path, mem0_config: Mem0Config | None = None):
        self.memory_dir = ensure_dir(workspace / "memory")
        self.memory_file = self.memory_dir / "MEMORY.md"
        self.history_file = self.memory_dir / "HISTORY.md"
        self._mem0: Mem0Store | None = None

        if mem0_config and mem0_config.enabled:
            try:
                from nanobot.agent.mem0_memory import Mem0Store

                self._mem0 = Mem0Store(
                    ollama_url=mem0_config.ollama_url,
                    embedding_model=mem0_config.embedding_model,
                    llm_model=mem0_config.llm_model,
                )
            except Exception as exc:
                logger.warning("Failed to enable mem0 semantic memory: {}", exc)
                self._mem0 = None

    def read_long_term(self) -> str:
        if self.memory_file.exists():
            return self.memory_file.read_text(encoding="utf-8")
        return ""

    def write_long_term(self, content: str) -> None:
        self.memory_file.write_text(content, encoding="utf-8")

    def append_history(self, entry: str) -> None:
        with open(self.history_file, "a", encoding="utf-8") as f:
            f.write(entry.rstrip() + "\n\n")

    @staticmethod
    def _extract_keywords(text: str) -> list[str]:
        """Extract meaningful keywords from text for history search."""
        words = re.findall(r"[a-zA-Z0-9_.-]+", text.lower())
        return [w for w in words if len(w) > 2 and w not in _STOP_WORDS]

    def recall(self, query: str, max_entries: int = 5, max_chars: int = 1500) -> str:
        """Search HISTORY.md for entries relevant to query. Returns matched entries."""
        if not self.history_file.exists():
            return ""
        keywords = self._extract_keywords(query)
        if not keywords:
            return ""

        raw = self.history_file.read_text(encoding="utf-8").strip()
        if not raw:
            return ""

        entries = _ENTRY_SPLIT_RE.split(raw)
        scored: list[tuple[int, str]] = []
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue
            lower = entry.lower()
            score = sum(1 for kw in keywords if kw in lower)
            if score > 0:
                scored.append((score, entry))

        scored.sort(key=lambda x: x[0], reverse=True)

        result_parts: list[str] = []
        total = 0
        for _, entry in scored[:max_entries]:
            if total + len(entry) > max_chars:
                break
            result_parts.append(entry)
            total += len(entry)

        return "\n\n".join(result_parts)

    def get_memory_context(self, query: str | None = None) -> str:
        """Build memory context with long-term facts and optionally recalled history."""
        parts: list[str] = []
        long_term = self.read_long_term()
        if long_term:
            parts.append(f"## Long-term Memory\n{long_term}")
        if query:
            recalled = self.recall(query)
            if recalled:
                parts.append(f"## Recalled History\n{recalled}")
            if self._mem0 is not None:
                semantic = self._mem0.search(query)
                if semantic:
                    parts.append(f"## Semantic Memory\n{semantic}")
        return "\n\n".join(parts)

    def save_to_mem0(self, text: str) -> None:
        if self._mem0 is not None:
            self._mem0.add(text)

    async def consolidate(
        self,
        session: Session,
        provider: LLMProvider,
        model: str,
        *,
        archive_all: bool = False,
        memory_window: int = 50,
    ) -> bool:
        """Consolidate old messages into MEMORY.md + HISTORY.md via LLM tool call.

        Returns True on success (including no-op), False on failure.
        """
        if archive_all:
            old_messages = session.messages
            keep_count = 0
            logger.info("Memory consolidation (archive_all): {} messages", len(session.messages))
        else:
            keep_count = memory_window // 2
            if len(session.messages) <= keep_count:
                return True
            if len(session.messages) - session.last_consolidated <= 0:
                return True
            old_messages = session.messages[session.last_consolidated:-keep_count]
            if not old_messages:
                return True
            logger.info("Memory consolidation: {} to consolidate, {} keep", len(old_messages), keep_count)

        lines = []
        for m in old_messages:
            if not m.get("content"):
                continue
            tools = f" [tools: {', '.join(m['tools_used'])}]" if m.get("tools_used") else ""
            lines.append(f"[{m.get('timestamp', '?')[:16]}] {m['role'].upper()}{tools}: {m['content']}")

        current_memory = self.read_long_term()
        prompt = f"""Process this conversation and call the save_memory tool with your consolidation.

## Current Long-term Memory
{current_memory or "(empty)"}

## Conversation to Process
{chr(10).join(lines)}"""

        try:
            response = await provider.chat(
                messages=[
                    {"role": "system", "content": "You are a memory consolidation agent. Call the save_memory tool with your consolidation of the conversation."},
                    {"role": "user", "content": prompt},
                ],
                tools=_SAVE_MEMORY_TOOL,
                model=model,
            )

            if not response.has_tool_calls:
                logger.warning("Memory consolidation: LLM did not call save_memory, skipping")
                return False

            args = response.tool_calls[0].arguments
            # Some providers return arguments as a JSON string instead of dict
            if isinstance(args, str):
                args = json.loads(args)
            if not isinstance(args, dict):
                logger.warning("Memory consolidation: unexpected arguments type {}", type(args).__name__)
                return False

            if entry := args.get("history_entry"):
                if not isinstance(entry, str):
                    entry = json.dumps(entry, ensure_ascii=False)
                self.append_history(entry)
            if update := args.get("memory_update"):
                if not isinstance(update, str):
                    update = json.dumps(update, ensure_ascii=False)
                if update != current_memory:
                    self.write_long_term(update)

            session.last_consolidated = 0 if archive_all else len(session.messages) - keep_count
            logger.info("Memory consolidation done: {} messages, last_consolidated={}", len(session.messages), session.last_consolidated)
            return True
        except Exception:
            logger.exception("Memory consolidation failed")
            return False
