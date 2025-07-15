# Juan

import sys
import pygame
from pygame.locals import *

from menu.menu import Button, TicTac_Layout

from game.game import Game
from algorithms.minimax import Minimax
from algorithms.alphabetapruning import AlphaBetaPruning

# Initialize pygame
pygame.init()

# Color variables
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Display Settings
DISPLAYSURF = pygame.display.set_mode((1000,600))
DISPLAYSURF.fill(WHITE)
FPS = pygame.time.Clock()
FPS.tick(30)

# Set up Text and Font
font = pygame.font.SysFont("Verdana", 20)
text1 = font.render("AI 1 vs AI 2", True, BLACK)
text2 = font.render("Player vs AI 1", True, BLACK)
text3 = font.render("Board Size", True, BLACK)
text4 = font.render("AI 1 Strategy", True, BLACK)
text5 = font.render("AI 2 Strategy", True, BLACK)
console1 = "Pick an option."
console2 = ""
console3 = "AI 1 Strat: Minimax" 
console4 = "AI 2 Strat: Minimax"

# Load sprites
square_img = pygame.image.load("images/square.png").convert_alpha()
baseimagex = pygame.image.load("images/ticx.png").convert_alpha()
baseimageo = pygame.image.load("images/tico.png").convert_alpha()

# Set up custom events and state variable
keyboardinput = pygame.USEREVENT + 0
player_vs_ai = pygame.USEREVENT + 1
ai_vs_ai = pygame.USEREVENT + 2
state = "title"

# Create Button instances
test_button1 = Button(620, 30, 180, 30)
test_button2 = Button(620, 70, 180, 30)
test_button3 = Button(620, 110, 180, 30)
test_button4 = Button(620, 150, 180, 30)
test_button5 = Button(620, 190, 180, 30)

# Initialize Game Settings and Player Variables
boardsize = 3
gameplay = TicTac_Layout(30, 30, 500, baseimagex, baseimageo)
tictactoe = Game(boardsize, None, "X")
player1 = Minimax(4)
player2 = Minimax(4)
ai1_strat = "Minimax"
ai2_strat = "Minimax"

# Draw buttons, button text and tictactoe outline
test_button1.draw(DISPLAYSURF, BLACK)
test_button2.draw(DISPLAYSURF, BLACK)
test_button3.draw(DISPLAYSURF, BLACK)
test_button4.draw(DISPLAYSURF, BLACK)
test_button5.draw(DISPLAYSURF, BLACK)
DISPLAYSURF.blit(text1, (635, 31))
DISPLAYSURF.blit(text2, (635, 71))
DISPLAYSURF.blit(text3, (635, 111))
DISPLAYSURF.blit(text4, (635, 151))
DISPLAYSURF.blit(text5, (635, 191))
pygame.draw.rect(DISPLAYSURF, BLACK, pygame.Rect(30, 30, 570, 550), 2)

# To update text on screen
def updateconsole():
    pygame.draw.rect(DISPLAYSURF, WHITE, pygame.Rect(615, 300, 400, 400))
    DISPLAYSURF.blit(font.render(console1, True, BLACK), (615, 300))
    DISPLAYSURF.blit(font.render(console2, True, BLACK), (615, 330))
    DISPLAYSURF.blit(font.render(console3, True, BLACK), (615, 360))
    DISPLAYSURF.blit(font.render(console4, True, BLACK), (615, 390))
    pygame.display.update()

# To update an (AI) player's strategy
def update_strategy(player, strat):
    if strat == "Minimax":
        player = Minimax(4)
    elif strat == "ABPruning":
        player = AlphaBetaPruning(4)
    elif strat == "ExpectMM":
        pass
        # player = Expectiminimax(4)


# Main Loop
while True:
    # Draw console and tic tac toe board
    updateconsole()
    gameplay.draw_turn(DISPLAYSURF, tictactoe)
    
    # Check if any menu buttons have been clicked
    if test_button1.clicked():
        pygame.event.post(pygame.event.Event(ai_vs_ai))
    if test_button2.clicked():
        pygame.event.post(pygame.event.Event(player_vs_ai))
    if test_button3.clicked():
        pygame.event.post(pygame.event.Event(keyboardinput))
        state = 'changesize'
    if test_button4.clicked():
        pygame.event.post(pygame.event.Event(keyboardinput))
        state = 'strategy1'
    if test_button5.clicked():
        pygame.event.post(pygame.event.Event(keyboardinput))
        state = 'strategy2'

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
                console1 = "Type a number between 2-9"
                updateconsole()
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
                tictactoe = Game(boardsize, None, "X")
                console1 = "Pick an option."

            # Changing AI 1's strategy
            elif state == "strategy1":
                console1 = "Type one of the options for AI 1:"
                console2 = "1 - Minimax"
                console3 = "2 - Alpha Beta Pruning"
                console4 = "3 - Expectiminimax"
                updateconsole()
                # Wait for valid user input
                while state == "strategy1":
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            temp = chr(event.key)
                    if temp == "1" or temp == "2" or temp == "3":
                        if temp == "1":
                            ai1_strat = "Minimax"
                        elif temp == "2":
                            ai1_strat = "ABPruning"
                        else:
                            ai1_strat = "ExpectMM"
                        state = 'title'
                # Update board
                console1 = "Pick an option."
                console2 = ""
                console3 = "AI 1 Strat: " + ai1_strat
                console4 = "AI 2 Strat: " + ai2_strat
                tictactoe = Game(boardsize, None, "X")

            # Changing AI 2's strategy
            elif state == "strategy2":
                console1 = "Type one of the options for AI 1:"
                console2 = "1 - Minimax"
                console3 = "2 - Alpha Beta Pruning"
                console4 = "3 - Expectiminimax"
                updateconsole()
                # Wait for valid user input
                while state == "strategy2":
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            temp = chr(event.key)
                    if temp == "1" or temp == "2" or temp == "3":
                        if temp == "1":
                            ai2_strat = "Minimax"
                        elif temp == "2":
                            ai2_strat = "ABPruning"
                        else:
                            ai2_strat = "ExpectMM"
                        state = 'title'
                # Update board
                console1 = "Pick an option."
                console2 = ""
                console3 = "AI 1 Strat: " + ai1_strat
                console4 = "AI 2 Strat: " + ai2_strat
                tictactoe = Game(boardsize, None, "X")

        # Start an AI vs AI Match
        elif event.type == ai_vs_ai:
            # Update game settings and start game
            tictactoe = Game(boardsize, None, "X")
            update_strategy(player1, ai1_strat)
            update_strategy(player2, ai2_strat)

            while tictactoe.is_over() == False:
                # Player 1
                if tictactoe.is_over() == False:
                    console1 = "Player X turn:"
                    updateconsole()
                    gameplay.draw_turn(DISPLAYSURF, tictactoe)
                    tictactoe = tictactoe.apply_move(player1.choose_move(tictactoe))
                    tictactoe.print_board()
                # Player 2
                if tictactoe.is_over() == False:
                    console1 = "Player O turn:"
                    updateconsole()
                    gameplay.draw_turn(DISPLAYSURF, tictactoe)
                    tictactoe = tictactoe.apply_move(player2.choose_move(tictactoe))
                    tictactoe.print_board()
            
            console1 = "Game Over"
            state = "results"

        # Start a Player VS AI Match ----------------NOT COMPLETE-----------------------
        elif event.type == player_vs_ai:
            # Update game settings and start game
            tictactoe = Game(3, None, "X")
            update_strategy(player2, ai1_strat)
            while tictactoe.is_over() == False:
                # Player 1
                tictactoe.print_board()
                gameplay.draw_turn(DISPLAYSURF, tictactoe)
                #     IMPLEMENT PLAYER INPUT




                #   tictactoe = tictactoe.apply_move())
                # Player 2
                tictactoe.print_board()
                gameplay.draw_turn(DISPLAYSURF, tictactoe)
                tictactoe = tictactoe.apply_move(player2.choose_move(tictactoe))
            
            console1 = "game over"
            state = "results"

    # Update Screen
    pygame.display.update()
