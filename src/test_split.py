# -*- coding: utf-8 -*-
"""
Created on Fri May  9 23:57:36 2025

@author: warlo
"""
import unittest
from split_delimiter import split_nodes_delimiter, split_nodes_images, split_nodes_links
from textnode import TextNode, TextType
class TestSplitNodesImages(unittest.TestCase):


    def test_split_nodes_images_no_images(self):
        old_nodes = [
            TextNode("This is just text.", TextType.TEXT),
            TextNode("Another text node.", TextType.TEXT)
        ]
        new_nodes = split_nodes_images(old_nodes)

        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is just text.")
        self.assertEqual(new_nodes[1].text, "Another text node.")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)


    def test_split_nodes_images_with_image(self):
        old_nodes = [
            TextNode("Some text ![alt text](http://example.com/image.png) more text.", TextType.TEXT)
        ]
        new_nodes = split_nodes_images(old_nodes)

        # Check if image is extracted and the text is split correctly
        self.assertEqual(len(new_nodes), 3)  # TextNode for before image, image node, and text after image
        self.assertEqual(new_nodes[0].text, "Some text ")
        self.assertEqual(new_nodes[1].text, "alt text")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "http://example.com/image.png")
        self.assertEqual(new_nodes[2].text, " more text.")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)


    def test_split_nodes_images_edge_case(self):
        old_nodes = [
            TextNode("![]() Some text after image.", TextType.TEXT)
        ]
        new_nodes = split_nodes_images(old_nodes)

        # Check if empty image alt text is handled correctly
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "")
        self.assertEqual(new_nodes[0].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].text, " Some text after image.")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)

if __name__ == '__main__':
    unittest.main()