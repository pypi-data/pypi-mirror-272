from switcore.pydantic_base_model import ViewElement


class Divider(ViewElement):
    type: str = "divider"
