#./main.sh
# hello world
from os import listdir, path
import os
import shutil
from blocks import markdown_to_html_node

import sys

def main():
    
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    

    get_contents()
    
    content_dir = "content"
    template_path = "template.html"
    dest_dir = "docs"
    
    generate_pages_recursive(content_dir, template_path, dest_dir, basepath)




    
def get_contents():
    
    src = os.path.join(os.getcwd(), "static")
    dst = os.path.join(os.getcwd(), "docs")
    contents = []
    
    if os.path.exists(dst):
        shutil.rmtree(dst) #delete public
    os.mkdir(dst) #make public
    if path.exists(src): # if src exist
        contents = listdir(src) # returns list
    
    
    
    if os.path.exists(src):
        
        get_items(src, dst, contents)
    
    else:
        raise ValueError("No source path exists")
    

def get_items(src, dst, contents):
    
    for item in contents:
        
        src_path = path.join(src, item)
        dst_path = path.join(dst, item)
        
        if os.path.isfile(src_path):
            
            shutil.copy2(src_path, dst_path)
            #print(f"Copied {src_path} to {dst_path}")
            
        if os.path.isdir(src_path): #if path is a directory, copy the contents of the directory again and do mdkir
            
            contents = listdir(src_path) # new src and dst = src/item and dst/item (which are directories)
            os.mkdir(dst_path)
            get_items(src_path, dst_path, contents) #recursively call get_items
    

def extract_title(markdown):
    
    lines = markdown.split("\n")
    
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()


def generate_page(from_path, template_path, dest_path, basepath):
    
    #print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    
    markdown = read_file(from_path)
    html_template = read_file(template_path)

    new_html = markdown_to_html_node(markdown)
    
    title = extract_title(markdown)
    #print("TITLE", title)
    
    
    final_html = html_template.replace("{{ Content }}", new_html.to_html())
    final_html = final_html.replace("{{ Title }}", title)
    
    final_html = final_html.replace('href="/', f"href={basepath}")
    final_html = final_html.replace('src="/', f"href={basepath}")

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    dest_path = os.path.splitext(dest_path)[0] + ".html"
    
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)
    
    
def read_file(file_path):
    
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print(f"Error: File not found at '{file_path}'")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    
    contents = listdir(dir_path_content)

    for content in contents:
        
        src_path = path.join(dir_path_content, content).replace("\\", "/")
        dst_path = path.join(dest_dir_path, content).replace("\\", "/")
        #print(src_path)
        if os.path.isfile(src_path):
           # file_stem = os.path.splitext(content)[0]
          # dst_folder = os.path.join(dest_dir_path, file_stem)
            print(dst_path)
            generate_page(src_path, template_path, dst_path, basepath)
        
        elif os.path.isdir(src_path):
            new_dst_dir = path.join(dest_dir_path, content).replace("\\", "/")
            os.makedirs(new_dst_dir, exist_ok=True)
            generate_pages_recursive(src_path, template_path, dst_path, basepath)



main()    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    