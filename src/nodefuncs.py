import re

from textnode import TextType, TextNode
from htmlnode import LeafNode


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(
                "img", "", {"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise TypeError(f"not a TextType: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    def helper():
        for node in old_nodes:
            if node.text_type != TextType.PLAIN:
                yield node
                continue

            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception(
                    f'No matching closing delimiter found: "{node.text}"'
                )

            for i, substring in enumerate(split_text):
                if substring == "":
                    continue
                elif i % 2 == 0:
                    yield TextNode(substring, TextType.PLAIN)
                else:
                    yield TextNode(substring, text_type)

    return list(helper())


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?:[^!]|$)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    def helper():
        for node in old_nodes:
            if node.text_type != TextType.PLAIN:
                yield node
                continue
            text = node.text
            images = extract_markdown_images(text)
            if len(images) == 0:
                yield node
                continue
            for image in images:
                parts = text.split(f"![{image[0]}]({image[1]})", 1)
                if len(parts) != 2:
                    raise Exception("Invalid markdown")
                if parts[0] != "":
                    yield TextNode(parts[0], TextType.PLAIN)
                yield TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
                text = parts[1]
        if text != "":
            yield TextNode(text, TextType.PLAIN)

    return list(helper())


def split_nodes_link(old_nodes):
    def helper():
        for node in old_nodes:
            if node.text_type != TextType.PLAIN:
                yield node
                continue
            text = node.text
            links = extract_markdown_links(text)
            if len(links) == 0:
                yield node
                continue
            for link in links:
                parts = text.split(f"[{link[0]}]({link[1]})", 1)
                if len(parts) != 2:
                    raise Exception("Invalid markdown")
                if parts[0] != "":
                    yield TextNode(parts[0], TextType.PLAIN)
                yield TextNode(
                    link[0],
                    TextType.LINK,
                    link[1],
                )
                text = parts[1]
        if text != "":
            yield TextNode(text, TextType.PLAIN)

    return list(helper())
