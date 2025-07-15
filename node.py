# Alianno
# This file implements all of the logic for how the nodes for each algorithm work

class Node:
    # Class Level variable, used for performance metrics tracking,
    # tracking how many nodes are tracked for each tree, throughout the entire game
    node_count = 0

    def __init__(self, game, game_state=None, depth=0, probability=1.0):
        """
        Represents a single node in the game tree.
        """
        # The game that is being played. Allows the node, or any algorithm that interacts with it, to access the methods of the game,
        # such as whether the game is in a winning state or not
        self.game = game

        # The current state that the game is in. AKA the current moves that have been performed.
        # Default value is None if it's the root (or chance) Node
        self.game_state = game_state
        
        self.depth = depth              # Depth in game tree - used for pruning, and utility tracking
        self.probability = probability  # Used for chance nodes - manipulated by chance nodes, default value of 1 for all other nodes
        self.children = []              # Each child node connected to this node

        # node_type: "MAX", "MIN", or "CHANCE" - is checked in the algorithms to determine how to treat each node
        self.node_type = self.get_node_type()
        
        # Base score value, aka if the outcome is a win, a loss, or a draw/past the depth limit.
        # The values for each state are arbitrary
        self.eval_score = None

        # Utility = (Score - the amount of moves it took to reach it) - faster wins WILL be prioritized
        self.utility = None

        # Increment global counter on creation - this works because once a depth limit is reached,
        # the node will simply be blocked from creating more nodes to explore
        Node.node_count += 1




    #                           EVERYTHING FROM HERE DOWN: Update method names to match with method names in the other classes



    def get_node_type(self):
        """
        Ask the Game object what type of node this is:
        "MAX", "MIN", or "CHANCE".
            - If "MAX": It is the algorithm's turn
            - If "MIN": It is the rational opponents turn, an opponent who will ALWAYS make the most optimal decision
                (Minimax, Alpha Beta Pruning)
            - If "CHANCE": It is the uncertain opponent's turn, an opponent who is expected/assumed to make random decisions,
                so your next MAX move is determined by which move has the highest chance of giving you the highest utility
                based on the moves your opponent COULD take in the future
                (Expectiminimax)
        """
        return self.game.get_node_type()

    def expand_children(self, max_depth=None):
        """
        Expands the node to look at its children.
            - If the node is a terminal/leaf node (no children, aka a win/lose/draw state), OR If the node hits the depth limit:
                - Then store evaluate and set utility
            - If the node is a CHANCE node:
                - adds all outcomes with equal probabilities.
            - If the node is a MAX or MIN node:
                - adds one child to the list, per available move.
        """

        #                                   THE REST OF THIS CODE HASNT BEEN CHECKED AND COMMENTED YET, BUT WILL BE VERY SOON



        if self.game.is_over() or (max_depth is not None and self.depth >= max_depth):
            self.eval_score = self.game.evaluate("AI")  # or self.game.active_player
            self.utility = self.adjust_score_for_depth(self.eval_score)
            return  # Do not expand further

        # CHANCE node: list of (Game object, probability) pairs
        if self.node_type == "CHANCE":
            outcomes = self.game.get_chance_outcomes()
            num_outcomes = len(outcomes)

            for next_state, _ in outcomes:
                child = Node(
                    game=next_state,
                    game_state=None,
                    depth=self.depth + 1,
                    probability=1.0 / num_outcomes
                )
                self.children.append(child)

        # MAX or MIN node: legal moves only
        else:
            states = self.game.get_available_moves()
            for state in states:
                next_state = self.game.apply_move(state)
                child = Node(
                    game=next_state,
                    game_state=state,
                    depth=self.depth + 1,
                    probability=1.0
                )
                self.children.append(child)

    def adjust_score_for_depth(self, score):
        """
        Decrease the score based on depth:
        - Fast wins = higher score
        - Slow losses = less penalized
        """
        if score == 10:
            return score - self.depth
        elif score == -10:
            return score + self.depth
        else:
            return score

