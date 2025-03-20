from dataclasses import dataclass


@dataclass
class LeafNode:
    tag: str | None
    value: str | None
    props: dict[str, str | bool] | None = None

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"

    def to_html(self):
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>" if self.tag else self.value

    def props_to_html(self):
        html = ""
        if self.props:
            for k, v in self.props.items():
                if not isinstance(v, bool):
                    html += f' {k}="{v}"'
                elif v:
                    html += f' {k}'
        return html
