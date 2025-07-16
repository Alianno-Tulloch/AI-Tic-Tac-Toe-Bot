from game import Game
from minimax import Minimax
from alphabetapruning import AlphaBetaPruning
from gemini_test import get_gemini_move
from dotenv import load_dotenv
import time
import os
from google import genai
# from expectiminimax import Exepctiminimax

def setup_gemini_client():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    return genai.Client(api_key=api_key)   

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
    # ai = Minimax(max_depth=8)
    ai = AlphaBetaPruning(max_depth=8)
    game_mode = 0  # 0 for human vs AI, 1 for AI vs AI

    print("Welcome to Tic Tac Toe!")
    game_mode = int(input("Choose game mode: 0 for Human vs AI, 1 for AI vs AI: "))
    if game_mode == 0:
        print("You are X, Minimax is O\n")
    else:
        client = setup_gemini_client()
        print("Gemini is X, Minimax is O\n")
    
    while not game.is_over():
        game.print_board()

        if game.active_player == "X":
            if game_mode == 0:
                move = get_human_move(game)
            else:
                invalid_moves = set()
                print(game.board)
                while True:
                    # Format invalid moves for prompt
                    invalid_moves_str = ', '.join([f"({move[0]},{move[1]})" for move in invalid_moves if isinstance(move, tuple) and len(move) == 2]) if invalid_moves else "None"
                    response = get_gemini_move(client, "X", board_size, game.board, invalid_moves_str)
                    try:
                        move = tuple(map(int, response.strip().split(",")))
                        if move in game.get_available_moves():
                            break
                        else:
                            if move in invalid_moves:
                                print(f"Gemini keeps suggesting the same invalid move {move}. Retrying...")
                            else:
                                print(f"Gemini suggested invalid move {move}. Retrying...")
                            invalid_moves.add(move)
                    except Exception:
                        print(f"Gemini response '{response}' could not be parsed. Retrying...")
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
