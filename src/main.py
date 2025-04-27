#./main.sh
# hello world
from textnode import TextNode
from textnode import TextType

def main():
    
    dummy = TextNode("qwdwadqwq", TextType.LINK, "www.google.com")
    
    print(dummy)
    
    
main()