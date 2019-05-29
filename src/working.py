from image_generator.node_generator import NodeGenerator
from image_generator.page import Page

gen = NodeGenerator(182, 160)
gen.add_goal_message(175, 'hello there, how is it going?')
node_list = gen.get_node_list()


page = Page()
page.create_nodes(node_list)
page.write_to_file('page_3.png')
