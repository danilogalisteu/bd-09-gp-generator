import unittest

from markdownparser import MD_IMG_FORMAT, MD_IMG_RE_PATTERN, MD_LINK_FORMAT, MD_LINK_RE_PATTERN, nodes_from_text, split_nodes_delimiter, split_nodes_pattern
from textnode import TextNode, TextType


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

    def test_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_pattern([node], MD_IMG_RE_PATTERN, TextType.IMAGE, MD_IMG_FORMAT)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0], TextNode("This is text with an ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"))
        self.assertEqual(new_nodes[2], TextNode(" and another ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"))

    def test_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_pattern([node], MD_LINK_RE_PATTERN, TextType.LINK, MD_LINK_FORMAT)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0], TextNode("This is text with a link ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"))
        self.assertEqual(new_nodes[2], TextNode(" and ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"))

    def test_mixed(self):
        node = TextNode(
            "This is text with a **bold type** expression, an _italic type_ expression and a `code block` expression. It also has [a link to boot dev](https://www.boot.dev) and ![an image](https://i.imgur.com/zjjcJKZ.png).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_pattern(new_nodes, MD_IMG_RE_PATTERN, TextType.IMAGE, MD_IMG_FORMAT)
        new_nodes = split_nodes_pattern(new_nodes, MD_LINK_RE_PATTERN, TextType.LINK, MD_LINK_FORMAT)
        self.assertEqual(len(new_nodes), 11)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold type", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" expression, an ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("italic type", TextType.ITALIC))
        self.assertEqual(new_nodes[4], TextNode(" expression and a ", TextType.TEXT))
        self.assertEqual(new_nodes[5], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[6], TextNode(" expression. It also has ", TextType.TEXT))
        self.assertEqual(new_nodes[7], TextNode("a link to boot dev", TextType.LINK, "https://www.boot.dev"))
        self.assertEqual(new_nodes[8], TextNode(" and ", TextType.TEXT))
        self.assertEqual(new_nodes[9], TextNode("an image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"))
        self.assertEqual(new_nodes[10], TextNode(".", TextType.TEXT))

    def test_text(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = nodes_from_text(text)
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


if __name__ == "__main__":
    unittest.main()
