import unittest

from blocknode import BlockNode, BlockType
from textnode import TextNode, TextType


class TestBlockNode(unittest.TestCase):
    node1_text = "# This is a heading"
    node2_text = "```single-line code block```"
    node3_text = "> This is a single-line quote block"
    node4_text = "- This is a single-line item list"
    node5_text = "1. This is a single-line item list"
    node6_text = "This is text with a **bold type** expression, an _italic type_ expression and a `code block` expression. It also has [a link to boot dev](https://www.boot.dev) and ![an image](https://i.imgur.com/zjjcJKZ.png)."

    def test_from_text(self):
        node1 = BlockNode.from_text(self.node1_text)
        self.assertEqual(node1.text, self.node1_text)
        self.assertEqual(node1.block_type, BlockType.HEADING)

        node2 = BlockNode.from_text(self.node2_text)
        self.assertEqual(node2.text, self.node2_text)
        self.assertEqual(node2.block_type, BlockType.CODE)

        node3 = BlockNode.from_text(self.node3_text)
        self.assertEqual(node3.text, self.node3_text)
        self.assertEqual(node3.block_type, BlockType.QUOTE)

        node4 = BlockNode.from_text(self.node4_text)
        self.assertEqual(node4.text, self.node4_text)
        self.assertEqual(node4.block_type, BlockType.UNORDERED_LIST)

        node5 = BlockNode.from_text(self.node5_text)
        self.assertEqual(node5.text, self.node5_text)
        self.assertEqual(node5.block_type, BlockType.ORDERED_LIST)

        node6 = BlockNode.from_text(self.node6_text)
        self.assertEqual(node6.text, self.node6_text)
        self.assertEqual(node6.block_type, BlockType.PARAGRAPH)

    def test_eq(self):
        node1 = BlockNode.from_text(self.node1_text)
        node2 = BlockNode.from_text(self.node1_text)
        self.assertEqual(node1, node2)

    def test_neq(self):
        node1 = BlockNode.from_text(self.node1_text)
        node2 = BlockNode.from_text(self.node2_text)
        self.assertNotEqual(node1, node2)

    def test_blocks_from_text(self):
        text = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = BlockNode.blocks_from_text(text)
        self.assertListEqual(
            [block.text for block in blocks],
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )
        self.assertListEqual(
            [block.block_type for block in blocks],
            [
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.UNORDERED_LIST,
            ],
        )

        text = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = BlockNode.blocks_from_text(text)
        self.assertListEqual(
            [block.text for block in blocks],
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        self.assertListEqual(
            [block.block_type for block in blocks],
            [
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.UNORDERED_LIST,
            ],
        )
