from game import Game
import random

# Alianno
class RandomGame(Game):
    # Overides Game's __init__
    # random_round_interval: How many rounds it takes for the random event to go off
    def __init__(self, board_size = 3, active_player = "X", random_round_interval = 3):
        super().__init__(board_size, active_player)
        self.random_round_interval = random_round_interval
        self.turn_count = 0

    # THIS OVERRIDES Game's apply_move
    def apply_move(self, move):
        new_game = super().apply_move(move) # runs the original game apply_move method
        new_game.round_count = self.round_count + 1

        # Check if a random event should happen
        if new_game.round_count % self.random_round_interval == 0:
            new_game.randomly_clear_occupied_square()

        return new_game

    def randomly_clear_occupied_square(self):
        # Collect all occupied positions
        occupied = [(r, c) for r in range(self.board_size)
                            for c in range(self.board_size)
                            if self.board[r][c] != " "]
        if occupied:
            r, c = random.choice(occupied)
            self.board[r][c] = " "
        return


    
