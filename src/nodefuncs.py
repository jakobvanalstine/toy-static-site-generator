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
