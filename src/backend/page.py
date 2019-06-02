import os
from PIL import Image, ImageDraw, ImageFont


class Page(object):
    """Represents a page filled with nodes"""

    # Page global settings
    width_in_inches = 8.5
    height_in_inches = 11
    pixels_per_inch = 300
    margin_top_in_inches = 1
    margin_bottom_in_inches = 1
    margin_left_in_inches = 1
    margin_right_in_inches = 1
    max_nodes_per_row = 5
    max_rows_per_page = 7

    font_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'assets/fonts/roboto_medium.ttf'
    )
    node_font = ImageFont.truetype(font_path, 45)

    node_diameter_pixels = 300
    node_padding_pixels = 105
    node_outline_width = 6

    def __init__(self):
        """Logic for class instantiation"""
        self.canvas = None
        self.image = None
        self.set_image_object()
        self.set_canvas_object()
        self.add_logo()

    def write_to_file(self, outfile):
        """Writes the page to a file"""
        self.image.save(outfile, 'PDF')
    
    def add_next_node_arrow(self, current_node_bounding_box):
        """Adds a next node arrow to the node to the right"""
        node_x, node_y = self.get_center_of_bounding_box(current_node_bounding_box)
        line_y = node_y
        arrow_offset_in_pixels = 30
        arrow_length_in_pixels = 40
        line_x_start =  node_x + (self.node_diameter_pixels / 2) + arrow_offset_in_pixels
        line_x_end = line_x_start + arrow_length_in_pixels
        self.canvas.line(
            (line_x_start, line_y, line_x_end, line_y),
            fill=(211, 211, 211),
            width=self.node_outline_width
        )
        triangle_height_pixels = 10
        triangle_depth_pixels = 10
        self.canvas.polygon(
            [
                (line_x_end, line_y),
                (line_x_end - triangle_depth_pixels, line_y + triangle_height_pixels),
                (line_x_end - triangle_depth_pixels, line_y - triangle_height_pixels)
            ],
            fill=(211, 211, 211)
        )
    
    def add_next_node_arrow_new_row(self, current_node_bounding_box):
        """Adds an arrow to the next row of nodes"""
        pass
    
    def add_logo(self):
        """Adds the colour_my_change logo to each page"""
        logo_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'assets/images/branding_badge.png'
        )
        logo = Image.open(logo_path, 'r')
        offset = (
            int(self.width_in_inches * self.pixels_per_inch) - 780,
            int(self.height_in_inches * self.pixels_per_inch) - 240,
        )
        self.image.paste(logo, offset)

    def get_in_pixels(self, dimension_in_inches):
        """Converts dimension in inches to pixels"""
        return dimension_in_inches * self.pixels_per_inch
    
    def get_max_nodes_per_page(self):
        """REturns the maximum number of nodes per page"""
        return int(self.max_nodes_per_row * self.max_rows_per_page)

    def set_image_object(self):
        """Sets a new pillow image object"""
        image_height = int(self.height_in_inches * self.pixels_per_inch)
        image_width = int(self.width_in_inches * self.pixels_per_inch)
        image_size = image_width, image_height
        self.image = Image.new(
            mode='RGB',
            size=image_size,
            color=(255, 255, 255)
        )
    
    def get_image_object(self):
        """Returns the pillow image object for the class"""
        return self.image

    def set_canvas_object(self):
        """Sets the canvas object"""
        self.canvas = ImageDraw.Draw(self.image)

    def build_bounding_box(self, column_counter, row_counter):
        """Returns a dictionary with bounding box coordinates"""
        return {
            'x1': int(
                column_counter * self.node_diameter_pixels + \
                self.node_padding_pixels * column_counter + self.get_in_pixels(self.margin_left_in_inches)
            ),
            'y1': int(
                row_counter * self.node_diameter_pixels + \
                self.node_padding_pixels * row_counter + self.get_in_pixels(self.margin_top_in_inches)
            ),
            'x2': int(
                column_counter * self.node_diameter_pixels + \
                self.node_diameter_pixels + self.node_padding_pixels \
                * column_counter + self.get_in_pixels(self.margin_left_in_inches)
            ),
            'y2': int(
                row_counter * self.node_diameter_pixels + \
                self.node_diameter_pixels + self.node_padding_pixels \
                * row_counter + self.get_in_pixels(self.margin_top_in_inches)
            ),
        }
    
    def get_center_of_bounding_box(self, bounding_box):
        """Returns the absolute center of the bounding box"""
        x = int(bounding_box['x1'] + (self.node_diameter_pixels / 2))
        y = int(bounding_box['y1'] + (self.node_diameter_pixels / 2))
        return (x, y)

    def get_center_of_bounding_box_for_text(self, bounding_box, text):
        """Returns the center xy coordinates of the bounding box accounting for text"""
        text_size_width, text_size_height = self.canvas.textsize(text, font=self.node_font)
        x_remainder_padding = int((self.node_diameter_pixels - text_size_width) / 2)
        y_remainder_padding = int((self.node_diameter_pixels - text_size_height) / 2)
        x = int(bounding_box['x1'] + x_remainder_padding)
        y = int(bounding_box['y1'] + y_remainder_padding)
        return (x, y)

    def create_nodes(self, node_array):
        """Dynamically creates nodes from the node array"""
        row_counter = 0
        column_counter = 0
        node_array_length = len(node_array)
        for index, node in enumerate(node_array):
            if row_counter is self.max_rows_per_page:
                continue
            node_width = self.node_outline_width
            if 'message' in node:
                node_width = node_width * 2
            bound_box = self.build_bounding_box(column_counter, row_counter)
            # Add node basics
            self.canvas.ellipse(
                (bound_box['x1'], bound_box['y1'], bound_box['x2'], bound_box['y2']),
                outline=(211, 211, 211),
                width=node_width
            )
            self.canvas.text(
                self.get_center_of_bounding_box_for_text(bound_box, node['text']),
                node['text'],
                font=self.node_font,
                fill=(100, 100, 100)
            )

            # Add Arrows
            if column_counter is not (self.max_nodes_per_row - 1):
                if index is not (node_array_length - 1):  # not the last node ever
                    self.add_next_node_arrow(bound_box)

            # Increment Logic
            column_counter += 1
            if column_counter is self.max_nodes_per_row:
                row_counter += 1
                column_counter = 0

