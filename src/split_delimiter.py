

from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    new_nodes = []
    
    delimiters = { #dict of delimiters with corresponsing tuples of node type and regex
        "**": (TextType.BOLD, r'^(.*?)\*\*(.*?)\*\*(.*)$'),
        "_": (TextType.ITALIC, r'^(.*?)\_(.*?)\_(.*)$'),
        "`": (TextType.CODE, r'^(.*?)\`(.*?)\`(.*)$')
    }
    
    if delimiter not in delimiters:
        
        raise ValueError("Invalid Delimiter")
    
    node_type, regex = delimiters[delimiter] #initialise node_type and regex with corrresponding delimiter
    


    for node in old_nodes:
        
        if node.text_type is not TextType.TEXT: #if node is not TEXT, add it as is
            new_nodes.append(TextNode(node.text, node.text_type))
            return new_nodes
            continue
        
        match = re.match(regex, node.text)
        
        if not match:
            raise ValueError("Regex detection issue, not correct format")
        
        before, between, after = match.groups() 
        
        
            
        if not between: #if between doesnt exist
            raise ValueError("invalid Markdown syntax")
        
        if before:
            new_nodes.append(TextNode(before, TextType.TEXT))
        
        new_nodes.append(TextNode(between, node_type))
        
        if after:
            new_nodes.append(TextNode(after, TextType.TEXT))
            
    return new_nodes