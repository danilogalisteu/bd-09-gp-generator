import unittest
from typing import ClassVar

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    node_tag: str = "p"
    node_value: str = "This is a paragraph"
    node2_tag: str = "a"
    node2_value: str = "This is a link"
    node2_props: ClassVar[dict[str, str]] = {"href": "https://www.example.com", "disabled": True}

    def test_init(self):
        node = LeafNode(self.node_tag, self.node_value)
        self.assertEqual(node.tag, self.node_tag)
        self.assertEqual(node.value, self.node_value)
        self.assertIsNone(node.props)

        node2 = LeafNode(self.node2_tag, self.node2_value, props=self.node2_props)
        self.assertEqual(node2.tag, self.node2_tag)
        self.assertEqual(node2.value, self.node2_value)
        self.assertEqual(node2.props, self.node2_props)

    def test_eq(self):
        node = LeafNode(self.node_tag, self.node_value)
        node2 = LeafNode(self.node_tag, self.node_value)
        self.assertEqual(node, node2)

        node3 = LeafNode(self.node2_tag, self.node2_value, props=self.node2_props)
        node4 = LeafNode(self.node2_tag, self.node2_value, props=self.node2_props)
        self.assertEqual(node3, node4)

    def test_neq(self):
        node = LeafNode(self.node_tag, self.node_value)
        node2 = LeafNode(self.node2_tag, self.node2_value, props=self.node2_props)
        self.assertNotEqual(node, node2)

    def test_html_props(self):
        node2_html_props = ' href="https://www.example.com" disabled'
        node2 = LeafNode(self.node2_tag, self.node2_value, props=self.node2_props)
        self.assertEqual(node2.props_to_html(), node2_html_props)

    def test_html(self):
        node_html = '<p>This is a paragraph</p>'
        node = LeafNode(self.node_tag, self.node_value)
        self.assertEqual(node.to_html(), node_html)

        node2_html = '<a href="https://www.example.com" disabled>This is a link</a>'
        node2 = LeafNode(self.node2_tag, self.node2_value, props=self.node2_props)
        self.assertEqual(node2.to_html(), node2_html)


if __name__ == "__main__":
    unittest.main()
