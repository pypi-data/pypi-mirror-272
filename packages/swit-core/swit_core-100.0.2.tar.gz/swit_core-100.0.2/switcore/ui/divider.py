from typing import Literal

from switcore.pydantic_base_model import SwitBaseModel, ViewElement


class Divider(ViewElement):
    type: Literal['divider'] = 'divider'