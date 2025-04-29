import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    
    def test_init(self):
        
        htmlnode = HTMLNode("p", "random text")
        self.assertEqual(htmlnode.tag, "p")
        self.assertEqual(htmlnode.value, "random text")
        
    def test_props_to_html(self):
        props = {
    "href": "https://www.google.com",
    "target": "_blank",
}
        htmlnode = HTMLNode("p", "random text", None, props)

        self.assertEqual(htmlnode.props_to_html(), ' href="https://www.google.com" target="_blank"')
        
    
    def test_repr(self):
        props = {
    "href": "https://www.google.com",
    "target": "_blank",
}
        htmlnode = HTMLNode("p", "random text", None, props)
        expected = "HTMLNode(tag='p', value='random text', children=[], props={'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(repr(htmlnode), expected)
        
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
        node2 = LeafNode("a", "Hello, world!")
        self.assertEqual(node2.to_html(), "<a>Hello, world!</a>")
        
        node3 = LeafNode("b", "Hello, world!")
        self.assertEqual(node3.to_html(), "<b>Hello, world!</b>")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
            )
    
    def test_nested_parents(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        parent2_node = ParentNode("div", [parent_node])
        parent3_node = ParentNode("div", [parent2_node])
        self.assertEqual(
            parent3_node.to_html(),
            "<div><div><div><span><b>grandchild</b></span></div></div></div>",
            )
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, url="https://www.youtube.com/")
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, "href:https://www.youtube.com/")
        self.assertEqual(html_node.value, "This is a link node")

    def test_image(self):
        node = TextNode('', TextType.IMAGE, url="https://www.youtube.com/")
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, "src:https://www.youtube.com/, alt:")
        self.assertEqual(html_node.value, '')
        
if __name__ == "__main__":
    unittest.main()