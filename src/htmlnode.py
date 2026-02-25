class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag if isinstance(tag, str) and tag != "" else None
        self.value = value if isinstance(value, str) and tag != "" else None
        self.children = (
            children if isinstance(children, list) and children != [] else None
        )
        self.props = props if isinstance(props, dict) and props != {} else None

    def to_html(self):
        raise NotImplementedError
        # Child classes will override this

    def props_to_html(self):
        if self.props is None or not isinstance(self.props, dict):
            return ""

        return "".join(f' {k}="{v}"' for k, v in self.props.items())

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
