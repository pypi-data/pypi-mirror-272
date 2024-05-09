from switcore.pydantic_base_model import SwitBaseModel, ViewElement
from switcore.ui.element_components import StaticAction


class InteractiveImage(ViewElement):
    type: str = "interactive_image"
    image_url: str
    alt: str | None = None
    action_id: str | None = None
    static_action: StaticAction | None = None
    draggable: bool = False
