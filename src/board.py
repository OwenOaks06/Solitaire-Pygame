from deck import Deck
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
                self.columns[i][j].rect.center = (i * (self.WINDOW_WIDTH/8), 100 + (j*20))
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