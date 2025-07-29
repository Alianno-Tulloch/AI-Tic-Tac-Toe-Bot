def get_gemini_move(client, marker, board_size, board_state, invalid_moves=None):
    """
    client: genai.Client instance
    marker: str, 'X' or 'O'
    board_size: int, e.g., 3 for 3x3
    board_state: list of lists, e.g., [['X', 'O', ''], ['', '', 'X'], ['O', '', '']]
    invalid_moves: set of tuples, e.g., {(0,0), (1,2)}
    Returns: str, the AI's suggested move in the format "row,col"
    """
    board_str = '\n'.join([f"{i}: " + ' | '.join(row) for i, row in enumerate(board_state)])
    available_moves = [(r, c) for r in range(board_size) for c in range(board_size) if board_state[r][c] == '']
    available_moves_str = ', '.join([f"({r},{c})" for r, c in available_moves])
    invalid_moves_str = ', '.join([f"({move[0]},{move[1]})" for move in invalid_moves if isinstance(move, tuple) and len(move) == 2]) if invalid_moves else "None"
    prompt = (
        f"You are playing Tic Tac Toe as {marker} on a {board_size}x{board_size} board.\n"
        f"Board format: each row is indexed, and cells are X, O, or blank.\n"
        f"Current board:\n{board_str}\n"
        f"Available moves: {available_moves_str}\n"
        f"Do NOT use any of these invalid moves: {invalid_moves_str}\n"
        "Your task: playing optimally, choose your next move as row,col (0-indexed). Respond ONLY with the move, e.g., 1,2."
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
