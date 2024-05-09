from typing import Literal

from switcore.pydantic_base_model import SwitBaseModel, ViewElement


class HtmlFrame(ViewElement):
    type: Literal['html_frame'] = 'html_frame'
    html_content: str
