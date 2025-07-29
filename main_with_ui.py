import pygame
from pygame.locals import *
from ui_assets.menu import Button, TicTac_Layout
from game.game import Game
from game.random_game import RandomGame
from algorithms.minimax import Minimax
from algorithms.alphabeta import AlphaBetaPruning
from algorithms.expectiminimax import Expectiminimax
from decision_tree.generate_decision_tree import generate_decision_tree
import sys

# Initialize pygame
pygame.init()

# Color variables
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Display Settings
DISPLAYSURF = pygame.display.set_mode((1400,600))
DISPLAYSURF.fill(WHITE)
FPS = pygame.time.Clock()
FPS.tick(30)

# Set up Text and Font
font = pygame.font.SysFont("Verdana", 20)
text1 = font.render("AI 1 vs AI 2", True, BLACK)
text2 = font.render("Player vs AI 1", True, BLACK)
text3 = font.render("Board Size", True, BLACK)
text4 = font.render("Game Type", True, BLACK)
text5 = font.render("AI 1 Strategy", True, BLACK)
text6 = font.render("AI 2 Strategy", True, BLACK)
text7 = font.render("Clear Board", True, BLACK)
text8 = font.render("Visualize Desicion Tree", True, BLACK)
console = "Pick an option.\n\nSize: 3\nGame Type: Regular\nAI 1 Strat: Minimax(8)\nAI 2 Strat: Minimax(8)"

# Load sprites
baseimagex = pygame.image.load(r"images\ticx.png").convert_alpha()
baseimageo = pygame.image.load(r"images\tico.png").convert_alpha()

# Set up custom events and state variable
keyboardinput = pygame.USEREVENT + 0
player_vs_ai = pygame.USEREVENT + 1
ai_vs_ai = pygame.USEREVENT + 2
clear = pygame.USEREVENT + 3
vizualise = pygame.USEREVENT + 4
state = "title"
buttonchanged = True

# Create Button instances
test_button1 = Button(615, 30, 160, 30)
test_button2 = Button(615, 70, 160, 30)
test_button3 = Button(800, 30, 160, 30)
test_button4 = Button(800, 70, 160, 30)
test_button5 = Button(800, 110, 160, 30)
test_button6 = Button(800, 150, 160, 30)
test_button7 = Button(615, 150, 160, 30)
test_button8 = Button(615, 110, 250, 30)

# Initialize Game Settings and Player Variables
boardsize = 3
gameplay = TicTac_Layout(30, 30, 500, baseimagex, baseimageo)
tictactoe = Game(board_size = boardsize)
game_type = "Regular"
depth_limit1 = 8
depth_limit2 = 8
rdm_event = 6
player1 = Minimax(max_depth=depth_limit1)
player2 = Minimax(max_depth=depth_limit2)
ai1_strat = "Minimax"
ai2_strat = "Minimax"
decision_tree_root = None

# Draw Tic Tac Toe board layout
pygame.draw.rect(DISPLAYSURF, BLACK, pygame.Rect(30, 30, 570, 550), 2)

# Draw buttons, button text
def updatebuttons(buttonchanged):
    if buttonchanged:
        pygame.draw.rect(DISPLAYSURF, WHITE, pygame.Rect(610, 25, 355, 180))
        if state == "title":
            test_button1.draw(DISPLAYSURF, BLACK)
            test_button2.draw(DISPLAYSURF, BLACK)
            test_button3.draw(DISPLAYSURF, BLACK)
            test_button4.draw(DISPLAYSURF, BLACK)
            test_button5.draw(DISPLAYSURF, BLACK)
            test_button6.draw(DISPLAYSURF, BLACK)
            DISPLAYSURF.blit(text1, (625, 31))
            DISPLAYSURF.blit(text2, (625, 71))
            DISPLAYSURF.blit(text3, (810, 31))
            DISPLAYSURF.blit(text4, (810, 71))
            DISPLAYSURF.blit(text5, (810, 111))
            DISPLAYSURF.blit(text6, (810, 151))
        elif state == "results":
            test_button7.draw(DISPLAYSURF, BLACK)
            test_button8.draw(DISPLAYSURF, BLACK)
            DISPLAYSURF.blit(text7, (625, 151))
            DISPLAYSURF.blit(text8, (625, 111))
        buttonchanged = False
    return buttonchanged

# To update text on screen
def updateconsole(console, x, y, w, h):
    pygame.draw.rect(DISPLAYSURF, WHITE, pygame.Rect(x, y, w, h))
    # pygame.draw.rect(DISPLAYSURF, BLACK, pygame.Rect(x, y, w, h), 2) # -> to see "console" outlines
    i = y
    for line in console.splitlines():
        DISPLAYSURF.blit(font.render(line, True, BLACK), (x, i))
        i += 30
    pygame.display.update()

# To update an (AI) player's strategy
def update_strategy(player, strat, depth_limit):
    if strat == "Minimax":
        player = Minimax(max_depth=depth_limit)
    elif strat == "ABPruning":
        player = AlphaBetaPruning(max_depth=depth_limit)
    elif strat == "ExpectMM":
        player = Expectiminimax(max_depth=depth_limit, random_round_interval=rdm_event)
    else:
        player = "Human"
    return player

# To clear game board
def clear_board(type):
    if type == "Random":
        game = RandomGame(board_size=boardsize, random_round_interval=rdm_event)
    else:
        game = Game(board_size=boardsize)
    return game

# To get human player's move
def get_human_move(game, console):
    waiting = True
    console2 = "Click to enter your move: "
    while waiting == True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                row, col = gameplay.clicked_rowcol(game)
                if (row, col) in game.get_available_moves():
                    return (row, col)
                else:
                    console2 = "That spot is taken or invalid.\nTry again"
        updateconsole(console + console2, 615, 300, 350, 300)        

# Main Loop
while True:
    # Draw console, and tic tac toe board
    buttonchanged = updatebuttons(buttonchanged)
    updateconsole(console, 615, 300, 350, 300)
    gameplay.draw_turn(DISPLAYSURF, tictactoe)

    if state == "title":
        if game_type == "Random":
            console = console = f"Pick an option.\n\nSize: {boardsize}\nGame Type: {game_type}\nRandom Event Interval: {rdm_event}\nAI 1 Strat: {ai1_strat}({depth_limit1})\nAI 2 Strat: {ai2_strat}({depth_limit2})"
        else:
            console = f"Pick an option.\n\nSize: {boardsize}\nGame Type: {game_type}\nAI 1 Strat: {ai1_strat}({depth_limit1})\nAI 2 Strat: {ai2_strat}({depth_limit2})"
    
    # Check if any menu buttons have been clicked
    if state == "title":
        if test_button1.clicked():
            pygame.event.post(pygame.event.Event(ai_vs_ai))
        if test_button2.clicked():
            pygame.event.post(pygame.event.Event(player_vs_ai))
        if test_button3.clicked():
            pygame.event.post(pygame.event.Event(keyboardinput))
            state = 'changesize'
        if test_button4.clicked():
            pygame.event.post(pygame.event.Event(keyboardinput))
            state = 'changegame'
        if test_button5.clicked():
            pygame.event.post(pygame.event.Event(keyboardinput))
            state = 'strategy1'
        if test_button6.clicked():
            pygame.event.post(pygame.event.Event(keyboardinput))
            state = 'strategy2'
    if state == "results":
        if test_button7.clicked():
            pygame.event.post(pygame.event.Event(clear))
        if test_button8.clicked():
            pygame.event.post(pygame.event.Event(vizualise))

    # Events
    for event in pygame.event.get():
        # Quit Program
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Input from User Keyboard
        elif event.type == keyboardinput:
            temp = ""

            # Changing size of board
            if state == "changesize":
                console = "Type a number between 2-9:"
                updateconsole(console, 615, 300, 350, 300)
                # Wait for valid user input
                while state == "changesize":
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            temp = chr(event.key)
                    if temp.isdigit() and temp != "1" and temp != "0":
                        state = 'title'
                # Update board
                boardsize = int(temp)
                tictactoe = Game(board_size = boardsize)

            # Change Game
            elif state == "changegame":
                console = "Type a valid option:\n\n1 - Regular Game\n (Regular Tic-Tac-Toe)\n2 - Random Game\n (Every n turns, an occupied\n square randomly gets deleted)"
                updateconsole(console, 615, 300, 350, 300)
                # Wait for valid user input
                while state == "changegame":
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            temp = chr(event.key)
                    if temp.isdigit() and (temp == "1" or temp == "2"):
                        state = 'title'
                # Update board
                if temp == "1":
                    game_type = "Regular"
                    if ai1_strat == "ExpectMM":
                        ai1_strat = "Minimax"
                    if ai2_strat == "ExpectMM":
                        ai2_strat = "Minimax"
                elif temp == "2":
                    game_type = "Random"
                    state = "pick"
                    console = "Type random event interval (1-9):"
                    updateconsole(console, 615, 300, 350, 300)
                    temp = ""
                    while state == "pick":
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.KEYDOWN:
                                temp = chr(event.key)
                        if temp.isdigit() and temp != "0":
                            rdm_event = int(temp)
                            state = 'title'

            # Changing AI 1's strategy
            elif state == "strategy1":
                if game_type == "Random":
                    console = "Type one of the options for AI 1:\n1 - Minimax\n2 - Alpha Beta Pruning\n3 - Expectiminimax"
                else:
                    console = "Type one of the options for AI 1:\n1 - Minimax\n2 - Alpha Beta Pruning\n\nExpectiminimax is \nRANDOM GAME ONLY"
                updateconsole(console, 615, 300, 350, 300)
                # Wait for valid user input
                while state == "strategy1":
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            temp = chr(event.key)
                    if temp == "1" or temp == "2":
                        if temp == "1":
                            ai1_strat = "Minimax"
                        elif temp == "2":
                            ai1_strat = "ABPruning"
                        state = 'pick'
                    elif temp == "3" and game_type == "Random":
                        ai1_strat = "ExpectMM"
                        state = 'pick'
                # Change depth limit
                console = "Type depth limit for AI 1 (1-9):"
                updateconsole(console, 615, 300, 350, 300)
                temp = ""
                while state == "pick":
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            temp = chr(event.key)
                    if temp.isdigit() and temp != "0":
                        depth_limit1 = int(temp)
                        state = 'title'

            # Changing AI 2's strategy
            elif state == "strategy2":
                if game_type == "Random":
                    console = "Type one of the options for AI 2:\n1 - Minimax\n2 - Alpha Beta Pruning\n3 - Expectiminimax"
                else:
                    console = "Type one of the options for AI 2:\n1 - Minimax\n2 - Alpha Beta Pruning\n\nExpectiminimax is \nRANDOM GAME ONLY"
                updateconsole(console, 615, 300, 350, 300)
                # Wait for valid user input
                while state == "strategy2":
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            temp = chr(event.key)
                    if temp == "1" or temp == "2":
                        if temp == "1":
                            ai2_strat = "Minimax"
                        elif temp == "2":
                            ai2_strat = "ABPruning"
                        state = 'pick'
                    elif temp == "3" and game_type == "Random":
                        ai2_strat = "ExpectMM"
                        state = 'pick'
                # Change depth limit
                console = "Type depth limit for AI 2 (1-9):"
                updateconsole(console, 615, 300, 350, 300)
                temp = ""
                while state == "pick":
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            temp = chr(event.key)
                    if temp.isdigit() and temp != "0":
                        depth_limit2 = int(temp)
                        state = 'title'

        # Start an AI vs AI Match
        elif event.type == ai_vs_ai:
            state = "aivsai"
            buttonchanged = True
            updatebuttons(buttonchanged)
            # Update game settings and start game
            tictactoe = clear_board(game_type)
            player1 = update_strategy(player1, ai1_strat, depth_limit1)
            player2 = update_strategy(player2, ai2_strat, depth_limit2)
            print("-"*30)
            print("\nNEW AI VS AI GAME:\n")

            while not tictactoe.is_over():
                tictactoe.print_board()
                gameplay.draw_turn(DISPLAYSURF, tictactoe)
                xscore = tictactoe.evaluate("X")
                oscore = tictactoe.evaluate("O")
                console = f"Player X evaluated score: {xscore}\nPlayer O evaluated score: {oscore}\n\n"
                # Player 1
                if tictactoe.active_player == "X":
                    print(f"Player X turn:\n{ai1_strat} AI is thinking...\n")
                    console += f"Player X turn:\n{ai1_strat} AI is thinking..."
                    updateconsole(console, 615, 300, 350, 300)
                    move, decision_tree_root = player1.choose_move(tictactoe)
                    metrics = player1.get_performance_metrics()
                    console2 = f"Player X:\nAlgorithm: {metrics['algorithm']}\nMax Depth: {metrics["max_depth"]}\nExecution Time (s): {metrics["execution_time"]:.12f}\nNodes Evaluated: {metrics["nodes_evaluated"]}\nTotal Nodes Generated: {metrics["total_nodes_generated"]}"
                    updateconsole(console2, 975, 30, 500, 200)
                # Player 2
                elif tictactoe.active_player == "O":
                    print(f"Player O turn:\n{ai2_strat} AI is thinking...\n")
                    console += f"Player O turn:\n{ai2_strat} AI is thinking..."
                    updateconsole(console, 615, 300, 350, 300)
                    move, decision_tree_root = player2.choose_move(tictactoe)
                    metrics = player2.get_performance_metrics()
                    console2 = f"Player O:\nAlgorithm: {metrics['algorithm']}\nMax Depth: {metrics["max_depth"]}\nExecution Time: {metrics["execution_time"]:.12f}\nNodes Evaluated: {metrics["nodes_evaluated"]}\nTotal Nodes Generated: {metrics["total_nodes_generated"]}"
                    updateconsole(console2, 975, 280, 500, 200)

                tictactoe = tictactoe.apply_move(move)
            tictactoe.print_board()
            gameplay.draw_turn(DISPLAYSURF, tictactoe)
            if tictactoe.is_win("X"):
                print(f"Player X ({ai1_strat}) wins!")
                console = f"Player X ({ai1_strat}) wins!"
            elif tictactoe.is_win("O"):
                print(f"Player O ({ai2_strat}) wins!")
                console = f"Player O ({ai2_strat}) wins!"
            else:
                print("It's a draw!")
                console = "It's a draw!"
            state = "results"

        # Start a Player VS AI Match
        elif event.type == player_vs_ai:
            state = "playervsai"
            buttonchanged = True
            updatebuttons(buttonchanged)
            # Update game settings and start game
            tictactoe = clear_board(game_type)
            player2 = update_strategy(player2, ai1_strat, depth_limit1)
            print("-"*30)
            print("\nNEW PLAYER VS AI GAME:\n")

            while tictactoe.is_over() == False:
                tictactoe.print_board()
                gameplay.draw_turn(DISPLAYSURF, tictactoe)
                xscore = tictactoe.evaluate("X")
                oscore = tictactoe.evaluate("O")
                console = f"Player X evaluated score: {xscore}\nPlayer O evaluated score: {oscore}\n\n"
                # Player 1
                if tictactoe.active_player == "X":
                    print("Your turn:")
                    move = get_human_move(tictactoe, console)
                # Player 2
                elif tictactoe.active_player == "O":
                    print(f"AI 1's turn:\n{ai1_strat} AI is thinking...")
                    console += f"AI 1's turn:\n{ai1_strat} AI is thinking..."
                    updateconsole(console, 615, 300, 350, 300)
                    move, decision_tree_root = player2.choose_move(tictactoe)
                    metrics = player2.get_performance_metrics()
                    console2 = f"AI 1:\nAlgorithm: {metrics['algorithm']}\nMax Depth: {metrics["max_depth"]}\nExecution Time: {metrics["execution_time"]:.12f}\nNodes Evaluated: {metrics["nodes_evaluated"]}\nTotal Nodes Generated: {metrics["total_nodes_generated"]}"
                    updateconsole(console2, 975, 280, 500, 200)

                tictactoe = tictactoe.apply_move(move)

            tictactoe.print_board()
            gameplay.draw_turn(DISPLAYSURF, tictactoe)
            if tictactoe.is_win("X"):
                print(f"Player X (You) wins!")
                console = f"Player X (You) wins!"
            elif tictactoe.is_win("O"):
                print(f"Player O ({ai1_strat}) wins!")
                console = f"Player O ({ai1_strat}) wins!"
            else:
                print("It's a draw!")
                console = "It's a draw!"
            state = "results"
        
        elif event.type == clear:
            buttonchanged = True
            tictactoe = clear_board(tictactoe)
            console2 = ""
            updateconsole(console2, 975, 30, 500, 800)
            state = "title"

        elif event.type == vizualise:
            if decision_tree_root:
                generate_decision_tree(decision_tree_root, max_nodes=100)
                console = "Desicion Tree file created as\nvisualized_decision_tree.png\n\nShort preview generated."
                baseimagetree = pygame.image.load(r"visualized_decision_tree.png").convert_alpha()
                baseimagetree = pygame.transform.scale(baseimagetree, (400, 400))
                console2 = ""
                updateconsole(console2, 975, 30, 500, 800)
                DISPLAYSURF.blit(baseimagetree, (980, 30))
            else:
                console = "No tree available."
            updateconsole(console, 615, 300, 350, 300)

    # Update Screen
    pygame.display.update()
    
