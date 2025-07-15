# Alianno
import math # to access -math.inf (negative infinity)

class Expectiminimax():
    # Chance node explaination - Uncertain Opponent
    # - the algo assumes that the opponent is not fully rational, and will act at random
    
    # Implementation: If this algorithm is selected, it assumes that Gemini is opponents an Uncertain Opponent, and 
    # that the Human is a certain opponent. Therefore, AI vs Algo uses only Max and Chance Nodes,
    # while Human vs Algo uses Max and Min Nodes
    #       - why? because otherwise, Min is implemented for no reason. This can be changed later if needed.


    def __init__(self, max_depth = 4):
        self.max_depth = max_depth
        # node_count counts how many nodes were evaluated - for tracking performance metrics
        self.node_count = 0

    def choose_move(self, game):
        self.node_count = 0

    
    def Expectiminimax(self, node, depth):
        if game.is_over() or depth == 0:
            return self.evaluate

        #           FIX LATER
        # If this is a max node, run this code
        if node is max:
            best_value = -math.inf
            for child in node.children:
                best_value = max(best_value, ExpectiMax(child, depth - 1))
            return best_value


        #           FIX LATER
        # If this is a min node, run this code
        if node is min:
            best_value = math.inf
            for child in node.children:



        #           FIX LATER - remember to add node class, and to add child value to it
        # If this is a chance node, run this code
        else:
            best_value = 0
            for child in node.children:
                prob = probability(child)
                best_value += prob * Expectiminimax(child, depth - 1)
            return best_value

    #                       Fix later
    # The way this should work - win/lose is an arbitrary score, but the more moves/the greater the depth it took to win, 
    # the lower the score, and the less optimal this path is
    def evaluate(self, game):
        if game.is_win(game.active_player):
            return -10 - depth
        elif game.is_win(self.get_opponent(game.active_player)):
            return 10 - depth
        else:
            return 0