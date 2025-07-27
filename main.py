from game import Game
from random_game import RandomGame
from minimax import Minimax
from alphabeta import AlphaBetaPruning
from expectiminimax import Expectiminimax
import time
# from expectiminimax import Exepctiminimax

def get_human_move(game):
    while True:
        try:
            raw = input("Enter your move as row,col (e.g., 0,1): ")
            row, col = map(int, raw.strip().split(","))
            if (row, col) in game.get_available_moves():
                return (row, col)
            else:
                print("That spot is taken or invalid. Try again.")
        except Exception:
            print("Invalid format. Enter row,col (e.g., 0,2).")

def main():
    board_size = 3  # Change to 5 or 7 for larger boards if you implement scalable heuristics
    game = Game(board_size = board_size, active_player = "X")
    game = RandomGame(board_size = board_size, active_player = "X", random_round_interval = 3)
    ai = Minimax(max_depth = 8)
    # ai = AlphaBetaPruning(max_depth = 8)
    # ai = Expectiminimax(max_depth = 8, random_round_interval = 3)

    print("Welcome to Tic Tac Toe!")
    print("You are X, Minimax is O\n")
    
    while not game.is_over():
        game.print_board()

        if game.active_player == "X":
            move = get_human_move(game)
        else:
            print("Minimax AI is thinking...\n")
            start_time = time.time()
            move = ai.choose_move(game)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Execution time: {execution_time:.12f} seconds")

        game = game.apply_move(move)

    game.print_board()

    if game.is_win("X"):
        print("You (X) win!")
    elif game.is_win("O"):
        print("Minimax (O) wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()