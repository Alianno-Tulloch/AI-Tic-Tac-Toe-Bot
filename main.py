from game import Game
from minimax import Minimax
from alphabetapruning import AlphaBetaPruning
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
    game = Game(board_size=board_size, active_player="X")
    ai = Minimax(max_depth=4)

    print("Welcome to Tic Tac Toe!")
    print("You are X, Minimax is O\n")
    
    while not game.is_over():
        game.print_board()

        if game.active_player == "X":
            move = get_human_move(game)
        else:
            print("Minimax AI is thinking...\n")
            move = ai.choose_move(game)

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