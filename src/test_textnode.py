import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_init(self):
        node = TextNode("This a text node", TextType.BOLD)
        self.assertEqual(node.text, "This a text node")
        self.assertEqual(node.text_type, TextType.BOLD)
        self.assertEqual(node.url, None)
    
        
    def test_repr(self):
        # Test the __repr__ method
        node = TextNode("Hello", TextType.LINK, "http://example.com")
        self.assertEqual(repr(node), "TextNode(Hello, link, http://example.com)")
        
        
if __name__ == "__main__":
    unittest.main()