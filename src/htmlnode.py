from dataclasses import dataclass
from typing import Self


@dataclass
class HTMLNode:
    tag: str | None = None
    value: str | None = None
    children: list[Self] | None = None
    props: dict[str, str] | None = None

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return "".join(f' {k}="{v}"' for k, v in self.props.items()) if self.props else ""
