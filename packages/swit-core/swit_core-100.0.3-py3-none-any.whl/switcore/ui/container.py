from typing import Literal

from pydantic import Field

from switcore.pydantic_base_model import SwitBaseModel, ViewElement
from switcore.ui.button import Button
from switcore.ui.datepicker import DatePicker
from switcore.ui.select import Select


class Container(ViewElement):
    type: Literal['container'] = 'container'
    elements: list[Select | Button | DatePicker] = Field(discriminator='resource_type')

    class Config:
        smart_union = True
