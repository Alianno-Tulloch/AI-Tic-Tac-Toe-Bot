import time
import math
from algorithms.node import Node

class AlphaBetaPruning:
    """
    Alpha-Beta Pruning algorithm using the Node-based tree structure.
    """

    def __init__(self, max_depth = 4):
        self.max_depth = max_depth
        self.root_node = None
        self.execution_time = 0
        self.performance_metrics = {}

    def choose_move(self, game):
        """
        Choose the best move using Alpha-Beta Pruning on the Node tree.
        """
        # Reset performance counters
        Node.reset_counters()
        start_time = time.time()

        # Create root node
        self.root_node = Node(game = game, depth = 0)

        # Start recursive search
        self.alpha_beta(self.root_node, self.max_depth, alpha = -math.inf, beta = math.inf, maximizing = True)

        # Select best move from children
        best_move = self.root_node.get_best_move()

        # Save and print metrics
        end_time = time.time()
        self.execution_time = end_time - start_time
        self.performance_metrics = {
            'algorithm': 'AlphaBetaPruning',
            'max_depth': self.max_depth,
            'execution_time': self.execution_time,
            'nodes_evaluated': Node.nodes_evaluated,
            'total_nodes_generated': Node.total_nodes_generated,
            'nodes_pruned': Node.nodes_pruned,
        }

        print("Alpha-Beta Pruning Performance:")
        print(f"  Execution time: {self.execution_time:.4f} seconds")
        print(f"  Nodes evaluated: {Node.nodes_evaluated}")
        print(f"  Total nodes generated: {Node.total_nodes_generated}")
        print(f"  Nodes pruned: {Node.nodes_pruned}")

        return best_move

    def alpha_beta(self, node, max_depth, alpha, beta, maximizing):
        """
        Recursive alpha-beta pruning search.
        """
        node.expand_children(max_depth)

        # Terminal or depth-limited?
        if node.utility is not None:
            return node.utility

        if maximizing:
            best_value = -math.inf
            for child in node.children:
                value = self.alpha_beta(child, max_depth, alpha, beta, maximizing = False)
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)

                # Prune
                if beta <= alpha:
                    child.is_pruned = True
                    Node.nodes_pruned += 1
                    break

            node.utility = best_value
            return best_value
        else:
            best_value = math.inf
            for child in node.children:
                value = self.alpha_beta(child, max_depth, alpha, beta, maximizing = True)
                best_value = min(best_value, value)
                beta = min(beta, best_value)

                # Prune
                if beta <= alpha:
                    child.is_pruned = True
                    Node.nodes_pruned += 1
                    break

            node.utility = best_value
            return best_value

    def get_performance_metrics(self):
        return self.performance_metrics.copy()

    def get_game_tree(self):
        return self.root_node
