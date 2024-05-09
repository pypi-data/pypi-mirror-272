from enum import Enum
from typing import Literal

from switcore.pydantic_base_model import SwitBaseModel, ViewElement


class InputVariant(str, Enum):
    text = 'text'
    select = 'select'


class Input(ViewElement):
    type: Literal['text_input'] = 'text_input'
    action_id: str
    placeholder: str | None = None
    trigger_on_input: bool = False
    value: str | None = None
    variant: InputVariant = InputVariant.text
