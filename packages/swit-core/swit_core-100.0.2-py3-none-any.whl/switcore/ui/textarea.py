from enum import Enum
from typing import Literal

from switcore.pydantic_base_model import SwitBaseModel, ViewElement


class TextareaSizeTypes(str, Enum):
    small = "small"
    medium = "medium"
    large = "large"


class Textarea(ViewElement):
    type: Literal['textarea'] = 'textarea'
    action_id: str
    placeholder: str | None = None
    value: str | None = None
    height: TextareaSizeTypes = TextareaSizeTypes.small
    disabled: bool = False
