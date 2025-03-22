import re
from enum import Enum

from textnode import TextNode, TextType

MD_HEADING_RE_PATTERN = r"^#{1,6} [\S\s]+"
MD_IMG_FORMAT = "![{0}]({1})"
MD_IMG_RE_PATTERN = r"[\!]\[([^\]]*)\]\(([^\)]*)\)"
MD_LINK_FORMAT = "[{0}]({1})"
MD_LINK_RE_PATTERN = r"(?<!!)\[([^\]]*)\]\(([^\)]*)\)"


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


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


def nodes_from_text(text):
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_pattern(new_nodes, MD_IMG_RE_PATTERN, TextType.IMAGE, MD_IMG_FORMAT)
    return split_nodes_pattern(new_nodes, MD_LINK_RE_PATTERN, TextType.LINK, MD_LINK_FORMAT)


def blocks_from_text(text):
    return [block.strip() for block in text.split("\n\n") if block]


def block_to_block_type(text):
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
