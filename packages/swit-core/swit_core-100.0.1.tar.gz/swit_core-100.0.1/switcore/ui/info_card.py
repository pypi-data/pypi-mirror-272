from switcore.pydantic_base_model import SwitBaseModel, ViewElement
from switcore.ui.item import Item


class InfoCard(ViewElement):
    type: str = 'info_card'
    items: list[Item]
    action_id: str | None = None
    draggable: bool = False
