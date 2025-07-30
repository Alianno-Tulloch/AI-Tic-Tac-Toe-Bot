# Alianno and Charlie
class Game:
    """
    board_size: The size of the game board, n x n. For example, 3x3, 5x5, 7x7
    board: The current state of the game board. 
        Example,    X |   | O
                    ---------
                      | X |  
                    ---------
                    O |   | X

    active_player: who's turn it currently is = X is Player 1 (Human), O is the AI/ Google Gemini
    """
    def __init__(self, board_size = 3, board = None, active_player = "X"):
        self.board_size = board_size
        self.active_player = active_player
        if board:
            self.board = [row[:] for row in board]  # Deep copy existing board
        else:
            self.board = [[" " for _ in range(board_size)] for _ in range(board_size)] # Create new game board from scratch

    # Returns all of the unoccupied squares on the game board
    def get_available_moves(self):
        return [(r, c) for r in range(self.board_size) for c in range(self.board_size) if self.board[r][c] == " "]

    # Attempts to place an X or an O on position r,c on the game board. Fails if the location is already taken
    def apply_move(self, move):
        r, c = move
        if self.board[r][c] != " ": # if the square is occupied, the move fails
            return "Invalid move"

        new_board = [row[:] for row in self.board]
        new_board[r][c] = self.active_player # places an X (for player) or an O (for the AI) on position r,c on the game board.
        next_player = "O" if self.active_player == "X" else "X" # updates who's turn is next. Useful for AI vs AI gameplay
        return Game(self.board_size, new_board, next_player)

    def is_over(self):
        # Returns True if Player X (Human) won, if Player O (Algorithm) won, or if the game board is full.
        # Returns False Otherwise
        return self.is_win("X") or self.is_win("O") or not self.get_available_moves()

    def is_win(self, player): # Checks all rows, columns, and diagonals, to see if the selected player won
        b = self.board
        n = self.board_size

        # Check rows and columns. Returns True if current player filled every line in the row/column
        for i in range(n):
            if all(b[i][j] == player for j in range(n)):
                return True
            if all(b[j][i] == player for j in range(n)):
                return True

        # Check diagonals. Returns True if current player filled every line in the diagonal
        if all(b[i][i] == player for i in range(n)):
            return True
        if all(b[i][n - 1 - i] == player for i in range(n)):
            return True

        return False # Returns False if the current player hasn't won


    # I just added this in case we need it for Gemini implementation.
    def print_board(self):
        for row in self.board:
            print(" | ".join(row))
            print("-" * (self.board_size * 4 - 3))

    
    def evaluate(self, player): #checks how good the board looks for the player
        """
        Heuristic evaluation function for non-terminal game states.
        Gives a basic score based on how many lines are still open for the player.
        """
        opponent = "O" if player == "X" else "X"
        score = 0
        n = self.board_size
        b = self.board #saves board size and boards itself into shorter names for easier use

        def line_score(line): #line_score checks how many lines are open for the player 
            if opponent in line:
                return 0 #if other play is in it, return 0 points
            return line.count(player)  #otherwise give you 1 point for each of your pieces in that line
 
        lines = [] 

        # Rows and columns
        for i in range(n): #add all rows and columns to the lines
            lines.append(b[i])  # row
            lines.append([b[j][i] for j in range(n)])  # column

        # Diagonals
        lines.append([b[i][i] for i in range(n)])  # main diagonal
        lines.append([b[i][n - 1 - i] for i in range(n)])  # anti-diagonal

        for line in lines:
            score += line_score(line) #adds results of line_score to the score

        return score


    
