from dataclasses import dataclass

from htmlnode import HTMLNode


@dataclass
class LeafNode(HTMLNode):
    tag: str | None
    value: str | None
    props: dict[str, str | bool] | None = None

    def to_html(self):
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>" if self.tag else self.value
