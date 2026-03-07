"""Tests for MCP tool propagation to subagents."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from nanobot.agent.tools.base import Tool
from nanobot.agent.tools.mcp import MCPToolWrapper
from nanobot.agent.tools.registry import ToolRegistry
from nanobot.agent.subagent import AGENT_TOOL_DENYLIST


def _make_mock_mcp_tool(server_name: str, tool_name: str) -> MCPToolWrapper:
    session = MagicMock()
    session.call_tool = AsyncMock(return_value=MagicMock(content=[]))
    tool_def = MagicMock()
    tool_def.name = tool_name
    tool_def.description = f"Mock {tool_name}"
    tool_def.inputSchema = {"type": "object", "properties": {"query": {"type": "string"}}}
    return MCPToolWrapper(session, server_name, tool_def, tool_timeout=10)


class TestRegistryGetMcpTools:
    def test_returns_only_mcp_tools(self):
        registry = ToolRegistry()

        class NativeTool(Tool):
            @property
            def name(self) -> str:
                return "native_tool"

            @property
            def description(self) -> str:
                return "native"

            @property
            def parameters(self) -> dict[str, Any]:
                return {"type": "object", "properties": {}}

            async def execute(self, **kwargs: Any) -> str:
                return "ok"

        registry.register(NativeTool())
        mcp_tool = _make_mock_mcp_tool("grep_app", "searchGitHub")
        registry.register(mcp_tool)

        mcp_tools = registry.get_mcp_tools()
        assert len(mcp_tools) == 1
        assert mcp_tools[0].name == "mcp_grep_app_searchGitHub"

    def test_returns_empty_when_no_mcp_tools(self):
        registry = ToolRegistry()
        assert registry.get_mcp_tools() == []

    def test_returns_multiple_mcp_tools(self):
        registry = ToolRegistry()
        registry.register(_make_mock_mcp_tool("grep_app", "searchGitHub"))
        registry.register(_make_mock_mcp_tool("context7", "resolve-library-id"))
        registry.register(_make_mock_mcp_tool("exa", "web_search_exa"))

        mcp_tools = registry.get_mcp_tools()
        assert len(mcp_tools) == 3
        names = {t.name for t in mcp_tools}
        assert names == {
            "mcp_grep_app_searchGitHub",
            "mcp_context7_resolve-library-id",
            "mcp_exa_web_search_exa",
        }


class TestSubagentMcpPropagation:
    def test_subagent_registry_gets_parent_mcp_tools(self):
        parent_registry = ToolRegistry()
        parent_registry.register(_make_mock_mcp_tool("grep_app", "searchGitHub"))
        parent_registry.register(_make_mock_mcp_tool("exa", "web_search_exa"))

        subagent_registry = ToolRegistry()
        for mcp_tool in parent_registry.get_mcp_tools():
            subagent_registry.register(mcp_tool)

        assert subagent_registry.has("mcp_grep_app_searchGitHub")
        assert subagent_registry.has("mcp_exa_web_search_exa")

    def test_mcp_tool_shared_session(self):
        session = MagicMock()
        tool_def = MagicMock()
        tool_def.name = "searchGitHub"
        tool_def.description = "search"
        tool_def.inputSchema = {"type": "object", "properties": {}}
        wrapper = MCPToolWrapper(session, "grep_app", tool_def)

        parent_registry = ToolRegistry()
        parent_registry.register(wrapper)

        subagent_registry = ToolRegistry()
        for mcp_tool in parent_registry.get_mcp_tools():
            subagent_registry.register(mcp_tool)

        parent_tool = parent_registry.get("mcp_grep_app_searchGitHub")
        child_tool = subagent_registry.get("mcp_grep_app_searchGitHub")
        assert parent_tool is child_tool

    @pytest.mark.asyncio
    async def test_mcp_tool_callable_from_subagent_registry(self):
        from mcp import types

        session = MagicMock()
        text_block = types.TextContent(type="text", text="result from grep_app")
        session.call_tool = AsyncMock(return_value=MagicMock(content=[text_block]))

        tool_def = MagicMock()
        tool_def.name = "searchGitHub"
        tool_def.description = "search"
        tool_def.inputSchema = {"type": "object", "properties": {"query": {"type": "string"}}}
        wrapper = MCPToolWrapper(session, "grep_app", tool_def)

        parent_registry = ToolRegistry()
        parent_registry.register(wrapper)

        subagent_registry = ToolRegistry()
        for mcp_tool in parent_registry.get_mcp_tools():
            subagent_registry.register(mcp_tool)

        result = await subagent_registry.execute("mcp_grep_app_searchGitHub", {"query": "test"})
        assert "result from grep_app" in result
        session.call_tool.assert_called_once_with("searchGitHub", arguments={"query": "test"})


class TestAgentToolDenylist:
    def test_worker_denies_nothing(self):
        assert AGENT_TOOL_DENYLIST["worker"] == set()

    def test_readonly_denies_write_and_exec(self):
        denied = AGENT_TOOL_DENYLIST["readonly"]
        assert "write_file" in denied
        assert "edit_file" in denied
        assert "exec" in denied
        assert "spawn" in denied

    def test_explorer_allows_exec(self):
        denied = AGENT_TOOL_DENYLIST["explorer"]
        assert "exec" not in denied
        assert "write_file" in denied
        assert "edit_file" in denied

    def test_denylist_preserves_mcp_tools(self):
        registry = ToolRegistry()

        class FakeWriteTool(Tool):
            @property
            def name(self) -> str:
                return "write_file"

            @property
            def description(self) -> str:
                return "write"

            @property
            def parameters(self) -> dict[str, Any]:
                return {"type": "object", "properties": {}}

            async def execute(self, **kwargs: Any) -> str:
                return "ok"

        registry.register(FakeWriteTool())
        registry.register(_make_mock_mcp_tool("grep_app", "searchGitHub"))

        denied = AGENT_TOOL_DENYLIST["readonly"]
        for tool_name in denied:
            registry.unregister(tool_name)

        assert not registry.has("write_file")
        assert registry.has("mcp_grep_app_searchGitHub")

    def test_unknown_agent_type_defaults_to_no_deny(self):
        denied = AGENT_TOOL_DENYLIST.get("nonexistent", set())
        assert denied == set()
