# Alianno - i'm just gonna put placeholder code here,
# stuff i need implemented by whoever is working on the game
#Ashvinan: added evlauate and print_board placeholders
class Game:
    '''
    Requirements:
        The game needs to be able to be played by
            - Human vs Algorithm
            - AI (Google Gemini) vs Algorithm
        
        The Game must:
            - Be Scalable (So for Tic Tac Toe, that means the grid can be dynamically chosen)
                - I.E., 3x3 grid, 5x5 grid, 7x7 grid, etc
            - Track AI and Algorithm performance metrics
                - Execution Time: Compare runtimes of Minimax and Alpha-Beta Pruning.
                - Node Evaluations: Count the number of nodes evaluated in the game tree.
                - Success Rate: Assess Algorithm win rates compared to Gemini API agents.



    In order to work, MiniMax (and the other algorithms) need to be able to see certain things
            - A way to get the currently available moves (e.g., open columns in Connect Four),
                so the algorithm knows which branches to explore.

            - A method to execute a move, and return the resulting game state 
                (e.g., dropping a piece into a column and returning a 
                new Game object with the updated board and active player).
            
            - A way to check if the game ended (either by someone winning, or both
                players drawing), so the algorithm knows when to stop recursion,
                and evaluate the result.

            - A method to check which player won (to evaluate terminal states).
            
            - A way to track whose turn it is (the active player), so the algorithm
                knows whether to minimize or maximize the score at a given depth level.
    
                
    In addition to this, the rest of the assignment also requires that the Game class also has:

            - A method that prints or display the board, so it can be connected to the UI,
                and for debugging purposes before the UI gets implemented.


            - A way to evaluate non-terminal board states (a heuristic function) if using depth-limited search.
            


            - a method to execute a move
            - a parameter that tells the algorithm when the is over, and who won
            - 
    '''

    def __init__(self, board_size=3, board=None, active_player="X"):
        self.board_size = board_size
        self.active_player = active_player
        if board:
            self.board = [row[:] for row in board]  # Deep copy
        else:
            self.board = [[" " for _ in range(board_size)] for _ in range(board_size)]

    def get_available_moves(self):
        return [(r, c) for r in range(self.board_size) for c in range(self.board_size) if self.board[r][c] == " "]

    # Pass move as a tuple of (row, column)
    def apply_move(self, move):
        r, c = move
        if self.board[r][c] != " ":
            return "Invalid move"

        new_board = [row[:] for row in self.board]
        new_board[r][c] = self.active_player
        next_player = "O" if self.active_player == "X" else "X"
        return Game(self.board_size, new_board, next_player)

    def is_over(self):
        return self.is_win("X") or self.is_win("O") or not self.get_available_moves()

    def is_win(self, player):
        b = self.board
        n = self.board_size

        # Check rows and columns
        for i in range(n):
            if all(b[i][j] == player for j in range(n)):
                return True
            if all(b[j][i] == player for j in range(n)):
                return True

        # Check diagonals
        if all(b[i][i] == player for i in range(n)):
            return True
        if all(b[i][n - 1 - i] == player for i in range(n)):
            return True

        return False


    # I just added this in case we need it for Gemini implementation.
    def print_board(self):
        for row in self.board:
            print(" | ".join(row))
            print("-" * (self.board_size * 4 - 3))


    
