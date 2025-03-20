from dataclasses import dataclass
from typing import Self


@dataclass
class HTMLNode:
    tag: str | None = None
    value: str | None = None
    children: list[Self] | None = None
    props: dict[str, str | bool] | None = None

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html = ""
        if self.props:
            for k, v in self.props.items():
                if not isinstance(v, bool):
                    html += f' {k}="{v}"'
                elif v:
                    html += f' {k}'
        return html
