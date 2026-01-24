"""Conversation Memory Module.

Conversation memory management using LangGraph state.
"""

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage


class ConversationMemory:
    """Conversation Memory Class.

    Manages conversation history using LangGraph state.

    Inherits:
        None

    Attrs:
        messages: list[BaseMessage] - Message history.

    Methods:
        add_user_message(content): Add user message to history.
        add_ai_message(content): Add AI message to history.
        get_messages(): Get all messages.
        clear(): Clear message history.
        get_last_n_messages(n): Get last n messages.
    """

    def __init__(self) -> None:
        """Initialize Conversation Memory.

        Creates a new conversation memory instance.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """

        self.messages: list[BaseMessage] = []

    def add_user_message(self, content: str) -> None:
        """Add User Message.

        Add a user message to the conversation history.

        Args:
            content: str - Message content.

        Returns:
            None

        Raises:
            None
        """

        self.messages.append(HumanMessage(content=content))

    def add_ai_message(self, content: str) -> None:
        """Add AI Message.

        Add an AI message to the conversation history.

        Args:
            content: str - Message content.

        Returns:
            None

        Raises:
            None
        """

        self.messages.append(AIMessage(content=content))

    def get_messages(self) -> list[BaseMessage]:
        """Get Messages.

        Get all messages in the conversation history.

        Args:
            None

        Returns:
            list[BaseMessage] - All messages.

        Raises:
            None
        """

        return self.messages

    def get_last_n_messages(self, n: int) -> list[BaseMessage]:
        """Get Last N Messages.

        Get the last n messages from the conversation history.

        Args:
            n: int - Number of messages to retrieve.

        Returns:
            list[BaseMessage] - Last n messages.

        Raises:
            None
        """

        return self.messages[-n:] if n > 0 else []

    def clear(self) -> None:
        """Clear History.

        Clear the conversation history.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """

        self.messages = []


__all__: list[str] = ["ConversationMemory"]
