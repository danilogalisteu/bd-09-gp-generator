import unittest

from textnode import TextNode


class TestExtract(unittest.TestCase):
    def test_clean(self):
        text = "This is text without any images or links"

        images = TextNode.extract_markdown_images(text)
        self.assertListEqual(images, [])

        links = TextNode.extract_markdown_links(text)
        self.assertListEqual(links, [])

    def test_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = TextNode.extract_markdown_images(text)
        self.assertListEqual(
            images,
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")],
        )

    def test_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = TextNode.extract_markdown_links(text)
        self.assertListEqual(
            links,
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],
        )

    def test_mixed(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) image and a link [to boot dev](https://www.boot.dev)"

        images = TextNode.extract_markdown_images(text)
        self.assertListEqual(images, [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

        links = TextNode.extract_markdown_links(text)
        self.assertListEqual(links, [("to boot dev", "https://www.boot.dev")])


if __name__ == "__main__":
    unittest.main()
