import unittest

from htmlnode import HTMLNode, LeafNode


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


if __name__ == "__main__":
    unittest.main()
