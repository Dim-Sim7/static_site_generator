from textnode import TextNode, TextType
from split_delimiter import split_nodes_delimiter, split_nodes_images, split_nodes_links
import unittest


class Test_Split_Delimiter(unittest.TestCase):
    
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`")
        expected = [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
]
        self.assertEqual(new_nodes, expected)
        
    def test_split_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**")
        expected = [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("bold", TextType.BOLD),
    TextNode(" word", TextType.TEXT),
]
        self.assertEqual(new_nodes, expected)
    
    def test_split_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_")
        expected = [
    TextNode("This is text with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word", TextType.TEXT),
]
        self.assertEqual(new_nodes, expected)
    
    def test_split_none(self):
        node = TextNode("This is text with a nothing word", TextType.TEXT)
        
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "")
        expected = "Invalid Delimiter"
        self.assertEqual(str(context.exception), expected)
        
    
    def test_split_error(self):
        node = TextNode("This is _text_ with a nothing word", TextType.IMAGE, url = "2334")

        new_nodes = split_nodes_delimiter([node], "_")
      
        expected = [TextNode("This is _text_ with a nothing word", TextType.IMAGE, "2334")]
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
    def test_split_images_2(self):
        node = TextNode(
            "This is text with anasdasda !![!image](https://i.imgur.com/zjjcJKZ.png)and another![second image](https://i.imgur.com/3elNhQu.png) ok ok oko k ok ok",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with anasdasda !", TextType.TEXT),
                TextNode("!image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("and another", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" ok ok oko k ok ok", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_nodes_images_single(self):
        node = TextNode("This is an ![image](https://img.com/image.png)", TextType.TEXT)
        result = split_nodes_images([node])
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://img.com/image.png"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_images_multiple(self):
        node = TextNode("Before ![one](url1.com) middle ![two](url2.com) end", TextType.TEXT)
        result = split_nodes_images([node])
        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode("one", TextType.IMAGE, "url1.com"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "url2.com"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    
    def test_split_nodes_images_no_images(self):
        node = TextNode("This is just text", TextType.TEXT)
        result = split_nodes_images([node])
        self.assertEqual(result, [node])
    
    def test_split_nodes_links_single(self):
        node = TextNode("Go to [site](https://site.com)", TextType.TEXT)
        result = split_nodes_links([node])
        expected = [
            TextNode("Go to ", TextType.TEXT),
            TextNode("site", TextType.LINK, "https://site.com"),
        ]
        self.assertEqual(result, expected)
    
    def test_split_nodes_links_multiple(self):
        node = TextNode("Visit [one](1.com) and [two](2.com) now!", TextType.TEXT)
        result = split_nodes_links([node])
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("one", TextType.LINK, "1.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.LINK, "2.com"),
            TextNode(" now!", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    
    def test_split_nodes_links_no_links(self):
        node = TextNode("This text has no links.", TextType.TEXT)
        result = split_nodes_links([node])
        self.assertEqual(result, [node])
    
    def test_preserves_non_text_nodes(self):
        image_node = TextNode("alt", TextType.IMAGE, "url.com")
        result_img = split_nodes_images([image_node])
        result_link = split_nodes_links([image_node])
        self.assertEqual(result_img, [image_node])
        self.assertEqual(result_link, [image_node])

if __name__ == "__main__":
    unittest.main()