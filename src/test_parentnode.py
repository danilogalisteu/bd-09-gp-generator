import unittest
from typing import ClassVar

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    leaf_tag: str = "p"
    leaf_value: str = "This is a paragraph"
    leaf_props: ClassVar[dict[str, str | bool]] = {"style": "bold;"}
    leaf2_tag: str = "a"
    leaf2_value: str = "This is a link"
    leaf2_props: ClassVar[dict[str, str | bool]] = {"href": "https://www.example.com", "disabled": True}
    parent_tag: str = "div"
    parent2_tag: str = "div"
    parent2_props: ClassVar[dict[str, str | bool]] = {"class": "flex flex-column"}

    def test_init(self):
        leaf = LeafNode(self.leaf_tag, self.leaf_value, self.leaf_props)

        node = ParentNode(self.parent_tag, [leaf])
        self.assertEqual(node.tag, self.parent_tag)
        self.assertEqual(node.children, [leaf])
        self.assertIsNone(node.props)

        node2 = ParentNode(self.parent2_tag, [leaf], props=self.parent2_props)
        self.assertEqual(node2.tag, self.parent2_tag)
        self.assertEqual(node2.children, [leaf])
        self.assertEqual(node2.props, self.parent2_props)

    def test_eq(self):
        leaf = LeafNode(self.leaf_tag, self.leaf_value, self.leaf_props)

        node = ParentNode(self.parent_tag, [leaf])
        node2 = ParentNode(self.parent_tag, [leaf])
        self.assertEqual(node, node2)

        node3 = ParentNode(self.parent2_tag, [leaf], props=self.parent2_props)
        node4 = ParentNode(self.parent2_tag, [leaf], props=self.parent2_props)
        self.assertEqual(node3, node4)

    def test_neq(self):
        leaf = LeafNode(self.leaf_tag, self.leaf_value, self.leaf_props)

        node = ParentNode(self.parent_tag, [leaf])
        node2 = ParentNode(self.parent2_tag, [leaf], props=self.parent2_props)
        self.assertNotEqual(node, node2)

    def test_html_props(self):
        leaf = LeafNode(self.leaf_tag, self.leaf_value, self.leaf_props)

        node2_html_props = ' class="flex flex-column"'
        node2 = ParentNode(self.parent2_tag, [leaf], props=self.parent2_props)
        self.assertEqual(node2.props_to_html(), node2_html_props)

    def test_html_with_children(self):
        leaf = LeafNode(self.leaf_tag, self.leaf_value, self.leaf_props)
        leaf2 = LeafNode(self.leaf2_tag, self.leaf2_value, self.leaf2_props)

        node_html = '<div><p style="bold;">This is a paragraph</p></div>'
        node = ParentNode(self.parent_tag, [leaf])
        self.assertEqual(node.to_html(), node_html)

        node2_html = '<div class="flex flex-column"><a href="https://www.example.com" disabled>This is a link</a></div>'
        node2 = ParentNode(self.parent2_tag, [leaf2], props=self.parent2_props)
        self.assertEqual(node2.to_html(), node2_html)

    def test_html_with_grandchildren(self):
        leaf = LeafNode(self.leaf_tag, self.leaf_value, self.leaf_props)
        leaf2 = LeafNode(self.leaf2_tag, self.leaf2_value, self.leaf2_props)
        node = ParentNode(self.parent_tag, [leaf])
        node2 = ParentNode(self.parent2_tag, [node, leaf2], props=self.parent2_props)

        node2_html = '<div class="flex flex-column"><div><p style="bold;">This is a paragraph</p></div><a href="https://www.example.com" disabled>This is a link</a></div>'
        self.assertEqual(node2.to_html(), node2_html)


if __name__ == "__main__":
    unittest.main()
