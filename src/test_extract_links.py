import unittest
from extract_links import extract_markdown_images, extract_markdown_links



class Test_Extract_Links(unittest.TestCase):
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
        
        


if __name__ == "__main__":
    unittest.main()