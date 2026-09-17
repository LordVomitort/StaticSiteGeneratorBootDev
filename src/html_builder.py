import re
import os
from parser import markdown_to_blocks, block_to_block_type, BlockType, text_to_textnodes, extract_title
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node

def text_to_children(block: str) -> list[HTMLNode]:
    text_nodos = text_to_textnodes(block)
    leaf_nodos = []
    for n in text_nodos:
        leaf_nodos.append(text_node_to_html_node(n))
    
    return leaf_nodos

def get_headind_tag(block: str) -> str:
    finds = re.findall(r"^(#+)", block)
    return f"h{len(finds[0])}"

def remove_heading_tag(text: str) -> str:
    matches = re.findall(r"#+ *(.*)",text)
    
    return matches[0]

def remove_quote_tag(text: str) -> str:
    matches = re.findall(r"> *(.*)",text)
    return matches[0]

def remove_unorder_list_tag(text: str) -> str:
    matches = re.findall(r"- *(.*)",text)
    return matches[0]

def build_unordered_list(text: str) -> list[ParentNode]:
    lineas = text.split("\n")
    
    un_nodos =[]
    for l in lineas:
        texto_limpio = re.findall(r"- *(.*)",l)[0]
        un_nodos.append(ParentNode("li",text_to_children(texto_limpio)))    

    return un_nodos

def build_ordered_list(text: str) -> list[ParentNode]:
    linas = text.split("\n")

    or_nodos =[]
    for l in linas:
        texto_limpio = re.findall(r"[\d+]\. *(.*)", l)[0]
        or_nodos.append(ParentNode("li", text_to_children(texto_limpio)))

    return or_nodos

def remove_code_tag(text: str) -> LeafNode:
    text=text[4:-3]
    return LeafNode(None,text)

def markdown_to_html_node(markdown: str):

    # nodo = ParentNode("div")
    bloques = markdown_to_blocks(markdown)

    nodos = []
    for b in bloques:
        tipo = block_to_block_type(b)

        match tipo:
            case BlockType.PARAGRAPH:
                b = b.split("\n")
                b = " ".join(b)
                nodos.append(ParentNode("p",text_to_children(b)))

            case BlockType.HEADING:
                linea = remove_heading_tag(b)
                nodos.append(ParentNode(get_headind_tag(b),text_to_children(linea)))

            case BlockType.QUOTE:
                linea = remove_quote_tag(b)
                nodos.append(ParentNode("blockquote", text_to_children(linea)))

            case BlockType.UN_LIST:
                
                nodos.append(ParentNode("ul", build_unordered_list(b)))

            case BlockType.OR_LIST:

                nodos.append(ParentNode("ol", build_ordered_list(b)))

            case BlockType.CODE:

                nodos.append(ParentNode("pre",[ParentNode("code", [remove_code_tag(b)])]))


    return ParentNode("div",nodos)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as md_file:
        md_content = md_file.read()
    with open(template_path) as t_file:
        template_content = t_file.read()

    html_string = markdown_to_html_node(md_content).to_html()

    titulo = extract_title(md_content)

    template_content = template_content.replace("{{ Title }}", titulo)

    template_content = template_content.replace("{{ Content }}", html_string)

    pre_path = os.path.dirname(dest_path)
    try:
        os.makedirs(pre_path)
    except:
        pass

    with open(dest_path,"w") as destino:
        destino.write(template_content)
