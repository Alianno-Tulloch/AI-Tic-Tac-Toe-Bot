from graphviz import Digraph

# Alianno
def generate_decision_tree(root_node, filename = "visualized_decision_tree", max_nodes = 100):

    dot = Digraph(comment = "AI Decision Tree") # creates a directional graph
    dot.attr(rankdir = "TB", splines = "true", nodesep = "0.5", ranksep = "0.75")
    visited = set()

    def add_node(node):
        if len(visited) > max_nodes:
            return

        # adds visisted nodes to this list, so the function doesn't accidentally traverse/graph them multiple times
        node_id = str(id(node))
        visited.add(node_id)

        # The label for all the chance nodes
        label  = f"{node.node_type}\n" # Node type
        label += f"Utility: {node.utility}\n" # node utility
        label += f"Node Depth: {node.depth}\n" # node depth
        label += f"{node.format_board()}\n" # the game move that it represents
        if node.node_type == "CHANCE": # display the probability of each of the chance node's children occuring (chance of each node getting deleted)
            chance = node.probability / len(node.children)
            label += f"Probability of each child: {chance:.3f}"

        # Visual appearance
        shape      = "ellipse"
        color      = "black"
        style      = "filled"
        fillcolor  = "white"

        if node.node_type == "MAX":
            shape      = "box"
            fillcolor  = "lightblue"
        elif node.node_type == "MIN":
            shape      = "box"
            fillcolor  = "lightpink"
        elif node.node_type == "CHANCE":
            shape      = "diamond"
            fillcolor  = "lightyellow"
        elif node.node_type == "TERMINAL":
            shape      = "oval"
            fillcolor  = "gray90"

        if node.is_pruned:
            style      = "filled,dashed"
            fillcolor  = "gray80"

        dot.node(node_id, label = label, shape = shape, style = style, color = color, fillcolor = fillcolor)

        for child in node.children:
            child_id = str(id(child))
            dot.edge(node_id, child_id)
            add_node(child)

    add_node(root_node)
    dot.render(filename, format = "png", cleanup = True)  # Generates visualized_decision_tree.png
