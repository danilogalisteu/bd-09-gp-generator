import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    node_text = "This is a text node"
    node_type = TextType.BOLD
    node2_text = "This is another text node"
    node2_type = TextType.NORMAL
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


if __name__ == "__main__":
    unittest.main()
