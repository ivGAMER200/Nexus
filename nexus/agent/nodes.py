"""Nodes Module.

Graph nodes for the LangGraph agent.
"""

from collections.abc import Callable
from typing import Any

from langchain_core.messages import AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from rich.console import Console
from rich.prompt import Confirm

from nexus.agent.state import AgentState
from nexus.config.prompts import SYSTEM_PROMPT
from nexus.config.settings import settings


def create_agent_node(llm: ChatOpenAI, tools: list, mcp_context: str = "") -> Callable:
    """Create Agent Node.

    Create the main agent node.

    Args:
        llm: ChatOpenAI - Language model.
        tools: list - List of tools.
        mcp_context: str - Optional MCP context string.

    Returns:
        callable - Agent node function.

    Raises:
        None
    """

    llm_with_tools: Any = llm.bind_tools(tools)

    full_system_prompt = SYSTEM_PROMPT
    if mcp_context:
        full_system_prompt += mcp_context

    def agent_node(state: AgentState) -> AgentState:
        """Agent Node.

        Agent reasoning node.

        Args:
            state: AgentState - Current state.

        Returns:
            AgentState - Updated state.

        Raises:
            None
        """

        messages: list = state["messages"]

        max_text_chars = 10000
        processed_messages = []
        for m in messages:
            if isinstance(m, SystemMessage):
                continue

            content = getattr(m, "content", "")
            if isinstance(content, str) and len(content) > max_text_chars:
                m.content = content[:max_text_chars] + "... (truncated for context safety)"
            processed_messages.append(m)

        max_recent_messages = 15
        if len(processed_messages) > max_recent_messages:
            processed_messages = processed_messages[-max_recent_messages:]

        final_messages = [SystemMessage(content=full_system_prompt), *processed_messages]

        response: AIMessage = llm_with_tools.invoke(final_messages)

        return {
            "messages": [response],
            "iteration_count": state.get("iteration_count", 0) + 1,
        }

    return agent_node


def should_continue(state: AgentState) -> str:
    """Should Continue.

    Determine if agent should continue or end.

    Args:
        state: AgentState - Current state.

    Returns:
        str - Next node name.

    Raises:
        None
    """

    messages: list = state["messages"]
    last_message: Any = messages[-1]

    if state.get("iteration_count", 0) >= settings.max_iterations:
        return "end"

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        if settings.approval_required:
            return "request_approval"
        return "continue"

    return "end"


def approval_node(state: AgentState) -> AgentState:
    """Approval Node.

    Request human approval for tool execution.

    Args:
        state: AgentState - Current state.

    Returns:
        AgentState - Updated state.

    Raises:
        None
    """

    console: Console = Console()
    last_message: Any = state["messages"][-1]

    console.print("\n[bold yellow]Tool Execution Pending Approval:[/bold yellow]")

    for tool_call in last_message.tool_calls:  # ty:ignore[unresolved-attribute]
        console.print(f"  • {tool_call['name']}")
        console.print(f"    Args: {tool_call['args']}")

    approved: bool = Confirm.ask("\nApprove tool execution?", default=True)

    return {
        "approval_granted": approved,
        "pending_approval": False,
    }  # ty:ignore[missing-typed-dict-key, invalid-return-type]


__all__: list[str] = ["approval_node", "create_agent_node", "should_continue"]
