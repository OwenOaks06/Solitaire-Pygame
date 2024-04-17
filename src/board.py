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
        self.aceColumns = []
        self.aceColumny = []
        self.aceColumnx = 100 + 7 * (self.WINDOW_WIDTH/9)
        self.columnPosx = []
        self.columnPosy = []
        self.aceBaseImgs = []
        self.aceBaseImgs.append(pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets', 'cards', 'bases', 'clubsAceBase.png')).convert_alpha())
        self.aceBaseImgs.append(pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets', 'cards', 'bases', 'heartsAceBase.png')).convert_alpha())
        self.aceBaseImgs.append(pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets', 'cards', 'bases', 'spadesAceBase.png')).convert_alpha())
        self.aceBaseImgs.append(pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets', 'cards', 'bases', 'diamondsAceBase.png')).convert_alpha())
        for i in range(4):
            self.aceColumns.append([])
        for i in range(4):
            self.aceColumny.append(100 + (i*150))
        for i in range(self.NUM_COLUMNS):
            self.columns.append([])
        for i in range(self.NUM_COLUMNS):
            self.columnPosx.append(100 + i * (self.WINDOW_WIDTH/9))
        for i in range(20):
            self.columnPosy.append(100 + (i*40))

    def dealDeck(self, deck):
        max = 1
        for i in range(self.NUM_COLUMNS):
            for j in range(max):
                self.columns[i].append(deck.pickCard())
                self.columns[i][j].rect.center = (self.columnPosx[i], self.columnPosy[j])
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
    
    def moveCard(self, sourceCard, sourceCol, targetCol, toAce):
        sourceColumn = self.columns[sourceCol]
        if toAce:
            targetColumn = self.aceColumns[targetCol]
        else:
            targetColumn = self.columns[targetCol]
        cardLoc = sourceColumn.index(sourceCard)
        # If moving to an ace pile
        if toAce:
            # If there are cards in the pile
            if len(targetColumn) > 0:
                targetCard = targetColumn[len(targetColumn)-1]
                # Move legality check
                if sourceCard.faceUp and sourceCard.suit == Deck.SUITS[targetCol] and sourceCard.number == targetCard.number+1 and cardLoc == len(sourceColumn)-1:
                    sourceCard.rect.center = (self.aceColumnx, self.aceColumny[targetCol])
                    targetColumn.append(sourceColumn.pop(len(sourceColumn)-1))
                    sourceCard.moving = False
                    sourceCard.locked = True
                    return True
            # If the ace pile is empty
            else:
                # Move legality check
                if sourceCard.faceUp and sourceCard.suit == Deck.SUITS[targetCol] and sourceCard.number == 1:
                    sourceCard.rect.center = (self.aceColumnx, self.aceColumny[targetCol])
                    targetColumn.append(sourceColumn.pop(len(sourceColumn)-1))
                    sourceCard.moving = False
                    sourceCard.locked = True
                    return True
        # Normal card pile
        else:
            # If the pile has cards
            if len(targetColumn) > 0:
                targetCard = targetColumn[len(targetColumn)-1]
                # Move legality check
                if sourceCard.faceUp and sourceCard.color != targetCard.color and sourceCard.number == targetCard.number-1:
                    for i in sourceColumn[cardLoc:len(sourceColumn)]:
                        i.rect.center = (self.columnPosx[targetCol], self.columnPosy[len(targetColumn)])
                        targetColumn.append(sourceColumn.pop(sourceColumn.index(i)))
                        i.moving = False
                        return True
            # If the pile is empty
            else:
                for i in sourceColumn[cardLoc:len(sourceColumn)]:
                    # Move legality check
                    if sourceCard.faceUp and sourceCard.number == 13:
                        i.rect.center = (self.columnPosx[targetCol], self.columnPosy[0])
                        targetColumn.append(sourceColumn.pop(sourceColumn.index(i)))
                        i.moving = False
                        return True
        return False

    def canMoveCard(self, cardToMove, column, event):
        if not cardToMove.faceUp or cardToMove.locked: return False
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
            fail = False
            success = False
            target = -1
            ace = False
            for card in column:
                fail = False
                if column.index(card) == len(column)-1:
                    card.faceUp = True
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
                        if card.moving:
                            for pos in self.columnPosx:
                                if abs(card.rect.centerx - pos) < 50 and abs(card.rect.centery - self.columnPosy[len(self.columns[self.columnPosx.index(pos)])]) < 50:
                                    cardIndex = column.index(card)
                                    if self.moveCard(card, self.columns.index(column), self.columnPosx.index(pos), False):
                                        for i in column[cardIndex:len(column)]:
                                            self.moveCard(i, self.columns.index(column), self.columnPosx.index(pos), False)
                                    else:
                                        for i in column[cardIndex:len(column)]:
                                            i.rect.center = (self.columnPosx[self.columns.index(column)], self.columnPosy[column.index(i)])

                            for pos in self.aceColumny:
                                if abs(card.rect.centery - pos) < 50 and abs(card.rect.centerx - self.aceColumnx) < 50 and not self.moveCard(card, self.columns.index(column), self.aceColumny.index(pos), True):
                                    for i in column[column.index(card):len(column)]:
                                        i.rect.center = (self.columnPosx[self.columns.index(column)], self.columnPosy[column.index(i)])
                        card.moving = False

                    elif event.type == MOUSEMOTION and card.moving:
                        card.rect.move_ip(event.rel)
                        
    
    def draw(self, screen):
        for i in self.aceBaseImgs:
            screen.blit(i, (self.aceColumnx - i.get_width()/2, self.aceColumny[self.aceBaseImgs.index(i)] - i.get_height()/2))
        for i in self.columns:
            for j in i:
                if not j.moving:
                    j.draw(screen)
        for i in self.aceColumns:
            for j in i:
                j.draw(screen)
        for i in self.columns:
            for j in i:
                if j.moving:
                    j.draw(screen)
        