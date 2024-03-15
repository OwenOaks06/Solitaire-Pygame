from deck import Deck
from board import Board
import pygame
from pygame.locals import QUIT
import sys
import os

pygame.init()

# Constants
WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280
FPS = 30

BACKGROUND = (0, 81, 44)

clock = pygame.time.Clock()


screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Soliatire in Python!")
board = Board(WINDOW_WIDTH, WINDOW_HEIGHT)
deck = Deck()
deck.shuffle()
board.dealDeck(deck)

while True:
    events = pygame.event.get()
    for i in board.columns:
        for j in i:
            j.update(events)
            j.draw(screen)
    
    screen.fill(BACKGROUND)

    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(FPS)
    pygame.display.update()