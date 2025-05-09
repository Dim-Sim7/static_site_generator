import unittest

from blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

import textwrap


class Test_Blocks(unittest.TestCase):
    
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph
    
    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line
    
    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_basic_paragraphs(self):
        md = "Paragraph one.\n\nParagraph two."
        self.assertEqual(
            markdown_to_blocks(md),
            ["Paragraph one.", "Paragraph two."]
        )

    def test_multiple_blank_lines(self):
        md = "First paragraph.\n\n\n\nSecond paragraph."
        self.assertEqual(
            markdown_to_blocks(md),
            ["First paragraph.", "Second paragraph."]
        )

    def test_whitespace_on_blank_lines(self):
        md = "First.\n \n\t\nSecond."
        self.assertEqual(
            markdown_to_blocks(md),
            ["First.", "Second."]
        )

    def test_leading_and_trailing_whitespace(self):
        md = "\n\n  Hello world.  \n\n\n Bye world. \n\n"
        self.assertEqual(
            markdown_to_blocks(md),
            ["Hello world.", "Bye world."]
        )

    def test_single_block(self):
        md = "Just one paragraph, no blank lines."
        self.assertEqual(
            markdown_to_blocks(md),
            ["Just one paragraph, no blank lines."]
        )

    def test_list_block(self):
        md = "- item one\n- item two\n\nNew paragraph"
        self.assertEqual(
            markdown_to_blocks(md),
            ["- item one\n- item two", "New paragraph"]
        )

    def test_multiline_paragraph(self):
        md = "Line one\nLine two\n\nNext block"
        self.assertEqual(
            markdown_to_blocks(md),
            ["Line one\nLine two", "Next block"]
        )
        
    # Headings
    def test_block_to_block_heading1(self):
        block = "# Heading level 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_heading2(self):
        block = "###### Heading level 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    # Code blocks
    def test_block_to_block_code1(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_code2(self):
        block = "```python\nx = 5\nprint(x)\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    # Quote blocks
    def test_block_to_block_quote1(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_quote2(self):
        block = "> Line 1\n> Line 2\n> Line 3"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    # Unordered lists
    def test_block_to_block_unlist1(self):
        block = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_unlist2(self):
        block = "- First\n- Second\n- Third"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    # Ordered lists
    def test_block_to_block_olist1(self):
        block = "1. First item\n2. Second item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_olist2(self):
        block = "1. Apple\n2. Banana\n3. Cherry"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    # Paragraph (default)
    def test_block_to_block_para1(self):
        block = "This is a paragraph of regular text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # None / Unrecognized
    def test_block_to_block_none1(self):
        block = "@@ This shouldn't match any known block"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
    
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here
    
    This is another paragraph with _italic_ text and `code` here
    
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )
    
    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """
    
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_orderedblock(self):
        md = """
        1. First Item
        2. Second Item
        3. Third Item
        """
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol>\n<li>First Item</li>\n<li>Second Item</li>\n<li>Third Item</li>\n</ol></div>"
            
            
        )
    
    def test_headings(self):
        md = """
        # Heading 1
        ## Heading 2
        ### Heading 3
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>")
    
    def test_unorderedblocks(self):
        md = """
        - Item one
        - Item two
        - Item three
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul>\n<li>Item one</li>\n<li>Item two</li>\n<li>Item three</li>\n</ul></div>"
            )
    def test_mixedblocks(self):
        md = """
        # Welcome to My Site

        This is a paragraph introducing the page.
        
        ## Features
        
        - Easy to use
        - Fast
        - Reliable
        
        ### Code Example
        
        ```
        def greet(name):
        return f'Hello, {name}!'
        ```
        
        Here’s another paragraph after the code block.
                
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.maxDiff = None
        self.assertEqual(
    html,
    "<div><h1>Welcome to My Site</h1><p>This is a paragraph introducing the page.</p><h2>Features</h2><ul>\n<li>Easy to use</li>\n<li>Fast</li>\n<li>Reliable</li>\n</ul><h3>Code Example</h3><pre><code>def greet(name):\nreturn f'Hello, {name}!'\n</code></pre><p>Here’s another paragraph after the code block.</p></div>"
)
        
        
        
if __name__ == "__main__":
    unittest.main()