import unittest

from textnode import TextNode, TextType, split_nodes_delimiter


class TestSplitNodes(unittest.TestCase):
    def test_clean(self):
        node = TextNode("This is text without any delimiter inside", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_other(self):
        node = TextNode("This is text with a `code block` word", TextType.ITALIC)

        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_bold(self):
        node = TextNode("This is text with a **bold type** expression", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold type", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" expression", TextType.TEXT))

    def test_italic(self):
        node = TextNode("This is text with an _italic type_ expression", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with an ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("italic type", TextType.ITALIC))
        self.assertEqual(new_nodes[2], TextNode(" expression", TextType.TEXT))

    def test_code(self):
        node = TextNode("This is text with a `code block` expression", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" expression", TextType.TEXT))

    def test_mixed(self):
        node = TextNode(
            "This is text with a **bold type** expression, an _italic type_ expression and a `code block` expression",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold type", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" expression, an ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("italic type", TextType.ITALIC))
        self.assertEqual(new_nodes[4], TextNode(" expression and a ", TextType.TEXT))
        self.assertEqual(new_nodes[5], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[6], TextNode(" expression", TextType.TEXT))


if __name__ == "__main__":
    unittest.main()
