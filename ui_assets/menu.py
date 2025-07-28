import pygame
from game.game import Game 
from pygame.locals import *

# Set up Clickable Button Class
class Button():
    # Initialize function
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.topleft = (x, y)
        self.pressed = False

    # Draw button on screen
    def draw(self, display, color):
        pygame.draw.rect(display, color, self.rect, 2)

    # Check mouse position to see if button has been clicked
    def clicked(self):
        action = False
        # Get mouse position
        pos = pygame.mouse.get_pos()
        # Check if mouse is over button and clicking
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.pressed == False:
                self.pressed = True
                action = True
        # "Unpress" button if not already
        if pygame.mouse.get_pressed()[0] == 0:
            self.pressed = False
        return action

# Set up TicTacToe display for turns. Adjustable size.
class TicTac_Layout:
    # Initialize function
    def __init__(self, x, y, width, image1, image2):
        self.rect = pygame.Rect(x, y, width, width)
        self.rect.topleft = (x, y)
        self.imagex = image1
        self.imageo = image2

    # Draw "game" turn
    def draw_turn(self, display, game:Game):
        # Draw white square to reset display
        pygame.draw.rect(display, (255, 255, 255), pygame.Rect(self.rect.x+10, self.rect.y+10, self.rect.width, self.rect.height))
        
        # Figure out component dimensions based on board size
        size = game.board_size
        game_width = self.rect.width * 0.9
        diff = self.rect.width - game_width
        square_width = game_width / size
        line_width = square_width * 0.1
        square_width -= line_width

        # Scale X and O's to board size
        imagex = pygame.transform.scale(self.imagex, (square_width, square_width))
        imageo = pygame.transform.scale(self.imageo, (square_width, square_width))

        # Base variables
        base_x = self.rect.x + diff
        x = base_x
        y = self.rect.y + diff

        # Matrix Loop
        i = 0
        while i < size:
            j = 0
            while j < size - 1:
                # Place image
                if game.board[i][j] == "X":
                    display.blit(imagex, (x, y))
                elif game.board[i][j] == "O":
                    display.blit(imageo, (x, y))
                x += square_width
                # Draw vertical divider lines on the first loop so it doesn't extend off the screen in future loops
                if (i == 0):
                    pygame.draw.rect(display, (0, 0, 0), pygame.Rect(x, y, line_width, game_width))
                x += line_width
                j += 1
            # Once loop reaches final square, stop making lines and place last image
            if game.board[i][j] == "X":
                display.blit(imagex, (x, y))
            elif game.board[i][j] == "O":
                display.blit(imageo, (x, y))

            # Reset x axis, draw horizontal divider, and loop from next y
            if i < size - 1:
                x = base_x
                y += square_width
                pygame.draw.rect(display, (0, 0, 0), pygame.Rect(x, y, game_width, line_width))
                y += line_width
            i += 1
        # Update Screen
        pygame.display.update()

    def clicked_rowcol(self, game:Game):
        # Get mouse position
        row = -1
        col = -1
        pos_x, pos_y = pygame.mouse.get_pos()
        
        base_x = self.rect.x + (self.rect.width * 0.1)
        base_y = self.rect.y + (self.rect.width * 0.1)
        game_width = self.rect.width * 0.9
        square_width = game_width / game.board_size

        # Check if mouse is over board
        if base_x <= pos_x <= base_x + game_width and base_y <= pos_y <= base_y + game_width:
            col = int((pos_x - base_x) // square_width)
            row = int((pos_y - base_y) // square_width)
        return row, col