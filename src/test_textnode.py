import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ne(self):
        node = TextNode("This is a text node", TextType.LINK, "www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_none(self):
        node = TextNode(1, [])
        node2 = TextNode(1, [], TextType.BOLD)
        self.assertTrue(
            node.text is None and node.text_type is None and node.url is None
        )
        self.assertTrue(
            node2.text is None
            and node2.text_type is None
            and node2.url is None
        )

    def test_repr(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(
            repr(node),
            "TextNode(This is a text node, link, https://www.boot.dev)",
        )


if __name__ == "__main__":
    unittest.main()
