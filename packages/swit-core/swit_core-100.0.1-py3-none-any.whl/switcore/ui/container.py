from switcore.pydantic_base_model import SwitBaseModel, ViewElement
from switcore.ui.button import Button
from switcore.ui.datepicker import DatePicker
from switcore.ui.select import Select


class Container(ViewElement):
    type: str = "container"
    elements: list[Select | Button | DatePicker]

    class Config:
        smart_union = True
