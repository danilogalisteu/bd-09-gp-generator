from dataclasses import dataclass
from enum import Enum

from leafnode import LeafNode


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

    def to_leaf(self):
        match self.text_type:
            case TextType.NORMAL:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                return LeafNode("a", self.text, {"href": self.url or ""})
            case TextType.IMAGE:
                return LeafNode("img", "", {"alt": self.text, "src": self.url or ""})
            case _:
                raise ValueError("invalid text type")
