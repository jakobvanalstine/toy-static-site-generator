from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode
from nodefuncs import text_to_text_nodes, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    return list(
        filter(
            lambda block: block != "",
            [block.strip() for block in markdown.split("\n\n")],
        )
    )


def block_to_block_type(block):
    lines = block.split("\n")
    if len(lines) == 1 and lines[0].startswith(
        ("# ", "## ", "### ", "#### ", "##### ", "###### ")
    ):
        return BlockType.HEADING
    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if lines[0].startswith(">") and lines[-1].startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
            return BlockType.QUOTE
    if lines[0].startswith("- ") and lines[-1].startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST
    if lines[0].startswith("1. ") and lines[-1][0].isdigit():
        for line in lines:
            i = 1
            if not (line.startswith("{i}. ") or line.startswith("1. ")):
                return BlockType.PARAGRAPH
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.CODE:
                node = code_block_to_html_node(block)
            case BlockType.QUOTE:
                node = quote_block_to_html_node(block)
            case BlockType.HEADING:
                node = heading_block_to_html_node(block)
            case BlockType.UNORDERED_LIST:
                node = ulist_block_to_html_node(block)
            case BlockType.ORDERED_LIST:
                node = olist_block_to_html_node(block)
            case BlockType.PARAGRAPH:
                node = paragraph_block_to_html_node(block)
            case _:
                raise ValueError("unknown BlockType")
        nodes.append(node)
    node = ParentNode(tag="div", children=nodes)
    return node


def text_to_children(text):
    children = []
    text_nodes = text_to_text_nodes(text)
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def code_block_to_html_node(block):
    text = block.strip().strip(r"```").lstrip()
    nested_node = LeafNode(tag="code", value=text)
    node = ParentNode(tag="pre", children=[nested_node])
    return node


def quote_block_to_html_node(block):
    text = block.lstrip(">").replace("\n> ", " ").replace("\n>", " ").strip()
    node = ParentNode(tag="blockquote", children=text_to_children(text))
    return node


def heading_block_to_html_node(block):
    i = 0
    while block[i] == "#":
        i += 1
    text = block.strip("#").strip()
    node = ParentNode(tag=f"h{i}", children=text_to_children(text))
    return node


def ulist_block_to_html_node(block):
    item_nodes = []
    lines = block.split("\n")
    for line in lines:
        text = line.lstrip("-").strip()
        item_node = ParentNode(tag="li", children=text_to_children(text))
        item_nodes.append(item_node)
    node = ParentNode(
        tag="ul",
        children=item_nodes,
    )
    return node


def olist_block_to_html_node(block):
    item_nodes = []
    lines = block.split("\n")
    for line in lines:
        text = line.split(". ", 1)[1].strip()
        item_node = ParentNode(tag="li", children=text_to_children(text))
        item_nodes.append(item_node)
    node = ParentNode(tag="ol", children=item_nodes)
    return node


def paragraph_block_to_html_node(block):
    text = block.strip().replace("\n", " ")
    node = ParentNode(tag="p", children=text_to_children(text))
    return node
