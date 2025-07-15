import math

class Minimax:
    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.node_count = 0 # To track how many nodes we evaluate for each move.
        self.player = None

    def choose_move(self, game):
        self.node_count = 0
        best_value = -math.inf
        best_move = None
        self.player = game.active_player

        for move in game.get_available_moves():
            new_game = game.apply_move(move)
            value = self.min_value(new_game, self.max_depth - 1)
            if value > best_value:
                best_value = value
                best_move = move

        print(f"Nodes evaluated: {self.node_count}")

        return best_move

    def max_value(self, game, depth):
        self.node_count += 1
        if game.is_over() or depth == 0:
            return self.evaluate(game)

        value = -math.inf
        for move in game.get_available_moves():
            value = max(value, self.min_value(game.apply_move(move), depth - 1))
        return value

    def min_value(self, game, depth):
        self.node_count += 1
        if game.is_over() or depth == 0:
            return self.evaluate(game)

        value = math.inf
        for move in game.get_available_moves():
            value = min(value, self.max_value(game.apply_move(move), depth - 1))
        return value


    # Leaving this in here for now, may be duplicate of what gets implemented in the game.
    def evaluate(self, game):
        if game.is_win(self.player):
            return 1
        elif game.is_win(self.get_opponent(self.player)):
            return -1
        else:
            return 0

    def get_opponent(self, player):
        if player == "X":
            return "O"
        else:
            return "X"



# game is defined by whatever games get implemented by the other coders, i just need to import game
#   so i can access its parameters/variables, such as figuring out who has won

#score is also implemented outside
# def outcome(game, player):
#     if (state == 0)
#



