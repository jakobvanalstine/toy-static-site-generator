import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from nodefuncs import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ne(self):
        node = TextNode("This is a text node", TextType.LINK, "www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            node = TextNode(0, 0, 0)

    def test_value_error(self):
        with self.assertRaises(ValueError):
            node = TextNode("", TextType.LINK, "")

    def test_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertTrue(node.url is None)

    def test_repr(self):
        node = TextNode(
            "This is a text node", TextType.LINK, "https://www.boot.dev"
        )
        self.assertEqual(
            repr(node),
            "TextNode(This is a text node, link, https://www.boot.dev)",
        )


class TestHTMLNode(unittest.TestCase):
    def test_type_error(self):
        with self.assertRaises(TypeError):
            node = HTMLNode(0, 0, 0, 0)

    def test_value_error(self):
        with self.assertRaises(ValueError):
            node = HTMLNode("", "", [], {})

    def test_none(self):
        node = HTMLNode()
        self.assertTrue(
            node.tag is None
            and node.value is None
            and node.children is None
            and node.props is None
        )

    def test_repr(self):
        node = HTMLNode(
            "a",
            "Boot.dev",
            None,
            {
                "href": "https://www.boot.dev",
                "target": "_blank",
            },
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(a, Boot.dev, None, {'href': 'https://www.boot.dev', 'target': '_blank'})",
        )

    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Boot.dev",
            None,
            {
                "href": "https://www.boot.dev",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.boot.dev" target="_blank"',
        )


class TestLeafNode(unittest.TestCase):
    def test_type_error(self):
        with self.assertRaises(TypeError):
            node = HTMLNode(0, 0, 0, 0)

    def test_value_error(self):
        with self.assertRaises(ValueError):
            node = HTMLNode("", "", [], {})

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), "<div><span>child</span></div>"
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


def test_text(self):
    node = TextNode("This is a text node", TextType.PLAIN)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")

def test_image(self):
    node = TextNode("Diagram showing...", TextType.IMAGE, "https://www.reliablesource.com")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "img")
    self.assertEqual(html_node.value, "")
    self.assertEqual(
        html_node.props,
        {"src": "https://www.reliablesource.com", "alt": "Diagram showing..."},
    )

def test_bold(self):
    node = TextNode("OBS", TextType.BOLD)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "b")
    self.assertEqual(html_node.value, "OBS")


if __name__ == "__main__":
    unittest.main()
