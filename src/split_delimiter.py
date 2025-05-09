

from textnode import TextNode, TextType
import re
from extract_links import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter):
    
    new_nodes = []
    
    delimiters = { #dict of delimiters with corresponsing tuples of node type and regex
        "**": (TextType.BOLD, r"(.*?)\*\*(.+?)\*\*(.*)"),
        "_": (TextType.ITALIC, r"(.*?)_(.+?)_(.*)"),
        "`": (TextType.CODE, r"(.*?)`(.+?)`(.*)")
    }
    
    if delimiter not in delimiters:
        
        raise ValueError("Invalid Delimiter")
    
    node_type, regex = delimiters[delimiter] #initialise node_type and regex with corrresponding delimiter
    
    

    for node in old_nodes:
        
        if node.text_type is not TextType.TEXT: #if node is not TEXT, add it as is
            new_nodes.append(node)
            continue
        

        text = node.text
        pattern = re.compile(regex)


        while True:
            match = pattern.search(text)
            if not match:
                new_nodes.append(TextNode(text, TextType.TEXT))
                break
        
            before, between, after = match.groups()
        
            
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
                
            new_nodes.append(TextNode(between, node_type)) 
            
            if after == text:
                break
            text = after

            
    return new_nodes



def split_nodes_images(old_nodes):
    
    new_nodes = []
    
    
    for node in old_nodes:
        
        if node.text_type is not TextType.TEXT: #if node is not TEXT, add it as is
            new_nodes.append(node)
            continue
        
        
        extract = extract_markdown_images(node.text) #Extract out all alt text and urls
        remaining_text = node.text
        last_end = 0
        

        for alt_text, url in extract:
            

            pattern = re.compile(rf"!\[{re.escape(alt_text)}\]\({re.escape(url)}\)") #regex to escape alt text and url
            match = pattern.search(remaining_text[last_end:]) #match all alt text and url text

            if not match:
                continue
            

            start, end = match.span()
            # Adjust start/end to the full string
            start += last_end
            end += last_end
            
            if start > last_end:
                before = remaining_text[last_end:start]
                new_nodes.append(TextNode(before, TextType.TEXT))
        
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url)) #add image
            last_end = end
            
        if last_end < len(remaining_text): #this section handles any left over text after the last url
            remaining_text = remaining_text[last_end:]
            new_nodes.append(TextNode(remaining_text, TextType.TEXT)) 
        
    return new_nodes


def split_nodes_links(old_nodes):
    
    new_nodes = []
    
    
    for node in old_nodes:
        
        if node.text_type is not TextType.TEXT: #if node is not TEXT, add it as is
            new_nodes.append(node)
            continue
        
        
        extract = extract_markdown_links(node.text) #Extract out all alt text and urls
        remaining_text = node.text
        last_end = 0
        

        for anchor_text, url in extract:
            
            pattern = re.compile(rf"\[{re.escape(anchor_text)}\]\({re.escape(url)}\)") #regex to escape alt text and url
            match = pattern.search(remaining_text[last_end:]) #match all alt text and url text

            if not match:
                continue
            

            start, end = match.span()
            # Adjust start/end to the full string
            start += last_end
            end += last_end
            
            if start > last_end:
                before = remaining_text[last_end:start]
                new_nodes.append(TextNode(before, TextType.TEXT))
        
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url)) #add image
            last_end = end
            
        if last_end < len(remaining_text): #this section handles any left over text after the last url
            remaining_text = remaining_text[last_end:]
            new_nodes.append(TextNode(remaining_text, TextType.TEXT)) 
        
    return new_nodes
    
'''
input old node list
iterate through list
store node.text in new variable
extract alttext and url from other function
match those two with the node.text
using span() I can see the index of where the alt text and url starts and ends
in new variable, store all string before the alt_text
store new textnode object in new_nodes
store new textnode image object in new nodes
change remaining text to the text that is after the url
repeat for the second instance of the alt text and url
''' 

#This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)

    
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**")
    nodes = split_nodes_delimiter(nodes, "_")
    nodes = split_nodes_delimiter(nodes, "`")
    
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes


    
    
    