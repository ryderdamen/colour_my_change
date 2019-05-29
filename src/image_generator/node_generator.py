"""Module for storing the NodeGenerator class, responsible for generating the node_list syntax"""


class NodeGenerator(object):
    """Generates a node array"""

    node_list = []

    def __init__(self, starting_weight, ending_weight):
        """Instantiation logic for the class"""
        if starting_weight > ending_weight:
            low = ending_weight
            high = starting_weight
        else:
            low = starting_weight
            high = ending_weight
        for weight in range(low, high + 1):
            self.node_list.append({
                'text': str(weight), 
            })
        if starting_weight > ending_weight:
            self.node_list = list(reversed(self.node_list))
    
    def add_goal_message(self, weight, message):
        """Adds a goal message to a particular weight"""
        for index, node in enumerate(self.node_list):
            if node['text'] == str(weight):
                self.node_list[index]['message'] = str(message)

    def get_node_list(self):
        """Gets the node_list"""
        return self.node_list
