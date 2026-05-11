# app/tools/tool_validator.py

from typing import Dict


def validate_tool_params(
    tool_name: str,
    tool_schema: Dict,
    params: Dict
):
    """
    Basic runtime validation for tool parameters.
    """

    required_fields = tool_schema.get("required", [])

    for field in required_fields:

        if field not in params:
            raise ValueError(
                f"Missing required parameter '{field}' "
                f"for tool '{tool_name}'"
            )

    return True