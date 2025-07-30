from game.game import Game
import random

# Alianno
class RandomGame(Game):
    # Overides Game's __init__
    # random_round_interval: How many rounds it takes for the random event to go off
    # round_count: how many rounds it's been since a random event has gone off
    def __init__(self, board_size = 3, board = None, active_player = "X", random_round_interval = 3, round_count = 0):
        super().__init__(board_size, board, active_player)
        self.random_round_interval = random_round_interval
        self.round_count = round_count

    # THIS OVERRIDES Game's apply_move
    def apply_move(self, move):
        r, c = move
        # If you try placing an O or X on an occupied square, it fails
        if self.board[r][c] != " ":
            return "Invalid move"

        # Copy board and apply the move
        new_board = [row[:] for row in self.board]
        new_board[r][c] = self.active_player

        # Alternate the player
        next_player = "O" if self.active_player == "X" else "X"

        # Create new game instance and increment round count
        new_game = RandomGame(
            board_size=self.board_size,
            board=new_board,
            active_player=next_player,
            random_round_interval=self.random_round_interval,
            round_count=self.round_count + 1
        )

        # If round_count % random_round_interval = 0, then it triggers the randomly deleted square
        if new_game.round_count % new_game.random_round_interval == 0:
            new_game.randomly_clear_occupied_square()

        return new_game

    def randomly_clear_occupied_square(self): # Randomly deletes an occupied square from the gameboard.
        # Creates a tuple of occupied squares
        occupied = [
            (r, c)
            for r in range(self.board_size)
            for c in range(self.board_size)
            if self.board[r][c] != " "
        ]

        if occupied: # Randomly choose a square from the occupied list, and clears it
            r, c = random.choice(occupied)
            self.board[r][c] = " "