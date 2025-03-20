from dataclasses import dataclass
from enum import Enum


class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


@dataclass
class TextNode:
    text: str
    text_type: TextType
    url: str | None = None

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
