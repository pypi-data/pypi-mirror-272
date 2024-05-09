from switcore.pydantic_base_model import SwitBaseModel, ViewElement


class HtmlFrame(ViewElement):
    type: str = 'html_frame'
    html_content: str
