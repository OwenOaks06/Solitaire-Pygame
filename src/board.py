from deck import Deck
from pygame.locals import MOUSEBUTTONDOWN
from pygame.locals import MOUSEBUTTONUP
from pygame.locals import MOUSEMOTION
import pygame
import os

class Board:
    NUM_COLUMNS = 7

    def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT):
        self.deck = None
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.columns = []
        for i in range(self.NUM_COLUMNS):
            self.columns.append([])

    def dealDeck(self, deck):
        max = 1
        for i in range(self.NUM_COLUMNS):
            for j in range(max):
                self.columns[i].append(deck.pickCard())
                self.columns[i][j].rect.center = (100 + i * (self.WINDOW_WIDTH/8), 100 + (j*20))
            self.columns[i][max-1].faceUp = True
            max += 1
        self.deck = deck

    def printBoard(self):
        print("Deck: ")
        for i in self.deck.cards:
            i.printCard()
        k = 1
        for i in self.columns:
            print("Column " + str(k) + ": ")
            k += 1
            for j in i:
                j.printCard()
    
    def moveCard(self, sourceCard, sourceCol, targetCol):
        sourceColumn = self.columns[sourceCol]
        targetColumn = self.columns[targetCol]
        cardLoc = sourceColumn.index(sourceCard)
        targetCard = targetColumn[len(targetColumn)-1]
        if sourceCard.faceUp and sourceCard.color != targetCard.color and sourceCard.number == targetCard.number-1:
            for i in sourceColumn[cardLoc:len(sourceColumn)]:
                targetColumn.append(sourceColumn.pop(sourceColumn.index(i)))

        return sourceCard
    
    def canMoveCard(self, cardToMove, column, event):
        if not cardToMove.faceUp: return False
        for card in column[column.index(cardToMove)::]:
            if len(column)-1 == column.index(cardToMove): return True
            nextCard = column[column.index(card)+1]
            if nextCard.rect.collidepoint(event.pos): return False
            if card.color != nextCard.color and card.number == nextCard.number+1:
                return True
            else:
                return False

    def update(self, events):
        for column in self.columns:
            for card in column:
                if card.faceUp: card.image = card.img_faceUp
                elif not card.faceUp: card.image = card.img_faceDown
                for event in events:
                    if event.type == MOUSEBUTTONDOWN:
                        if column.index(card) != len(column):
                            if column[column.index(card)-1].moving:
                                card.moving = True
                        if card.rect.collidepoint(event.pos) and self.canMoveCard(card, column, event):
                            card.moving = True
                    elif event.type == MOUSEBUTTONUP:
                        card.moving = False
                    elif event.type == MOUSEMOTION and card.moving:
                        card.rect.move_ip(event.rel)
    
    def draw(self, screen):
        for i in self.columns:
            for j in i:
                j.draw(screen)

        