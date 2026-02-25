class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        if tag is not None and (not tag or not isinstance(tag, str)):
            raise TypeError("HTMLNode.tag must be truthy str or None")

        if value is not None and (not value or not isinstance(value, str)):
            raise TypeError("HTMLNode.value must be truthy str or None")

        if children is not None and (
            not children or not isinstance(children, list)
        ):
            raise TypeError("HTMLNode.children must be truthy list or None")

        if props is not None and (not props or not isinstance(props, dict)):
            raise TypeError("HTMLNode.props must be truthy dict or None")

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
