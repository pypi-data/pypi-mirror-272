from typing import Literal
from lib.conversations.messages.base import BaseMessage


class AIMessage(BaseMessage):
    """Message from an AI."""
    
    type: Literal["ai"] = "ai"
