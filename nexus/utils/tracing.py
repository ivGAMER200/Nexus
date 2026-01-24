"""Tracing Module.

LangSmith tracing integration for Nexus.
"""

from collections.abc import Callable
from typing import Any

from langsmith import traceable
from langsmith.run_helpers import get_current_run_tree


@traceable(
    run_type="chain",
    name="nexus_operation",
    metadata={"version": "1.0", "component": "nexus"},
)
async def trace_operation(operation_name: str, operation_func: Callable, *args, **kwargs) -> Any:
    """Trace Operation.

    Traces an operation with LangSmith.

    Args:
        operation_name: str - Name of operation.
        operation_func: callable - Function to execute.
        *args: Variable positional arguments.
        **kwargs: Variable keyword arguments.

    Returns:
        any - Result of operation.

    Raises:
        None
    """

    run_tree = get_current_run_tree()

    if run_tree:
        run_tree.metadata["operation"] = operation_name

    result: Any = await operation_func(*args, **kwargs)

    if run_tree:
        run_tree.metadata["completed"] = True

    return result


__all__: list[str] = ["trace_operation"]
