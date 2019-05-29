"""Helper methods for generating pages"""
import io

from backend.node_generator import NodeGenerator
from backend.page import Page
from PIL import Image


def split_node_list_into_pages(node_list, max_nodes_per_page):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(node_list), max_nodes_per_page):
        yield node_list[i:i + max_nodes_per_page]


def build_pdf_output(node_list):
    """Renders a multipage output from a node list"""
    dummy_page = Page()
    max_nodes_per_page = dummy_page.get_max_nodes_per_page()
    rendered_pages = []
    for page_node_list in split_node_list_into_pages(node_list, max_nodes_per_page):
        page = Page()
        page.create_nodes(page_node_list)
        rendered_pages.append(page.get_image_object())
        del page
    output_file = io.BytesIO()
    rendered_pages[0].save(output_file, 'PDF', save_all=True, append_images=rendered_pages[1:])
    output_file.seek(0)
    return output_file
