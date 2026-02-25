from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode


def main():
    dummy = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(repr(dummy))


if __name__ == "__main__":
    main()
