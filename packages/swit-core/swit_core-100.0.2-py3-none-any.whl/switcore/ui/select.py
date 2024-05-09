from enum import Enum
from typing import Any, Literal

from pydantic import root_validator, validator, model_validator

from switcore.pydantic_base_model import SwitBaseModel, ViewElement
from switcore.ui.element_components import Tag
from switcore.ui.image import Image
from switcore.ui.select_item import SelectItem


class NoOptionsReason(SwitBaseModel):
    message: str


class Option(SelectItem):
    """
        https://devdocs.swit.io/docs/user-actions/ref/schemas/select
    """
    icon: Image | None = None
    tag: Tag | None = None


class OptionGroup(SwitBaseModel):
    label: str
    options: list[Option]

    # add validator to check if options is not empty
    @validator('options')
    def options_must_not_be_empty(cls, v):
        if len(v) == 0:
            raise ValueError("options must not be empty")
        return v


class SelectStyleTypes(str, Enum):
    filled = "filled"
    outlined = "outlined"
    ghost = "ghost"


class Style(SwitBaseModel):
    variant: SelectStyleTypes = SelectStyleTypes.outlined


class SelectQuery(SwitBaseModel):
    query_server: bool = True
    disabled: bool = False
    placeholder: str | None = None
    value: str | None = None
    action_id: str | None = None


class Select(ViewElement):
    type: Literal['select'] = 'select'
    placeholder: str | None = None
    multiselect: bool = False
    trigger_on_input: bool = False
    value: list[str] | None = None
    options: list[Option] = []
    option_groups: list[OptionGroup] = []
    no_options_reason: NoOptionsReason | None = None
    style: Style | None = None
    query: SelectQuery | None = None

    @model_validator(mode='after')
    def validate_options_exclusivity(self) -> 'Select':
        if self.options and self.option_groups:
            raise ValueError('options and option_groups are mutually exclusive')

        if not self.options and not self.option_groups and not self.no_options_reason:
            raise ValueError('options or option_groups must be provided')

        return self