from deck import Deck
from board import Board

board = Board()
deck = Deck()
deck.shuffle()
board.dealDeck(deck)
board.printBoard()