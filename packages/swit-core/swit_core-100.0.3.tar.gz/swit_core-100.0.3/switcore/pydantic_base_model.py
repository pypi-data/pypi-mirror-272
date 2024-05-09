from typing import Optional

from pydantic import BaseModel


class SwitBaseModel(BaseModel):
    class Config:
        use_enum_values = True


class ViewElement(SwitBaseModel):
    element_id: Optional[str] = None
