import unittest
from typing import ClassVar

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    node_tag: str = "p"
    node_value: str = "This is a paragraph"
    node2_tag: str = "a"
    node2_value: str = "This is a link"
    node2_props: ClassVar[dict[str, str]] = {"href": "https://www.example.com"}
    node3_tag: str = "div"
    node3_children: ClassVar[list[HTMLNode]] = []
    node3_props: ClassVar[dict[str, str]] = {"id": "content", "class": "h-full flex flex-col", "disabled": True}

    def test_init(self):
        node = HTMLNode(self.node_tag, self.node_value)
        self.assertEqual(node.tag, self.node_tag)
        self.assertEqual(node.value, self.node_value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

        node2 = HTMLNode(self.node2_tag, self.node2_value, props=self.node2_props)
        self.assertEqual(node2.tag, self.node2_tag)
        self.assertEqual(node2.value, self.node2_value)
        self.assertIsNone(node2.children)
        self.assertEqual(node2.props, self.node2_props)

        node3 = HTMLNode(self.node3_tag, children=self.node3_children, props=self.node3_props)
        self.assertEqual(node3.tag, self.node3_tag)
        self.assertIsNone(node3.value)
        self.assertEqual(node3.children, self.node3_children)
        self.assertEqual(node3.props, self.node3_props)

    def test_eq(self):
        node = HTMLNode(self.node_tag, self.node_value)
        node2 = HTMLNode(self.node_tag, self.node_value)
        self.assertEqual(node, node2)

        node3 = HTMLNode(self.node2_tag, self.node2_value, props=self.node2_props)
        node4 = HTMLNode(self.node2_tag, self.node2_value, props=self.node2_props)
        self.assertEqual(node3, node4)

        node5 = HTMLNode(self.node3_tag, children=self.node3_children, props=self.node3_props)
        node6 = HTMLNode(self.node3_tag, children=self.node3_children, props=self.node3_props)
        self.assertEqual(node5, node6)

    def test_neq(self):
        node = HTMLNode(self.node_tag, self.node_value)
        node2 = HTMLNode(self.node2_tag, self.node2_value, props=self.node2_props)
        node3 = HTMLNode(self.node3_tag, children=self.node3_children, props=self.node3_props)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node2, node3)

    def test_html_props(self):
        node2_html_props = ' href="https://www.example.com"'
        node2 = HTMLNode(self.node2_tag, self.node2_value, props=self.node2_props)
        self.assertEqual(node2.props_to_html(), node2_html_props)

        node3_html_props = ' id="content" class="h-full flex flex-col" disabled'
        node3 = HTMLNode(self.node3_tag, children=self.node3_children, props=self.node3_props)
        self.assertEqual(node3.props_to_html(), node3_html_props)


if __name__ == "__main__":
    unittest.main()
