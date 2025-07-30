import time
import math
from algorithms.node import Node

# Alianno and Charlie
class Minimax:
    def __init__(self, max_depth = 4):
        """
        Initialize the Minimax algorithm.
        """
        self.max_depth = max_depth # The max node depth that the algorithm is allowed to explore (default is 4)
        self.root_node = None # The root node
        self.execution_time = 0 # Execution time, in seconds
        self.performance_metrics = {} # Holds performance metrics, such as execution_time, nodes_evaluated, total_nodes_generated

    def choose_move(self, game):
        """
        Choose the best move using the Minimax algorithm and the Node tree.
        """
        # Reset counters
        Node.reset_counters()
        start_time = time.time()

        # Initialize root node
        self.root_node = Node(game = game, depth = 0)

        # Compute utility from root using recursive minimax
        self.start_minimax(self.root_node, self.max_depth, maximizing = True)

        # Get best move from root node
        best_move = self.root_node.get_best_move()

        # Performance info
        end_time = time.time()
        self.execution_time = end_time - start_time
        self.performance_metrics = {
            'algorithm': 'Minimax',
            'max_depth': self.max_depth,
            'execution_time': self.execution_time,
            'nodes_evaluated': Node.nodes_evaluated,
            'total_nodes_generated': Node.total_nodes_generated,
        }

        print(f"Minimax Performance:")
        print(f"  Execution time: {self.execution_time:.4f} seconds")
        print(f"  Nodes evaluated: {Node.nodes_evaluated}")
        print(f"  Total nodes generated: {Node.total_nodes_generated}")

        # Returns the best move, and the root_node, so the graphing method can draw out the graph
        return best_move, self.root_node

    def start_minimax(self, node, max_depth, maximizing):
        """
        Starts the recursive minimax algorithm that creates a node tree to find the best move
        """
        # Expand current node
        node.expand_children(max_depth)

        # If it's a terminal or depth-limited node, return its utility
        if node.utility is not None:
            return node.utility

        # If MAXIMIZING NODE
        if maximizing: 
            best_value = -math.inf
            for child in node.children:
                value = self.start_minimax(child, max_depth, maximizing = False)
                best_value = max(best_value, value)
            node.utility = best_value
        else:
            best_value = math.inf
            for child in node.children:
                value = self.start_minimax(child, max_depth, maximizing = True)
                best_value = min(best_value, value)
            node.utility = best_value

        return node.utility

    def get_performance_metrics(self):
        return self.performance_metrics.copy()
