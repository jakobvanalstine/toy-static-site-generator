class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        if tag is not None and not isinstance(tag, str):
            raise TypeError("HTMLNode.tag must be truthy str or None")
        elif tag == "":
            raise ValueError("HTMLNode.tag must be truthy str or None")

        if value is not None and not isinstance(value, str):
            raise TypeError("HTMLNode.value must be str or None")

        if children is not None and not isinstance(children, list):
            raise TypeError("HTMLNode.children must be truthy list or None")
        elif children == []:
            raise ValueError("HTMLNode.children must be truthy list or None")

        if props is not None and (not props or not isinstance(props, dict)):
            raise TypeError("HTMLNode.props must be truthy dict or None")
        elif props == {}:
            raise ValueError("HTMLNode.props must be truthy dict or None")

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
        # Child classes will override this

    def props_to_html(self):
        if self.props is None:
            return ""

        return "".join(f' {k}="{v}"' for k, v in self.props.items())

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode.value must not be None")

        if self.tag is None:
            return f"{self.value}"

        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}{self.value}>"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode.tag must not be None")

        if self.children is None:
            raise ValueError("ParentNode.children must not be None")

        injection = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{injection}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
