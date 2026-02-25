from enum import Enum


class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        if not text or not isinstance(text, str):
            raise TypeError("TextNode.text must be truthy str")

        if not isinstance(text_type, TextType):
            raise TypeError("TextNode.text_type must be TextType")

        if url is not None and (not url or not isinstance(url, str)):
            raise TypeError("TextNode.url must be truthy str or None")

        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
