"""MCP client adapter layer (T016). All external tool invocation goes through MCP only.

When no MCP server is configured, invoke_tool returns a stub result so the pipeline can run.
"""
from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("chimera.mcp")

# Optional: connect to real MCP server when MCP_SERVER_URL or similar is set
_mcp_client: Any = None


def get_client() -> Any:
    """Return MCP client if configured; otherwise None."""
    global _mcp_client
    if _mcp_client is not None:
        return _mcp_client
    try:
        # When MCP SDK is integrated, instantiate client from config here
        # from config import settings
        # if getattr(settings, "mcp_server_url", None): ...
        pass
    except Exception as e:
        logger.warning("MCP client not available: %s", e)
    return None


async def invoke_tool(tool_name: str, params: dict[str, Any]) -> dict[str, Any]:
    """Invoke a tool via MCP only. Workers must use this; no direct external SDKs.

    Returns a result dict with at least: content_type, content_ref (or inline content), metadata.
    When MCP is unavailable, returns a stub result so the pipeline can continue.
    """
    client = get_client()
    if client is not None:
        try:
            # MCP SDK call: e.g. result = await client.call_tool(tool_name, params)
            # return {"content_type": "text", "content_ref": result.get("content"), ...}
            pass
        except Exception as e:
            logger.exception("MCP invoke failed for %s: %s", tool_name, e)
            return _stub_result(tool_name, params, error=str(e))
    return _stub_result(tool_name, params)


def _stub_result(tool_name: str, params: dict[str, Any], error: str | None = None) -> dict[str, Any]:
    """Stub result when MCP is not available."""
    return {
        "content_type": "text",
        "content_ref": f"[stub] {tool_name}({list(params.keys())})" + (f" error={error}" if error else ""),
        "metadata": {"stub": True, "tool": tool_name},
    }
