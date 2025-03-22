import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    node_text = "This is a text node"
    node_type = TextType.BOLD
    node2_text = "This is another text node"
    node2_type = TextType.TEXT
    node2_url = "http://www.example.com"

    def test_init(self):
        node = TextNode(self.node_text, self.node_type)
        self.assertEqual(node.text, self.node_text)
        self.assertEqual(node.text_type, self.node_type)
        self.assertIsNone(node.url)

        node2 = TextNode(self.node2_text, self.node2_type, self.node2_url)
        self.assertEqual(node2.text, self.node2_text)
        self.assertEqual(node2.text_type, self.node2_type)
        self.assertEqual(node2.url, self.node2_url)

    def test_eq(self):
        node = TextNode(self.node_text, self.node_type)
        node2 = TextNode(self.node_text, self.node_type)
        self.assertEqual(node, node2)

        node3 = TextNode(self.node2_text, self.node2_type, self.node2_url)
        node4 = TextNode(self.node2_text, self.node2_type, self.node2_url)
        self.assertEqual(node3, node4)

    def test_neq(self):
        node = TextNode(self.node_text, self.node_type)
        node2 = TextNode(self.node_text, self.node2_type)
        self.assertNotEqual(node, node2)

        node = TextNode(self.node_text, self.node_type)
        node2 = TextNode(self.node_text, self.node_type, self.node2_url)
        self.assertNotEqual(node, node2)

    def test_from_text(self):
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

    def test_leaf_normal(self):
        leaf = TextNode(self.node_text, TextType.TEXT, None).to_leaf()
        self.assertIsNone(leaf.tag)
        self.assertEqual(leaf.value, self.node_text)
        self.assertIsNone(leaf.props)

    def test_leaf_bold(self):
        leaf = TextNode(self.node_text, TextType.BOLD, None).to_leaf()
        self.assertEqual(leaf.tag, "b")
        self.assertEqual(leaf.value, self.node_text)
        self.assertIsNone(leaf.props)

    def test_leaf_italic(self):
        leaf = TextNode(self.node_text, TextType.ITALIC, None).to_leaf()
        self.assertEqual(leaf.tag, "i")
        self.assertEqual(leaf.value, self.node_text)
        self.assertIsNone(leaf.props)

    def test_leaf_code(self):
        leaf = TextNode(self.node_text, TextType.CODE, None).to_leaf()
        self.assertEqual(leaf.tag, "code")
        self.assertEqual(leaf.value, self.node_text)
        self.assertIsNone(leaf.props)

    def test_leaf_link(self):
        leaf1 = TextNode(self.node_text, TextType.LINK, None).to_leaf()
        self.assertEqual(leaf1.tag, "a")
        self.assertEqual(leaf1.value, self.node_text)
        self.assertEqual(leaf1.props, {"href": ""})

        leaf2 = TextNode(self.node_text, TextType.LINK, self.node2_url).to_leaf()
        self.assertEqual(leaf2.tag, "a")
        self.assertEqual(leaf2.value, self.node_text)
        self.assertEqual(leaf2.props, {"href": self.node2_url})

    def test_leaf_image(self):
        leaf1 = TextNode(self.node_text, TextType.IMAGE, None).to_leaf()
        self.assertEqual(leaf1.tag, "img")
        self.assertEqual(leaf1.value, "")
        self.assertEqual(leaf1.props, {"alt": self.node_text, "src": ""})

        leaf2 = TextNode(self.node_text, TextType.IMAGE, self.node2_url).to_leaf()
        self.assertEqual(leaf2.tag, "img")
        self.assertEqual(leaf2.value, "")
        self.assertEqual(leaf2.props, {"alt": self.node_text, "src": self.node2_url})


if __name__ == "__main__":
    unittest.main()
