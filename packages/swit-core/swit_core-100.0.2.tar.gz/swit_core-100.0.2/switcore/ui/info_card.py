from typing import Literal

from switcore.pydantic_base_model import SwitBaseModel, ViewElement
from switcore.ui.item import Item


class InfoCard(ViewElement):
    type: Literal['info_card'] = 'info_card'
    items: list[Item]
    action_id: str | None = None
    draggable: bool = False
