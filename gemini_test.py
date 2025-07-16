import os
from google import genai

# Securely get the API key from the environment variable
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")
client = genai.Client(api_key=api_key)


def get_gemini_move(marker, board_size, board_state):
    """ 
    marker: str, 'X' or 'O'  
    board_size: int, e.g., 3 for 3x3
    board_state: list of lists, e.g., [['X', 'O', ''], ['', '', 'X'], ['O', '', '']]
    Returns: str, the AI's suggested move in the format "row,col"
    """
    board_str = '\n'.join([' '.join(row) for row in board_state])
    prompt = (
        f"Tic Tac Toe game of size {board_size}. You are {marker}. "
        f"Current board:\n{board_str}\n"
        "Give your next move as row,col (0-indexed), and only the move."
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text.strip()
'''
# Example usage
use_gemini = False  # Set to True to use Gemini, False for custom AI
marker = 'O'
board_size = 3
board_state = [['X', 'O', ''], ['', '', 'X'], ['O', '', '']]

if use_gemini:
    move = get_gemini_move(marker, board_size, board_state)
    print(f"Gemini suggests move: {move}")
else:
    move = get_custom_ai_move(marker, board_size, board_state)
    print(f"Custom AI ({marker}) moves at: {move}")
'''
