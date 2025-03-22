import re
from dataclasses import dataclass
from enum import Enum

from htmlnode import LeafNode

MD_IMG_FORMAT = "![{0}]({1})"
MD_IMG_RE_PATTERN = r"[\!]\[([^\]]*)\]\(([^\)]*)\)"
MD_LINK_FORMAT = "[{0}]({1})"
MD_LINK_RE_PATTERN = r"(?<!!)\[([^\]]*)\]\(([^\)]*)\)"


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

    @staticmethod
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

    @staticmethod
    def split_nodes_pattern(old_nodes, pattern, text_type, text_format):
        new_nodes = []
        for node in old_nodes:
            if node.text_type != TextType.TEXT:
                new_nodes.append(node)
            else:
                node_text = node.text
                while len(node_text) > 0:
                    items = re.findall(pattern, node_text)
                    if items:
                        item = items[0]
                        item_text = text_format.format(*item)
                        pos = node_text.find(item_text)
                        if pos > 0:
                            new_nodes.append(TextNode(node_text[:pos], TextType.TEXT))
                        new_nodes.append(TextNode(item[0], text_type, item[1]))
                        node_text = node_text[pos + len(item_text) :]
                    else:
                        new_nodes.append(TextNode(node_text, TextType.TEXT))
                        break
        return new_nodes

    @classmethod
    def from_text(cls, text):
        node = cls(text, TextType.TEXT)
        new_nodes = cls.split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = cls.split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        new_nodes = cls.split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        new_nodes = cls.split_nodes_pattern(new_nodes, MD_IMG_RE_PATTERN, TextType.IMAGE, MD_IMG_FORMAT)
        new_nodes = cls.split_nodes_pattern(new_nodes, MD_LINK_RE_PATTERN, TextType.LINK, MD_LINK_FORMAT)
        return new_nodes
