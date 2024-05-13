from typing import Any, List
from lib.conversations.chat_memory import BaseChatMemory
from lib.conversations.messages.base import BaseMessage
from lib.utils.utils import get_buffer_string


class ConversationBufferMemory(BaseChatMemory):
    human_prefix: str = "Human"
    ai_prefix: str = "AI"

    @property
    def buffer(self) -> Any:
        """String buffer of memory."""
        return self.buffer_as_messages if self.return_messages else self.buffer_as_str

    def _buffer_as_str(self, messages: List[BaseMessage]) -> str:
        return get_buffer_string(
            messages,
            human_prefix=self.human_prefix,
            ai_prefix=self.ai_prefix,
        )

    @property
    def buffer_as_str(self) -> str:
        """Exposes the buffer as a string in case return_messages is True."""
        return self._buffer_as_str(self.chat_memory.messages)

    @property
    def buffer_as_messages(self) -> List[BaseMessage]:
        """Exposes the buffer as a list of messages in case return_messages is False."""
        return self.chat_memory.messages
