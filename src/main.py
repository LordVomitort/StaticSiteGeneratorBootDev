from textnode import TextNode, TextType
from html_builder import generate_page

from pathlib import Path
import os
import shutil

def copy_static_to_public(dir: str, final: str):
    if final == "public":
        print(f"Cleaning {final} directory")
        shutil.rmtree(final, True)
    if not os.path.exists(dir):
        raise Exception("directory doesn't exists")
    if not os.path.exists(final):
        print(f"Making dir: {final}")
        os.mkdir(final)

    dir_list = os.listdir(dir)
    for dr in dir_list:
        dir_line = os.path.join(dir, dr)
        final_line = os.path.join(final,dr)
        if os.path.isdir(dir_line):
            print(f"Accesing dir {dir_line}")
            copy_static_to_public(dir_line, final_line)
        else:
            print(f"Copying file: {dir_line} to {final_line}")
            shutil.copy(dir_line, final_line)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    if not os.path.exists(dir_path_content):
        raise Exception("Content path doesn't exists")
    list_dir = os.listdir(dir_path_content)

    for d in list_dir:
        dir_line = os.path.join(dir_path_content, d)
        final_line = os.path.join(dest_dir_path, d)
        if os.path.isdir(dir_line):
            generate_pages_recursive(dir_line, template_path, final_line)
        else:
            f = Path(dir_line)
            if f.suffix == ".md":
                file_name = f"{f.stem}.html"
                dest = Path(final_line)
                dest = Path(dest.parent)
                dest = dest / file_name
                
                generate_page(dir_line, template_path, dest)

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)

    copy_static_to_public("static", "public")
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")


main()