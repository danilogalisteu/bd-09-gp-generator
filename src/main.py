import pathlib
import shutil

from blocknode import BlockNode

PATH_TEMPLATE = pathlib.Path("./template.html")
PATH_CONTENT = pathlib.Path("./content")
PATH_STATIC = pathlib.Path("./static")
PATH_PUBLIC = pathlib.Path("./public")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    content_md = from_path.read_text()
    doc = BlockNode.from_document(content_md)

    title_nodes = [node for node in doc.children if node.tag == "h1"]
    if not title_nodes:
        raise ValueError("missing h1 heading", from_path)

    title = title_nodes[0].children[0].value
    content_html = doc.to_html()
    template_html = template_path.read_text()
    page_html = template_html.replace("{{ Title }}", title).replace("{{ Content }}", content_html)

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(page_html)


def build():
    if PATH_PUBLIC.exists():
        shutil.rmtree(PATH_PUBLIC)

    shutil.copytree(PATH_STATIC, PATH_PUBLIC)

    for from_path in PATH_CONTENT.glob("**/*.md"):
        dest_path = PATH_PUBLIC / from_path.relative_to(PATH_CONTENT).with_suffix(".html")
        generate_page(from_path, PATH_TEMPLATE, dest_path)


def main():
    build()


if __name__ == "__main__":
    main()
