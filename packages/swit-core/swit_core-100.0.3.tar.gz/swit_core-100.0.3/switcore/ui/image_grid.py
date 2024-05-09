from typing import Literal

from pydantic import Field

from switcore.pydantic_base_model import SwitBaseModel, ViewElement
from switcore.ui.interactive_image import InteractiveImage


class ImageGrid(ViewElement):
    type: Literal['image_grid'] = 'image_grid'
    images: list[InteractiveImage]
    column_count: int = Field(..., ge=2, le=3)
