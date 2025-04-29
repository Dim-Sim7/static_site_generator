
from textnode import TextNode, TextType

class HTMLNode():
    def __init__(self, tag=None, value='', children=None, props=None):
        
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
        
    
    def to_html(self):
        
        raise NotImplementedError
    
    def props_to_html(self):
        
        if not self.props:
            return ''
        html_string = ''
        for k,v in self.props.items():
            
            
            html_string += f' {k}="{v}"'
        return html_string
            
    def __repr__(self):
        
        return (f"HTMLNode(tag='{self.tag}', value='{self.value}', "
                f"children={self.children}, props={self.props})")

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None): #doesnt allow for children || value and tag is required
        super().__init__(tag=tag, value=value, children = [], props=props)
                
        
    
    def to_html(self):
        if self.value == '':
            raise ValueError("All leaf nodes must have a value")
        
        if self.tag is None:
            
            return rf"<>{self.value}.</>"
        
        return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
        
    
    
    def to_html(self):
        
        if not self.tag:
            raise ValueError("tag is missing")
        
        if not self.children:
            raise ValueError("children are missing")
        
        for c in self.children:
            return f"<{self.tag}>{c.to_html()}</{self.tag}>"
            

def text_node_to_html(node):
    
    if node.text_type == TextType.TEXT:
        return LeafNode(tag=None,value=node.text)
        
    elif node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=node.text)
        
    elif node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=node.text)
        
    elif node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=node.text)
        
    elif node.text_type == TextType.LINK:
        return LeafNode(tag="a",value=node.text, props=f"href:{node.url}")
    
    elif node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value='', props=f"src:{node.url}, alt:{node.text}")
    
    else:
        raise ValueError(f"Unknown TextType: {node.text_type}")
        
    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            