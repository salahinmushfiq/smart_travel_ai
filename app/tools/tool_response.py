# app/tools/tool_response.py

from typing import Any, Dict


def success_response(
        tool: str,
        message: str,
        data: Dict[str, Any] = None
):
    return {
        "status": "success",
        "tool": tool,
        "message": message,
        "data": data or {}
    }


def error_response(
        tool: str,
        message: str
):
    return {
        "status": "error",
        "tool": tool,
        "message": message,
        "data": {}
    }
