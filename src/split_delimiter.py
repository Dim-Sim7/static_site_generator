

from textnode import TextNode, TextType
import re
from extract_links import extract_markdown_images, extract_markdown_links

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

def split_nodes_images(old_nodes):
    
    new_nodes = []
    
    
    for node in old_nodes:
        
        if node.text_type is not TextType.TEXT: #if node is not TEXT, add it as is
            new_nodes.append(TextNode(node.text, node.text_type))
            continue
        
        if not node.text:
            continue
        
        
        extract = extract_markdown_images(node.text) #Extract out all alt text and urls
        remaining_text = node.text
        last_end = 0
        
        for alt_text, url in extract:
            
            pattern = rf"!\[{re.escape(alt_text)}\]\({re.escape(url)}\)" #escape alt text and url
            match = re.search(pattern, remaining_text) #match all alt text and url text
            start, end = match.span() #start and end of the escaped alt text and url (indexes)
            
            if start > 0: #if there is text before
            
                before = remaining_text[last_end:start] #before is the text at 0 and ends at the start of the escaped alt text
                print("BEFOR E", before)

                new_nodes.append(TextNode(before, TextType.TEXT)) #add text
        
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url)) #add image
            
            #remaining_text = remaining_text[end:] #change remaining text to the end of the url
            
            print("Start", start)
            print("End", end)
            print("Last End", last_end)
            last_end = end
            
    if last_end < len(remaining_text):
        new_nodes.append(TextNode(remaining_text, TextType.TEXT)) #add any ending text
        
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
    
node = [TextNode(
    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
    TextType.TEXT,
)]
new = split_nodes_images(node)
print(new)
    
    
    
    
    
    
    
    
    
    