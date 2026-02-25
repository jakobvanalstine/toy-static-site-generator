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

    def test_type_error(self):
        with self.assertRaises(TypeError):
            node = TextNode(0, 0, 0)

    def test_value_error(self):
        with self.assertRaises(ValueError):
            node = TextNode("", "bold", "")

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


if __name__ == "__main__":
    unittest.main()
