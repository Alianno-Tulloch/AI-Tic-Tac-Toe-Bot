from game import Game
from minimax import Minimax
from alphabetapruning import AlphaBeta
from expectiminimax import Exepctiminimax

def main():
    game = Game(board_size=3)
    ai = Minimax()
    # ai = AlphaBeta()
    # ai = Expectiminimax

    while not game.is_over():
        game.print_board()

        if game.active_player == "X":
            move = get_human_input(game)
        else:
            move = ai.choose_move(game)
        
        game = game.apply_move(move)

    winner = game.get_winner()
    print("Game Over! Winner:", winner if winner else "Draw")

if __name__ == "__main__":
    main()
