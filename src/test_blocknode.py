import unittest

from blocknode import BlockNode, BlockType
from htmlnode import LeafNode, ParentNode


class TestBlockNode(unittest.TestCase):
    node1_text = "# This is a heading"
    node2_text = "```This is a single-line code block```"
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

    def test_parent_heading(self):
        parent = BlockNode.from_text(self.node1_text).to_parent()
        self.assertIsInstance(parent, ParentNode)
        self.assertEqual(parent.tag, "h1")
        self.assertListEqual(parent.children, [LeafNode(None, "This is a heading")])
        self.assertIsNone(parent.props)

    def test_parent_code(self):
        parent = BlockNode.from_text(self.node2_text).to_parent()
        self.assertIsInstance(parent, ParentNode)
        self.assertEqual(parent.tag, "pre")
        self.assertListEqual(parent.children, [LeafNode("code", "This is a single-line code block")])
        self.assertIsNone(parent.props)

    def test_parent_quote(self):
        parent = BlockNode.from_text(self.node3_text).to_parent()
        self.assertIsInstance(parent, ParentNode)
        self.assertEqual(parent.tag, "blockquote")
        self.assertListEqual(parent.children, [LeafNode(None, " This is a single-line quote block")])
        self.assertIsNone(parent.props)

    def test_parent_unordered(self):
        parent = BlockNode.from_text(self.node4_text).to_parent()
        self.assertIsInstance(parent, ParentNode)
        self.assertEqual(parent.tag, "ul")
        self.assertListEqual(
            parent.children,
            [
                ParentNode(
                    "li",
                    [
                        LeafNode(None, "This is a single-line item list"),
                    ],
                ),
            ],
        )
        self.assertIsNone(parent.props)

    def test_parent_ordered(self):
        parent = BlockNode.from_text(self.node5_text).to_parent()
        self.assertIsInstance(parent, ParentNode)
        self.assertEqual(parent.tag, "ol")
        self.assertListEqual(
            parent.children,
            [
                ParentNode(
                    "li",
                    [
                        LeafNode(None, "This is a single-line item list"),
                    ],
                ),
            ],
        )
        self.assertIsNone(parent.props)

    def test_parent_paragraph(self):
        parent = BlockNode.from_text(self.node6_text).to_parent()
        self.assertIsInstance(parent, ParentNode)
        self.assertEqual(parent.tag, "p")
        self.assertListEqual(
            parent.children,
            [
                LeafNode(None, "This is text with a "),
                LeafNode("b", value="bold type"),
                LeafNode(None, value=" expression, an "),
                LeafNode("i", value="italic type"),
                LeafNode(None, value=" expression and a "),
                LeafNode("code", value="code block"),
                LeafNode(None, value=" expression. It also has "),
                LeafNode("a", value="a link to boot dev", props={"href": "https://www.boot.dev"}),
                LeafNode(None, value=" and "),
                LeafNode("img", value="", props={"alt": "an image", "src": "https://i.imgur.com/zjjcJKZ.png"}),
                LeafNode(None, value="."),
            ],
        )
        self.assertIsNone(parent.props)

    def test_document_html(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        html = BlockNode.from_document(md).to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        html = BlockNode.from_document(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
