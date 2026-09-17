
class HTMLNode:
    def __init__(
            self, tag: str | None = None, 
            value: str | None = None, 
            children: list[HTMLNode] | None = None, 
            props: dict[str, str] | None = None
            ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        atr_list = []
        for k in self.props.keys():
            atr_list.append(f'{k}="{self.props[k]}"')

        return " " + " ".join(atr_list)

    def __repr__(self) -> str:
        return f'Tag: {self.tag}\nValue: {self.value}\nAttributes: {self.props_to_html()}'

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None or self.tag == "":
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f'Tag: {self.tag}\nValue: {self.value}\nAttributes: {self.props_to_html()}'

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError("Missing Tag")
        if not self.children:
            raise ValueError("Missing children")

        childen_list = []
        for c in self.children:
            childen_list.append(f"{c.to_html()}")
        return f"<{self.tag}{self.props_to_html()}>{''.join(childen_list)}</{self.tag}>"
        