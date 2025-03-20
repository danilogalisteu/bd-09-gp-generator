from dataclasses import dataclass

from htmlnode import HTMLNode


@dataclass
class ParentNode(HTMLNode):
    tag: str
    children: list[HTMLNode]
    props: dict[str, str | bool] | None = None

    def to_html(self):
        if not self.tag:
            raise ValueError("missing tag")
        if not self.children:
            raise ValueError("missing children")

        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html
