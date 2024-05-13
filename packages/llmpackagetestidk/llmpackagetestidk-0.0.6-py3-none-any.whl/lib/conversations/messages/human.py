from typing import Literal
from lib.conversations.messages.base import BaseMessage


class HumanMessage(BaseMessage):
    """Message from a human."""

    type: Literal["human"] = "human"
