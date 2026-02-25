import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
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

    def test_none(self):
        node = HTMLNode()
        self.assertTrue(
            node.tag is None
            and node.value is None
            and node.children is None
            and node.props is None
        )
        node2 = HTMLNode("", "", [], {})
        self.assertTrue(
            node2.tag == None
            and node2.value == None
            and node2.children == None
            and node2.props == None
        )


if __name__ == "__main__":
    unittest.main()
