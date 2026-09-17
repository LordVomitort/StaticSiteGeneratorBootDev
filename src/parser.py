from textnode import TextNode, TextType
import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UN_LIST = "unordered_list"
    OR_LIST = "ordered_list"


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    exit_list = []
    for old in old_nodes:
        if old.text_type != TextType.TEXT:
            exit_list.append(old)
            continue
        split_nodes = []
        splited = old.text.split(delimiter)
        if len(splited) % 2 == 0:
            raise Exception("No matching delimiters")
        for i in range(len(splited)):
            if splited[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(splited[i],TextType.TEXT))
            else:
                split_nodes.append(TextNode(splited[i],text_type))
        
        exit_list.extend(split_nodes)

    return exit_list

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    exit_list = []
    for old in old_nodes:
        if old.text_type != TextType.TEXT:
            exit_list.append(old)
            continue
        extracts = extract_markdown_images(old.text)
        if not extracts:
            exit_list.append(old)
            continue
        text= old.text
        splited = []
        for ex in extracts:
            image_alt, image_link = ex
            
            splited = text.split(f"![{image_alt}]({image_link})",1)
            text = splited[1]
            exit_list.extend([TextNode(splited[0],TextType.TEXT), TextNode(image_alt, TextType.IMAGE, image_link)])

        if len(splited) > 1:
            if splited[1] != "":
                exit_list.extend([TextNode(splited[1],TextType.TEXT)])
    
    return exit_list

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    exit_list = []
    for old in old_nodes:
        if old.text_type != TextType.TEXT:
            exit_list.append(old)
            continue
        extracts = extract_markdown_links(old.text)
        if not extracts:
            exit_list.append(old)
            continue
        text= old.text
        splited = []
        for ex in extracts:
            link_alt, link_link = ex
            
            splited = text.split(f"[{link_alt}]({link_link})",1)
            text = splited[1]
            
            exit_list.extend([TextNode(splited[0],TextType.TEXT), TextNode(link_alt, TextType.LINK, link_link)])

        if len(splited) > 1:
            if splited[1] != "":
                exit_list.extend([TextNode(splited[1],TextType.TEXT)])
    
    return exit_list


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text,TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda b: b.strip(), blocks))
    def white_space_helper(block: str):
        if block!= "":
            return True
        return False
    blocks = list(filter(white_space_helper, blocks))
    return blocks

def block_to_block_type(block: str) -> BlockType:
    lineas = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if len(lineas) > 1 and lineas[0].startswith("```") and lineas[-1].startswith("```"):
        return BlockType.CODE
    result = False

    if block.startswith(">"):
        for l in lineas:
            if not l.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("-"):
        for l in lineas:
            if not l.startswith("-"):
                return BlockType.PARAGRAPH
        return BlockType.UN_LIST

    if block.startswith("1. "):
        i = 1
        for l in lineas:
            if not l.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OR_LIST

    return BlockType.PARAGRAPH

def remove_heading_tag(text: str) -> str:
    matches = re.findall(r"#+ *(.*)",text)
    
    return matches[0]

def extract_title(markdown: str):
    blocks = markdown_to_blocks(markdown)
    head = ""
    for b in blocks:
        if b.startswith("#"):
            head = b
            break
    if head == "":
        raise Exception("No title found")
    return remove_heading_tag(head)
    