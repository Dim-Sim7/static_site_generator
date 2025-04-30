from textnode import TextNode, TextType
from split_delimiter import split_nodes_delimiter, split_nodes_images
import unittest


class Test_Split_Delimiter(unittest.TestCase):
    
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
]
        self.assertEqual(new_nodes, expected)
        
    def test_split_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.CODE)
        expected = [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("bold", TextType.BOLD),
    TextNode(" word", TextType.TEXT),
]
        self.assertEqual(new_nodes, expected)
    
    def test_split_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.CODE)
        expected = [
    TextNode("This is text with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word", TextType.TEXT),
]
        self.assertEqual(new_nodes, expected)
    
    def test_split_none(self):
        node = TextNode("This is text with a nothing word", TextType.TEXT)
        
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "", TextType.CODE)
        expected = "Invalid Delimiter"
        self.assertEqual(str(context.exception), expected)
        
    
    def test_split_error(self):
        node = TextNode("This is _text_ with a nothing word", TextType.IMAGE, url = "2334")

        new_nodes = split_nodes_delimiter([node], "_", TextType.IMAGE)
        repr(new_nodes)
        expected = [TextNode("This is _text_ with a nothing word", TextType.IMAGE)]
        self.assertEqual(new_nodes, expected)
    
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()