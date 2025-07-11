def alphabeta(game, depth, alpha, beta, maximizing_player, max_player, min_player):
    """
    alpha-beta pruning th choose best move for the maximizing player
    
    Parameters:
    game (Game): The current game state
    depth (int): The maximum depth to search
    alpha (float): The best score that the maximizing player can guarantee at that level or above
    beta (float): The best score that the minimizing player can guarantee at that level or above
    maximizing_player (bool): True if it's the maximizing player's turn, False otherwise
    max_player (str): The maximizing player's identifier
    min_player (str): The minimizing player's identifier
    Returns:
    tuple (score, best_move)
    
    

    
    base case (game over or depth limit reached)
     if node is terminal or depth ==0:
         return nodes score, None 
    
     if maximizing player 
         start with worst case for maximizer
            #explore each possible move
            #recursive call 

            update alpha

            prune if beta <= alpha

        return best score and move
    
        if minimizing player
         start with worst case for minimizer
            #explore each possible move
            #recursive call 

            update beta

            prune if beta <= alpha
    
    return best scoer and move
     """
