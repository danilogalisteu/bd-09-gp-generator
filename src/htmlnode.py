from typing import Self


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[Self] | None = None,
        props: dict[str, str | bool] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode(tag='{self.tag}', value='{self.value}', children={self.children}, props={self.props})"

    def __eq__(self, other: Self):
        return (
            (self.tag == other.tag)
            and (self.value == other.value)
            and (self.children == other.children)
            and (self.props == other.props)
        )

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html = ""
        if self.props:
            for k, v in self.props.items():
                if not isinstance(v, bool):
                    html += f' {k}="{v}"'
                elif v:
                    html += f" {k}"
        return html
