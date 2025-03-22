import unittest

from blocknode import BlockNode, BlockType
from textnode import TextNode, TextType


class TestParseText(unittest.TestCase):
    def test_splittext(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = TextNode.from_text(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_splitblocks(self):
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

    def test_blocktypes(self):
        blocks = [
            (BlockType.HEADING, "# This is a heading"),
            (BlockType.CODE, "```\nthis is a code block\nhere continues the code block\nthe code block ends here\n```"),
            (
                BlockType.QUOTE,
                "> This is a quote block\n> This continues the quote block\n> This is the end of the quote block",
            ),
            (
                BlockType.UNORDERED_LIST,
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ),
            (BlockType.ORDERED_LIST, "1. abcd\n2. efgh\n3. ijkl"),
            (BlockType.PARAGRAPH, "This is a paragraph of text. It has some **bold** and _italic_ words inside of it."),
        ]
        for block in blocks:
            self.assertEqual(block[0], BlockNode.get_block_type(block[1]))

    def test_blockheading(self):
        self.assertEqual(BlockType.HEADING, BlockNode.get_block_type("# This is a heading"))
        self.assertEqual(BlockType.HEADING, BlockNode.get_block_type("## This is a heading"))
        self.assertEqual(BlockType.HEADING, BlockNode.get_block_type("### This is a heading"))
        self.assertEqual(BlockType.HEADING, BlockNode.get_block_type("#### This is a heading"))
        self.assertEqual(BlockType.HEADING, BlockNode.get_block_type("##### This is a heading"))
        self.assertEqual(BlockType.HEADING, BlockNode.get_block_type("###### This is a heading"))
        self.assertNotEqual(BlockType.HEADING, BlockNode.get_block_type("This is not a heading"))
        self.assertNotEqual(BlockType.HEADING, BlockNode.get_block_type(" # This is not a heading"))
        self.assertNotEqual(BlockType.HEADING, BlockNode.get_block_type("#This is not a heading"))
        self.assertNotEqual(BlockType.HEADING, BlockNode.get_block_type("####### This is not a heading"))

    def test_blockcode(self):
        self.assertEqual(BlockType.CODE, BlockNode.get_block_type("```single-line code block```"))
        self.assertEqual(BlockType.CODE, BlockNode.get_block_type("```\nmulti-line code block\n```"))
        self.assertEqual(BlockType.CODE, BlockNode.get_block_type("```\nmulti-line\ncode block\n```"))
        self.assertNotEqual(BlockType.CODE, BlockNode.get_block_type("This is not a code block"))
        self.assertNotEqual(BlockType.CODE, BlockNode.get_block_type(" ```This is not a code block```"))
        self.assertNotEqual(BlockType.CODE, BlockNode.get_block_type("```This is not a code block"))
        self.assertNotEqual(BlockType.CODE, BlockNode.get_block_type(" ```This is not a code block"))

    def test_blockquote(self):
        self.assertEqual(BlockType.QUOTE, BlockNode.get_block_type("> This is a single-line quote block"))
        self.assertEqual(BlockType.QUOTE, BlockNode.get_block_type("> This is a multi-line\n> quote block"))
        self.assertEqual(BlockType.QUOTE, BlockNode.get_block_type("> This is\n> a multi-line\n> quote block"))
        self.assertEqual(BlockType.QUOTE, BlockNode.get_block_type(">This is\n>a multi-line\n>quote block"))
        self.assertNotEqual(BlockType.QUOTE, BlockNode.get_block_type("This is not a quote block"))
        self.assertNotEqual(BlockType.QUOTE, BlockNode.get_block_type(" > This is not a quote block"))
        self.assertNotEqual(BlockType.QUOTE, BlockNode.get_block_type(" >This is not a quote block"))

    def test_blockunordered(self):
        self.assertEqual(BlockType.UNORDERED_LIST, BlockNode.get_block_type("- This is a single-line item list"))
        self.assertEqual(
            BlockType.UNORDERED_LIST,
            BlockNode.get_block_type("- This is the first list item in a list block\n- This is the second list item"),
        )
        self.assertEqual(
            BlockType.UNORDERED_LIST,
            BlockNode.get_block_type(
                "- This is the first list item in a list block\n- This is the second list item\n- This is another list item",
            ),
        )
        self.assertNotEqual(BlockType.UNORDERED_LIST, BlockNode.get_block_type("This is not a list block"))
        self.assertNotEqual(BlockType.UNORDERED_LIST, BlockNode.get_block_type(" - This is not a list block"))
        self.assertNotEqual(BlockType.UNORDERED_LIST, BlockNode.get_block_type("-This is not a list block"))
        self.assertNotEqual(BlockType.UNORDERED_LIST, BlockNode.get_block_type(" -This is not a list block"))

    def test_blockordered(self):
        self.assertEqual(BlockType.ORDERED_LIST, BlockNode.get_block_type("1. This is a single-line item list"))
        self.assertEqual(
            BlockType.ORDERED_LIST,
            BlockNode.get_block_type("1. This is the first list item in a list block\n2. This is the second list item"),
        )
        self.assertEqual(
            BlockType.ORDERED_LIST,
            BlockNode.get_block_type(
                "1. This is the first list item in a list block\n2. This is the second list item\n3. This is another list item",
            ),
        )
        self.assertNotEqual(BlockType.ORDERED_LIST, BlockNode.get_block_type("This is not a list block"))
        self.assertNotEqual(BlockType.ORDERED_LIST, BlockNode.get_block_type(" 1. This is not a list block"))
        self.assertNotEqual(BlockType.ORDERED_LIST, BlockNode.get_block_type("1.This is not a list block"))
        self.assertNotEqual(BlockType.ORDERED_LIST, BlockNode.get_block_type(" 1.This is not a list block"))

    def test_blockparagraph(self):
        self.assertEqual(BlockType.PARAGRAPH, BlockNode.get_block_type("This is not a heading"))
        self.assertEqual(BlockType.PARAGRAPH, BlockNode.get_block_type(" # This is not a heading"))
        self.assertEqual(BlockType.PARAGRAPH, BlockNode.get_block_type("#This is not a heading"))
        self.assertEqual(BlockType.PARAGRAPH, BlockNode.get_block_type("####### This is not a heading"))
        self.assertEqual(BlockType.PARAGRAPH, BlockNode.get_block_type("This is not a code block"))
        self.assertEqual(BlockType.PARAGRAPH, BlockNode.get_block_type(" ```This is not a code block```"))
        self.assertEqual(BlockType.PARAGRAPH, BlockNode.get_block_type("```This is not a code block"))
        self.assertEqual(BlockType.PARAGRAPH, BlockNode.get_block_type(" ```This is not a code block"))
        self.assertEqual(BlockType.PARAGRAPH, BlockNode.get_block_type("This is not a quote block"))
        self.assertEqual(BlockType.PARAGRAPH, BlockNode.get_block_type(" > This is not a quote block"))
        self.assertEqual(BlockType.PARAGRAPH, BlockNode.get_block_type(" >This is not a quote block"))
        self.assertEqual(BlockType.PARAGRAPH, BlockNode.get_block_type("This is not a list block"))
        self.assertEqual(BlockType.PARAGRAPH, BlockNode.get_block_type(" - This is not a list block"))
        self.assertEqual(BlockType.PARAGRAPH, BlockNode.get_block_type("-This is not a list block"))
        self.assertEqual(BlockType.PARAGRAPH, BlockNode.get_block_type(" -This is not a list block"))
        self.assertEqual(BlockType.PARAGRAPH, BlockNode.get_block_type("This is not a list block"))
        self.assertEqual(BlockType.PARAGRAPH, BlockNode.get_block_type(" 1. This is not a list block"))
        self.assertEqual(BlockType.PARAGRAPH, BlockNode.get_block_type("1.This is not a list block"))
        self.assertEqual(BlockType.PARAGRAPH, BlockNode.get_block_type(" 1.This is not a list block"))
        self.assertNotEqual(BlockType.PARAGRAPH, BlockNode.get_block_type("# This is a heading"))
        self.assertNotEqual(BlockType.PARAGRAPH, BlockNode.get_block_type("```single-line code block```"))
        self.assertNotEqual(BlockType.PARAGRAPH, BlockNode.get_block_type("> This is a single-line quote block"))
        self.assertNotEqual(BlockType.PARAGRAPH, BlockNode.get_block_type("- This is a single-line item list"))
        self.assertNotEqual(BlockType.PARAGRAPH, BlockNode.get_block_type("1. This is a single-line item list"))


if __name__ == "__main__":
    unittest.main()
