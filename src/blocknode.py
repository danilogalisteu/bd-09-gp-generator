import re
from dataclasses import dataclass
from enum import Enum

from htmlnode import LeafNode, ParentNode
from textnode import TextNode

MD_HEADING_RE_PATTERN = r"^#{1,6} [\S\s]+"


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


@dataclass
class BlockNode:
    text: str
    block_type: BlockType

    @staticmethod
    def get_block_type(text):
        if re.match(MD_HEADING_RE_PATTERN, text):
            return BlockType.HEADING

        if text.startswith("```") and text.endswith("```"):
            return BlockType.CODE

        lines = text.split("\n")

        if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE

        if all(line.startswith("- ") for line in lines):
            return BlockType.UNORDERED_LIST

        item_count = 1
        ordered = True
        for line in lines:
            if not line.startswith(f"{item_count}. "):
                ordered = False
                break
            item_count += 1
        if ordered:
            return BlockType.ORDERED_LIST

        return BlockType.PARAGRAPH

    @classmethod
    def from_text(cls, text):
        return cls(text, cls.get_block_type(text))

    @classmethod
    def blocks_from_text(cls, text):
        return [cls.from_text(block.strip()) for block in text.split("\n\n") if block]

    @classmethod
    def from_document(cls, text):
        return ParentNode(
            "div",
            [block.to_parent() for block in cls.blocks_from_text(text)],
        )

    def to_parent(self):
        match self.block_type:
            case BlockType.PARAGRAPH:
                text = " ".join(self.text.split("\n"))
                return ParentNode(
                    "p",
                    [node.to_leaf() for node in TextNode.from_text(text)],
                )
            case BlockType.HEADING:
                heading, title = self.text.split("# ", maxsplit=1)
                level = 1 + len(heading)
                return ParentNode(
                    f"h{level}",
                    [node.to_leaf() for node in TextNode.from_text(title)],
                )
            case BlockType.CODE:
                text = "\n".join(
                    line for line in 
                    self.text.removeprefix("```").removesuffix("```").split("\n")
                    if line
                )
                return ParentNode("pre", [LeafNode("code", text)])
            case BlockType.QUOTE:
                text = "\n".join([line.removeprefix(">") for line in self.text.split("\n")])
                return ParentNode(
                    "blockquote",
                    [node.to_leaf() for node in TextNode.from_text(text)],
                )
            case BlockType.UNORDERED_LIST:
                return ParentNode(
                    "ul",
                    [
                        ParentNode(
                            "li",
                            [node.to_leaf() for node in TextNode.from_text(line.removeprefix("- "))],
                        )
                        for line in self.text.split("\n")
                    ],
                )
            case BlockType.ORDERED_LIST:
                return ParentNode(
                    "ol",
                    [
                        ParentNode(
                            "li",
                            [node.to_leaf() for node in TextNode.from_text(line.split(". ", maxsplit=1)[1])],
                        )
                        for line in self.text.split("\n")
                    ],
                )
            case _:
                raise ValueError("invalid block type")
