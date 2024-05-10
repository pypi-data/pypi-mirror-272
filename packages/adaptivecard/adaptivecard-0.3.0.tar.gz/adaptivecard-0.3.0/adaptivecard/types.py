from typing import Literal
from adaptivecard._typing import DefaultNone
import adaptivecard._base_types
from adaptivecard._mixin import Mixin


class Backgroundimage(Mixin):
    __slots__ = ("url", "fill_mode", "horizontal_alignment", "vertical_alignment")
    def __init__(self,
                 url: str,
                 fill_mode: Literal["cover", "repeatHorizontally",
                                    "repeatVertically", "repeat"] = DefaultNone,
                 horizontal_alignment: Literal["left", "center", "right"] = DefaultNone,
                 vertical_alignment: Literal["top", "center", "bottom"] = DefaultNone
                 ) -> None:
        self.url = url
        self.fill_mode = fill_mode
        self.horizontal_alignment = horizontal_alignment
        self.vertical_alignment = vertical_alignment



adaptivecard._base_types.BackgroundImage.register(Backgroundimage)