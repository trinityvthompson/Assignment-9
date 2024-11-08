"""
# File: GraphFill.py

#  Description: Implements a graph traversal with color flood fill (BFS and DFS)
for nodes in an image graph based on adjacency and target color.

#  Student Name: Trinity Thompson

#  Student UT EID: tyt242

#  Partner Name: Marissa Shuchart

#  Partner UT EID: ms87339

#  Course Name: CS 313E

#  Unique Number: 50165

#  Date Created: 11.07.2024

#  Date Last Modified: 11.07.2024
"""

import os
import sys

# -----------------------PRINTING LOGIC, DON'T WORRY ABOUT THIS PART----------------------------

# this enables printing colors on Windows somehow
os.system("")

# code to reset the terminal color
RESET_CHAR = "\u001b[0m"
# color codes for the terminal
COLOR_DICT = {
    "black": "\u001b[30m",
    "red": "\u001b[31m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33m",
    "blue": "\u001b[34m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m"
}
# character code for a block
BLOCK_CHAR = "\u2588"

# Input: text is some string we want to write in a specific color
#   color is the name of a color that is looked up in COLOR_DICT
# Output: returns the string wrapped with the color code
def colored(text, color):
    """Returns input text wrapped in specified color"""
    color = color.strip().lower()
    if not color in COLOR_DICT:
        raise Exception(color + " is not a valid color!")
    return COLOR_DICT[color] + text

# Input: color is the name of a color that is looked up in COLOR_DICT
# prints a block (two characters) in the specified color
def print_block(color):
    """Prints a block of color (two characters wide)"""
    print(colored(BLOCK_CHAR, color)*2, end='')

# -----------------------PRINTING LOGIC, DON'T WORRY ABOUT THIS PART----------------------------



# Stack class; you can use this for your search algorithms
class Stack():
    """Stack implementation for depth-first search traversal"""
    def __init__(self):
        self.stack = []

    def push(self, item):
        """add an item to the top of the stack"""
        self.stack.append(item)

    def pop(self):
        """remove an item from the top of the stack"""
        return self.stack.pop()


    def peek(self):
        """check the item on the top of the stack"""
        return self.stack[-1]

    def is_empty(self):
        """check if the stack if empty"""
        return len(self.stack) == 0

    def size(self):
        """return the number of elements in the stack"""
        return len(self.stack)

# Queue class; you can use this for your search algorithms
class Queue():
    """Queue implementation for breadth-first search traversal"""
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        """add an item to the end of the queue"""
        self.queue.append(item)

    def dequeue(self):
        """remove an item from the beginning of the queue"""
        return self.queue.pop(0)

    def peek(self):
        """checks the item at the top of the Queue"""
        return self.queue[0]

    def is_empty(self):
        """check if the queue is empty"""
        return len(self.queue) == 0

    def size(self):
        """return the size of the queue"""
        return len(self.queue)

class ColorNode:
    """
    class for a graph node; contains x and y coordinates, a color, a list of edges and
    a flag signaling if the node has been visited (useful for serach algorithms)
    it also contains a "previous color" attribute.
    This might be useful for your flood fill implementation.
    """

    def __init__(self, index, x, y, color):
        """
        Input: x, y are the location of this pixel in the image
        color is the name of a color
        """
        self.index = index
        self.color = color
        self.prev_color = color
        self.x = x
        self.y = y
        self.edges = []
        self.visited = False

    def add_edge(self, node_index):
        """Input: node_index is the index of the node we want to create an edge to in the node list
        adds an edge and sorts the list of edges"""
        self.edges.append(node_index)

    def visit_and_set_color(self, color):
        """Input: color is the name of the color the node should be colored in;
        the function also saves the previous color, might be useful for your 
        flood fill implementation"""
        self.visited = True
        self.prev_color = self.color
        self.color = color

        print("Visited node " + str(self.index))

class ImageGraph:
    """Class that contains graph"""
    def __init__(self, image_size):
        self.nodes = []
        self.image_size = image_size

    def print_image(self):
        """Prints the image formed by the nodes on the command line"""
        img = [["black" for i in range(self.image_size)] for j in range(self.image_size)]

        # fill img array
        for node in self.nodes:
            img[node.y][node.x] = node.color

        for line in img:
            for pixel in line:
                print_block(pixel)
            print()
        # print new line/reset color
        print(RESET_CHAR)

    def reset_visited(self):
        """sets the visited flag to False for all nodes"""
        for _, node in enumerate(self.nodes):
            node.visited = False

    def print_adjacency_matrix(self):
        """Prints the adjacency matrix of the graph, showing connections between nodes."""
        print("Adjacency matrix:")

        # Create a matrix initialized with 0s
        matrix = [[0] * len(self.nodes) for _ in range(len(self.nodes))]

        # Fill in the matrix with edges
        for node in self.nodes:
            for edge in node.edges:
                matrix[node.index][edge] = 1
                matrix[edge][node.index] = 1  # Since it's undirected

        # Print the matrix
        for row in matrix:
            print("".join(map(str, row)))
        # empty line afterwards
        print()

    # implement your bfs algorithm here. Call print_image() after coloring a node
    # Input: graph is the graph containing the nodes
    #   start_index is the index of the currently visited node
    #   color is the color to fill the area containing the current node with
    def bfs(self, start_index, color):
        """Performs a breadth-first search (BFS) starting from given node index.
        It colors the connected nodes with the target color."""

        # print initial state
        print("Starting BFS; initial state:")
        self.print_image()

        # reset visited status
        self.reset_visited()
        target_color = self.nodes[start_index].color

        # intialize queue with the starting node's color and mark it as visited
        queue = Queue()
        queue.enqueue(start_index)
        self.nodes[start_index].visited = True
        self.nodes[start_index].visit_and_set_color(color) # set the start node's color

        # Print the image after coloring the starting node
        self.print_image()

        # countinue until all reachable nodes are processed
        while not queue.is_empty():
            # get the next node in the queue
            current_index = queue.dequeue()
            current_node = self.nodes[current_index]

            # check each neighbor of the current node
            for neighbor_index in current_node.edges:
                neighbor_node = self.nodes[neighbor_index]

                # Process unvisited neighbors only
                if not neighbor_node.visited and neighbor_node.color == target_color:
                    neighbor_node.visited = True # mark as visited
                    neighbor_node.visit_and_set_color(color) # set neighbor's color
                    queue.enqueue(neighbor_index) # add neighbor to queue for further exploration

                    # print image after each node is colored and processed
                    self.print_image()

    # implement your dfs algorithm here. Call print_image() after coloring a node
    # Input: graph is the graph containing the nodes
    #   start_index is the index of the currently visited node
    #   color is the color to fill the area containing the current node with
    def dfs(self, start_index, color):
        """Performs a depth-first search (DPS) starting from the given node index.
        It colors the connected nodes with the target color."""

        # print initial state
        print("Starting DFS; initial state:")
        self.print_image()

        # reset visited status for all nodes before starting DFS
        self.reset_visited()

        # Define the color of the starting node as the target color
        target_color = self.nodes[start_index].color

        # Initialize the stack and start with the given node (# Stack used for DFS due to LIFO nature)
        stack = Stack()
        stack.push(start_index)

        # Mark the following node as visited and change its color 
        self.nodes[start_index].visit_and_set_color(color)
        self.nodes[start_index].visited = True

        # Print the image after coloring the starting node
        self.print_image()

        # DFS traversal
        while not stack.is_empty():
            # Pop the current node from the stack 
            current = stack.pop()
            current_node = self.nodes[current]

            # If this node hasn't been visited and matches the target color
            if not current_node.visited and current_node.color == target_color:
                # Mark it as visited
                current_node.visited = True

                # Color the node with the new color
                current_node.visit_and_set_color(color)
                
                # Print image after coloring each node that macthes the target color
                self.print_image()
            
            # Push all unvisited neighbors to the stack if they match the target color
            for neighbor in current_node.edges:
                neighbor_node = self.nodes[neighbor]
                # Only push neighbors that have not been visited and match the target color
                if not neighbor_node.visited and neighbor_node.color == target_color:
                    stack.push(neighbor)
            

def create_graph(data):
    """creates graph from read in data"""
    data_list = data.split("\n")

    # get size of image, number of nodes
    image_size = int(data_list[0])
    node_count = int(data_list[1])

    graph = ImageGraph(image_size)

    index = 2

    # create nodes
    for _ in range(node_count):
        # node info has the format "x,y,color"
        node_info = data_list[index].split(",")
        new_node = ColorNode(len(graph.nodes), int(node_info[0]), int(node_info[1]), node_info[2])
        graph.nodes.append(new_node)
        index += 1

    # read edge count
    edge_count = int(data_list[index])
    index += 1

    # create edges between nodes
    for _ in range(edge_count):
        # edge info has the format "fromIndex,toIndex"
        edge_info = data_list[index].split(",")
        # connect node 1 to node 2 and the other way around
        graph.nodes[int(edge_info[0])].add_edge(int(edge_info[1]))
        graph.nodes[int(edge_info[1])].add_edge(int(edge_info[0]))
        index += 1

    # read search info
    search_info = data_list[index].split(",")
    search_start = int(search_info[0])
    search_color = search_info[1]

    return graph, search_start, search_color


def main():
    """Main function to read graph data, create graph, and perform search algorithms."""
    # read input
    data = sys.stdin.read()

    graph, search_start, search_color = create_graph(data)

    # print matrix
    graph.print_adjacency_matrix()

    # run bfs
    graph.bfs(search_start, search_color)

    # reset by creating graph again
    graph, search_start, search_color = create_graph(data)

    # run dfs
    graph.dfs(search_start, search_color)


if __name__ == "__main__":
    main()
