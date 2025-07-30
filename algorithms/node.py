# Alianno
import math

class Node:
    """
    Represents a single node in the game tree.
    All algorithms will call this node class when they explore the possible outcomes.
    """

    # Performance Metrics Tracking
    total_nodes_generated = 0 # total nodes generated. NOT evaluated or pruned, just generated
    nodes_evaluated = 0 # Nodes that have been checked/evaluated/explored by the algorithm
    nodes_pruned = 0 # represents the number of nodes pruned by Alpha Beta

    def __init__(self, game, move = None, depth = 0, probability = 1.0, parent = None):
        """
        Initialize a new node.
        
        Args:
            game: Current game state
            move: Move that led to this node (None if root)
            depth: Depth in the tree
            probability: Probability for chance nodes
            parent: Parent node reference
        """
        self.game = game # the current game, and the game state that it's in
        self.move = move # the current move being explored
        self.depth = depth # the depth of the node in the tree
        self.probability = probability # The probability, (only used by chance nodes)
        self.parent = parent # the parent node, used for traversing
        self.children = [] # the list of all children of the current node

        # Node classification
        self.node_type = self.get_node_type() # "MAX", "MIN", or "CHANCE"

        # Evaluation Metrics
        """
        The utility of the node. Higher Utilty nodes are chosen.
        - Equation: (10 for win, 0 for draw/depth limited, -10 for loss) - node.depth
        """
        self.utility = None 
        self.alpha = -math.inf # Alpha value for pruning
        self.beta = math.inf # Beta value for pruning
        # added just in case we want to display depth limited nodes differently from win/loss/draw nodes
        self.is_depth_limited = False # True if evaluation was due to reaching max depth

        # Visualization Metrics
        self.is_pruned = False # Whether the node is pruned, used for data visualization
        self.is_expanded = False # Whether children have been generated, used for data visualization

        # Tracking
        Node.total_nodes_generated += 1
        self.node_id = Node.total_nodes_generated # node_id added for visualization purposes

    def get_node_type(self):
        """
        Determine whether this node is MAX, MIN, or CHANCE.
        MAX = AI's move, MIN = opponent's move
        CHANCE = used in expectiminimax for random events (if applicable)
        
        Returns:
            str: "MAX", "MIN", or "CHANCE"
        """
        if self.game.is_over():
            return "TERMINAL"
        
        # Alternate between MAX and MIN based on depth
        return "MAX" if self.depth % 2 == 0 else "MIN"
    

    def get_root_player(self):
        """ 
        Searches up the tree until it gets to the root node. Used for determining whether Algorithm (the root Maximimzing Node) wins or not
        """
        node = self
        while node.parent is not None:
            node = node.parent
        return node.game.active_player  # or node.game.starting_player if available
    
    def get_opponent(self, player):
        """Returns the opponent of the given player."""
        return "O" if player == "X" else "X"

    def evaluate_terminal_node(self):
        """
        Evaluates this node if it's terminal or depth-limited.
        Sets its utility based on win/loss/draw or evaluation heuristic.
        """
        Node.nodes_evaluated += 1
        root_player = self.get_root_player()

        if self.game.is_win(root_player):
            self.utility = 100 - self.depth  # Win for AI (higher utility = faster wins = better)
        elif self.game.is_win(self.get_opponent(root_player)):
            self.utility = -100 + self.depth  # Loss for AI (higher utility = slower loss = better)
        elif self.is_depth_limited:
            self.utility = 0  # Depth-limited node (neutral)
        else:
            self.utility = 0  # Draw or no winner


    """
    Gets the best MAX or MIN move of all the children. If no children, then returns nothing.
    MAX and MIN logic have been placed here because this base logic is used by all algorithms
    """
    def get_best_move(self):
        # if this node doesn't have any kids (caused either by being a win/draw/loss outcome, or by
        # being depth limited), then it is checked to find an outcome
        if not self.children:
            return None

        # Searches children, and returns the MAX or MIN child, depending on the node type
        best_child = self.children[0]
        for child in self.children[1:]:
            if self.node_type == "MAX":
                if child.utility is not None and (best_child.utility is None or child.utility > best_child.utility):
                    best_child = child
            elif self.node_type == "MIN":
                if child.utility is not None and (best_child.utility is None or child.utility < best_child.utility):
                    best_child = child

        return best_child.move
    
    def expand_children(self, max_depth = None, random_chance_interval = None):
        """
        Expands the node to look at its children.
            - If the node is a terminal/leaf node (no children, aka a win/lose/draw state), OR If the node hits the depth limit:
                - Then store evaluate and set utility
            - If the node is a MAX or MIN node:
                - adds one child to the list, per available move.
            - If the node is a CHANCE node:
                - Calculates the utility of the CHANCE node by adding:
                    Utility of child node / (1/number of children), which is the chance of that node being deleted
                For each child node
        """
        
        # Prevent duplicate expansion
        if self.is_expanded:
            return
        
        # If the game reaches a game over, check if it's a win/draw/loss, and return utility
        if self.game.is_over():
            self.evaluate_terminal_node() # evaluates utility, saves it to the node instance's utility value
            return
        
        # If we've reached max depth, mark as depth-limited, check if it's a win/draw/loss, and return utility
        if max_depth is not None and self.depth >= max_depth:
            self.is_depth_limited = True # sets this check on, just in case we want to visualize depth limited nodes later
            self.evaluate_terminal_node()
            return
        
        # CHANCE NODE SECTION:
        if random_chance_interval is not None and self.depth % random_chance_interval == 0 and self.depth != 0:
            self.node_type = "CHANCE"
            # Get all occupied squares
            occupied = [(r, c) for r in range(self.game.board_size)
                                for c in range(self.game.board_size)
                                if self.game.board[r][c] != " "]
            num_outcomes = len(occupied)
            if num_outcomes == 0:
                self.evaluate_terminal_node()
                return

            prob = 1.0 / num_outcomes
            for square in occupied:
                # Make a copy of the board and clear this square
                new_board = [row[:] for row in self.game.board]
                r, c = square
                new_board[r][c] = " "
                # Create a new game with same active player
                new_game = self.game.__class__(
                    board_size = self.game.board_size,
                    board = new_board,
                    active_player = self.game.active_player,
                    random_round_interval=getattr(self.game, 'random_round_interval', 3)
                )
                child_node = Node(
                    game = new_game,
                    move = ("CHANCE", square),
                    depth = self.depth + 1,
                    probability = prob,
                    parent = self
                )
                self.children.append(child_node)

            self.is_expanded = True
            return

        
        # MIN and MAX NODE SECTION
        # Checks all available moves from this game state, and creates child nodes
        moves = self.game.get_available_moves() # generates all possible moves from this exact game board state
        for move in moves:
            new_game = self.game.apply_move(move)
            child_node = Node(
                game = new_game,
                move = move,
                depth = self.depth + 1,
                probability = self.probability,  # used for chance nodes
                parent = self
            )
            self.children.append(child_node)

        self.is_expanded = True


    def format_board(self):
        """
        Returns a string representation of the game board.
        This is used when the node tree gets visualized.
        Example:    X |   | O
                    ---------
                      | X |  
                    ---------
                    O |   | X
        """
        lines = []
        size = self.game.board_size
        for r in range(size):
            row = " | ".join(self.game.board[r])
            lines.append(row)
            if r < size - 1:
                lines.append("-" * (size * 4 - 3))  # Adjusts for spacing
        return "\n".join(lines)

    

    # Resets all class performance metrics.
    @classmethod
    def reset_counters(cls):
        cls.total_nodes_generated = 0
        cls.nodes_evaluated = 0
        cls.nodes_pruned = 0

    # Returns all class performance metrics as a string
    @classmethod
    def get_performance_metrics(cls):
        return {
            'total_nodes_generated': cls.total_nodes_generated,
            'nodes_evaluated': cls.nodes_evaluated,
            'nodes_pruned': cls.nodes_pruned,
        }

    def __str__(self):
        """Text label used in visualizations or debug printouts."""
        return f"Node(id = {self.node_id}, type = {self.node_type}, depth = {self.depth}, utility = {self.utility})"

    def __repr__(self):
        return self.__str__()