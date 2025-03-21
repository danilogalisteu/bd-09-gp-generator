import re
from dataclasses import dataclass
from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "normal"
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
            case TextType.TEXT:
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


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            new_nodes.append(node)
        else:
            if node.text.count(delimiter) % 2 != 0:
                raise ValueError("unmatched delimiter found")

            for i, part in enumerate(node.text.split(delimiter)):
                if part:
                    new_nodes.append(TextNode(part, TextType.TEXT if i % 2 == 0 else text_type))

    return new_nodes


def extract_markdown_images(text):
    img_pattern = r"[\!]\[([^\]]*)\]\(([^\)]*)\)"
    return re.findall(img_pattern, text)


def extract_markdown_links(text):
    link_pattern = r"(?<!!)\[([^\]]*)\]\(([^\)]*)\)"
    return re.findall(link_pattern, text)
