"""Worker service (T018): stateless single-task execution via MCP only."""
from __future__ import annotations

from uuid import UUID

from mcp.client import invoke_tool
from storage import postgres_repository as repo


async def execute_task(task_id: UUID) -> dict:
    """Execute one task via MCP and return the produced output (content + metadata).

    Fetches task from repo; invokes MCP tool; returns result dict for Judge.
    """
    task = await repo.get_task(task_id)
    if not task:
        return {"content_type": "text", "content_ref": "", "sensitive_topic_flags": [], "error": "task not found"}
    tool_name = "execute_" + task["type"]
    params = task.get("payload") or {}
    result = await invoke_tool(tool_name, params)
    content_ref = result.get("content_ref") or result.get("content", "")
    return {
        "content_type": result.get("content_type", "text"),
        "content_ref": content_ref,
        "sensitive_topic_flags": result.get("sensitive_topic_flags", []),
    }
