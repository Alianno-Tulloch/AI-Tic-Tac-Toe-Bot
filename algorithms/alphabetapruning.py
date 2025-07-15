import math  # we need math for ±math.inf

class AlphaBetaPruning:
    """
    Alpha-Beta Pruning algorithm for m×n, k-in-a-row games (e.g., Tic-Tac-Toe, Connect 4).
    Tracks node count for performance and supports depth-limited search.
    """

    def __init__(self, max_depth=4):
        self.max_depth = max_depth #max depth for search 
        self.node_count = 0 # count of nodes evaluated during the search

    def choose_move(self, game): 
        """
        Chooses the best move for the AI using Alpha-Beta Pruning.
        """
        self.node_count = 0 # reset node count for each new game
        best_value = -math.inf # initialize best value to negative infinity
        best_move = None 
        max_player = game.active_player #current player (AI) where we are trying to maximize the score
        min_player = self.get_opponent(max_player) # opponent player where we are trying to minimize the score
        alpha = -math.inf 
        beta = math.inf 
        # if beta is less than or equal to alpha, we can prune the search tree

        for move in game.get_available_moves(): # get all available moves
            # apply the move to the game state
            new_game = game.apply_move(move)
            value = self.min_value(
                new_game, self.max_depth - 1, alpha, beta, max_player, min_player
            ) # recursive alpha beta serach to evalaute the move above, its now the oppoents turn and depth is reduced by 1 as we move down

            if value > best_value:
                best_value, best_move = value, move # update best value and move if the current move is better
            alpha = max(alpha, best_value) #update alpha value

        print(f"Nodes evaluated: {self.node_count}") #total evalauted ndes
        return best_move # move ai will play

    def max_value(self, game, depth, alpha, beta, max_player, min_player): #maximizing players turn 
        # evaluates best score max_player can get from game state
        self.node_count += 1 # increment node count for each node evaluated
        if game.is_over() or depth == 0:
            return self.evaluate(game, max_player, min_player)
        # if the game is over or we reached the max depth, we evaluate the game state


        value = -math.inf
        for move in game.get_available_moves(): #loop through valid moves in current state
            next_game = game.apply_move(move)
            score = self.min_value(
                next_game, depth - 1, alpha, beta, max_player, min_player 
            ) # recursive call to min_value to evaluate the opponents best response to this move
            value = max(value, score) #best value maximizer can achieve
            alpha = max(alpha, value) #update alpha value
            if alpha >= beta:
                break  # β cutoff
        return value

    def min_value(self, game, depth, alpha, beta, max_player, min_player):  # minimizing player's turn
    # evaluates best score min_player can get from game state
        self.node_count += 1  # increment node count for each node evaluated

        if game.is_over() or depth == 0:
            return self.evaluate(game, max_player, min_player)
        # if the game is over or we reached the max depth, we evaluate the game state

        value = math.inf
        for move in game.get_available_moves():  # loop through valid moves in current state
            next_game = game.apply_move(move)
            score = self.max_value(
                next_game, depth - 1, alpha, beta, max_player, min_player
            )  # recursive call to max_value to simulate the opponent’s (maximizer's) best response
            value = min(value, score)  # best value minimizer can achieve
            beta = min(beta, value)  # update beta value
            if beta <= alpha:
                break  # α cutoff — prune branch since maximizer won’t allow it
        return value

    def evaluate(self, game, max_player, min_player):
        if game.is_win(max_player): #if max player wins, return a high score
            return 1000
        if game.is_win(min_player): # if min player wins, return a low score
            return -1000
        return game.evaluate(max_player) 

    def get_opponent(self, player): 
        return 'O' if player == 'X' else 'X' #returns the opponent player based on the current player
