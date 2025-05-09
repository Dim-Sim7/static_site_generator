import textwrap
import re
from enum import Enum

from split_delimiter import text_to_textnodes
from htmlnode import HTMLNode, ParentNode, LeafNode, text_node_to_html
from textnode import TextNode, TextType

def markdown_to_blocks(markdown: str):
    
    cleaned = textwrap.dedent(markdown).strip()
    new_blocks = []
    
    raw_blocks = re.split(r'\ns*\n', cleaned)

    new_blocks = [block.strip() for block in raw_blocks if block.strip() != ""]
    #print(new_blocks)
    return new_blocks
   
    
    
    
class BlockType(Enum):

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    

def block_to_block_type(text: str) -> BlockType:
    
    blocks = {
        "# ": BlockType.HEADING,
        "```": BlockType.CODE,
        ">": BlockType.QUOTE,
        "- ": BlockType.UNORDERED_LIST,
        "%d. ": BlockType.ORDERED_LIST
        
        }
    if not text:
        raise ValueError("No block was entered")
        
    lines = text.splitlines() #stores each line in lines

            
    if text[0].startswith("#"):
        
        prefix = text.split(" ")[0] #split at each space, [0] is the #

        if 1 <= len(prefix) <= 6 and prefix == "#" * len(prefix) and text[len(prefix)] == " ": #if the number of # is less than or equal to 6, and if all prefix is # and if space after the # is " "
  
            return blocks["# "]
            
    if text.endswith("```") and text.startswith("```"):
        return blocks["```"]
    
    if all(line.startswith(">") for line in lines):
        return blocks[">"]
    
    if all(line.startswith("- ") for line in lines):
        return blocks["- "]
    
    counter = 0
    for line in lines:
        
        
        if "." not in line:
            return BlockType.PARAGRAPH
        
        prefix = line.split(".", 1)[0]
        if not prefix.isdigit():
            return BlockType.PARAGRAPH
        
        number = int(prefix)
        if number != counter + 1 or not line.startswith(f"{number}. "):
            return BlockType.PARAGRAPH
        
        counter += 1
        
        if counter == len(lines) - 1:
            return blocks["%d. "]
    
    return BlockType.PARAGRAPH










def block_to_parent_node(block_type, block):

    lines = block.splitlines()
    #print("THIS IS A SINGLE BLOCK",block)
    
    if block_type == BlockType.UNORDERED_LIST: #handle unordered list
        
        li_nodes = []
        for line in lines:
       
            
            content = line[2:] # Strip - (value is - Disney _didn't ruin it_ (okay, but Amazon might have))

            text_nodes = text_to_textnodes(content) #make list of text nodes [TextNode(Why Glorfindel is More Impressive than Legolas, link, /blog/glorfindel)]
            
            leaf_nodes = [text_node_to_html(text_node) for text_node in text_nodes] #make leaf node for each text node [HTMLNode(tag='a', value='Why Glorfindel is More Impressive than Legolas', children=[], props={'href': '/blog/glorfindel'})]
            #print("LEADNODE: ", leaf_nodes) 
            
            #wWrap inline nodes in a <li> parent
            li_node = ParentNode(tag="li", children=leaf_nodes)
            li_nodes.append(li_node)
            
        #print(li_nodes)
        return ParentNode(tag="ul", children=li_nodes)            
    
        
        
    if block_type == BlockType.ORDERED_LIST:
        
        counter = 1
        li_nodes = []
        
        for line in lines:
            
            content = line[len(f"{counter}. "):]
            #print(line)
          
            text_nodes = text_to_textnodes(content)
            #print(text_nodes)
            leaf_nodes = [text_node_to_html(text_node) for text_node in text_nodes]
            #print(leaf_nodes)
            counter += 1
            #Wrap inline nodes in <li>
            li_node = ParentNode(tag="li", children=leaf_nodes)
            li_nodes.append(li_node)
        
        return ParentNode(tag="ol", children=li_nodes)
    
    if block_type == BlockType.CODE:
        
        lines = block.splitlines()
        content_lines = lines[1:-1]  # remove ``` markers
        # Remove leading/trailing whitespace from each line
        stripped_lines = [line.strip() for line in content_lines]
        content = "\n".join(stripped_lines)
        if not content.endswith("\n"):
            content += "\n"
        raw_text_node = TextNode(content, TextType.TEXT)
        child = text_node_to_html(raw_text_node)
        code = ParentNode("code", [child])
        return ParentNode("pre", [code])
        
    
    if block_type == BlockType.HEADING:
        

        for line in lines: #go through each heading line
            prefix = line.split(" ")[0] # gets number of # on current line
            h_number = len(prefix) #set the h#
            h_tag = f"h{h_number}"
            
            content = line.strip(f"{prefix}").strip() #strip off the #
            
            in_line_nodes = text_to_textnodes(content.replace("\n", " ")) #list of text nodes
            html_nodes = [text_node_to_html(text_node) for text_node in in_line_nodes]

            heading_node = ParentNode(tag=h_tag, children=html_nodes) #make leafnode of current line

        return heading_node
    
    
    if block_type == BlockType.PARAGRAPH:
        

        paragraph_text = " ".join(lines)

        in_line_nodes = text_to_textnodes(paragraph_text) #list of text nodes

        html_nodes = [text_node_to_html(text_node) for text_node in in_line_nodes]
            

        return ParentNode(tag="p", children=html_nodes)




def markdown_to_html_node(markdown):
    
    new_blocks = markdown_to_blocks(markdown)#get list of blocks
    #print(new_blocks)
    parents = []

    for block in new_blocks: #iterate each block
        #rint(block)
        block_type = block_to_block_type(block) #'T
        #print(block_type)
        parent_node = block_to_parent_node(block_type, block) #create parents with children
        if parent_node is not None:
            parents.append(parent_node)
        #print(parents)
    div = ParentNode("div", children=parents)#make div node
    
    return div
    

