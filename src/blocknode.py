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
