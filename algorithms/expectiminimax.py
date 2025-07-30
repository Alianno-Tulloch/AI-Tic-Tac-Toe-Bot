import time
import math
from algorithms.node import Node

# Alianno
class Expectiminimax:
    def __init__(self, max_depth = 4, random_round_interval = 3):
        """
        Initialize the Expectiminimax algorithm.

        Args:
            max_depth (int): Maximum depth for tree exploration
            random_round_interval (int): Number of plies before a random event occurs
        """
        self.max_depth = max_depth
        self.random_round_interval = random_round_interval  # how often randomness happens (in plies)
        self.root_node = None
        self.execution_time = 0
        self.performance_metrics = {}

    def choose_move(self, game):
        """
        Choose the best move using Expectiminimax algorithm.

        Args:
            game: Current game state

        Returns:
            tuple: Best move
        """
        Node.reset_counters()
        start_time = time.time()

        # Initialize root node
        self.root_node = Node(game = game, depth = 0)

        # Begin expectiminimax traversal
        self._expectiminimax(self.root_node, self.max_depth)

        best_move = self.root_node.get_best_move()

        # Capture performance data
        end_time = time.time()
        self.execution_time = end_time - start_time
        self.performance_metrics = {
            'algorithm': 'Expectiminimax',
            'max_depth': self.max_depth,
            'execution_time': self.execution_time,
            'nodes_evaluated': Node.nodes_evaluated,
            'total_nodes_generated': Node.total_nodes_generated,
            'nodes_pruned': Node.nodes_pruned,
        }

        print("Expectiminimax Performance:")
        print(f"  Execution time: {self.execution_time:.4f} seconds")
        print(f"  Nodes evaluated: {Node.nodes_evaluated}")
        print(f"  Total nodes generated: {Node.total_nodes_generated}")

        # Returns the best move, and the root_node, so the graphing method can draw out the graph
        return best_move, self.root_node

    def _expectiminimax(self, node, max_depth):
        """
        Recursive Expectiminimax function
        """
        node.expand_children(max_depth, random_chance_interval = self.random_round_interval)

        if node.utility is not None:
            return node.utility

        if node.node_type == "MAX":
            best_value = -math.inf
            for child in node.children:
                val = self._expectiminimax(child, max_depth)
                best_value = max(best_value, val)
            node.utility = best_value

        elif node.node_type == "MIN":
            best_value = math.inf
            for child in node.children:
                val = self._expectiminimax(child, max_depth)
                best_value = min(best_value, val)
            node.utility = best_value

        elif node.node_type == "CHANCE":
            # Expected utility over all random outcomes
            expected_utility = 0
            for child in node.children:
                val = self._expectiminimax(child, max_depth)
                expected_utility += child.probability * val
            node.utility = expected_utility

        return node.utility

    def get_performance_metrics(self):
        return self.performance_metrics.copy()
