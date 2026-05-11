# app/tools/tool_executor.py

from app.tools.registry import TOOLS
from app.tools.tool_validator import validate_tool_params
from app.utils.logger import logger


def execute_tool(
    tool_name: str,
    params: dict
):
    """
    Centralized tool execution layer.
    """

    tool_data = TOOLS.get(tool_name)

    if not tool_data:
        raise ValueError(
            f"Tool '{tool_name}' not found."
        )

    # =====================================
    # VALIDATE PARAMS
    # =====================================
    validate_tool_params(
        tool_name=tool_name,
        tool_schema=tool_data,
        params=params
    )

    tool_function = tool_data["function"]

    logger.info(
        f"[Tool Executor] "
        f"Executing tool={tool_name}"
    )

    # =====================================
    # EXECUTE TOOL
    # =====================================
    result = tool_function(**params)

    return result