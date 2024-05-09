from typing import Literal

from switcore.pydantic_base_model import SwitBaseModel, ViewElement
from switcore.ui.select_item import SelectItem


class Tabs(ViewElement):
    """
        An element representing an array of tabs.
    """
    type: Literal['tabs'] = 'tabs'
    tabs: list[SelectItem]
    value: str
