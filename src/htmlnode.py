
from textnode import TextNode, TextType
import html

class HTMLNode():
    def __init__(self, tag=None, value='', children=None, props=None):
        
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
        
    
    def to_html(self):
        
        pass
            
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

        super().__init__(tag=tag, value=value, children = None, props= props)
                
        
    
    def to_html(self):
        #if self.value == '':
            #raise ValueError("All leaf nodes must have a value")
        
        if self.tag is None:
            
            return self.value
        
        
        props_str = ""
        if self.props:
            props_str = " " + " ".join(f'{key}="{html.escape(value)}"' for key, value in self.props.items())

        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
        
        
    def to_html(self):
        if self.tag is None and not self.children:
            return self.value  # plain text node
        
        if self.tag is None:
            return "".join(child.to_html() for child in self.children)

        # Build attributes string
        props_str = ""
        if self.props:
            props_str = " " + " ".join(f'{key}="{html.escape(value)}"' for key, value in self.props.items())

        # Handle leaf node with value
        if self.value and not self.children:
            return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
        if self.tag == "code" and "\n" in self.value:
            return f"<pre><code>{self.value}</code></pre>\n"
        


        inner_html = "".join(child.to_html() for child in self.children)
        if self.tag == "li":
            return f"<{self.tag}{props_str}>{inner_html}</{self.tag}>\n"
        if self.tag == "ol" or self.tag == "ul":
            return f"<{self.tag}{props_str}>\n{inner_html}</{self.tag}>"
        return f"<{self.tag}{props_str}>{inner_html}</{self.tag}>"

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
        return LeafNode(tag="a",value=node.text, props={"href":html.escape(node.url)})
    
    elif node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value='', props={"src":html.escape(node.url), "alt":node.text})
    
    else:
        raise ValueError(f"Unknown TextType: {node.text_type}")
        
    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            