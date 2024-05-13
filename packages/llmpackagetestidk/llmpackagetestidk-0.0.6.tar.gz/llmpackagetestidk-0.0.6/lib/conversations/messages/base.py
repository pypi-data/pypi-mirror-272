from typing import Any, Dict, List, Optional, Union

from pydantic import Field


class BaseMessage():
    """Base abstract Message class.

    Messages are the inputs and outputs of ChatModels.
    """

    content: Union[str, List[Union[str, Dict]]]
    """The string contents of the message."""

    additional_kwargs: dict = Field(default_factory=dict)
    """Reserved for additional payload data associated with the message.
    
    For example, for a message from an AI, this could include tool calls."""

    response_metadata: dict = Field(default_factory=dict)
    """Response metadata. For example: response headers, logprobs, token counts."""

    type: str

    name: Optional[str] = None

    id: Optional[str] = None
    """An optional unique identifier for the message. This should ideally be
    provided by the provider/model which created the message."""

    def __init__(
        self, content: Union[str, List[Union[str, Dict]]], **kwargs: Any
    ) -> None:
        """Pass in content as positional arg."""
        self.content = content
