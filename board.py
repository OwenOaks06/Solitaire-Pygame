from deck import Deck

class Board:
    NUM_COLUMNS = 7

    def __init__(self):
        self.columns = []
        for i in range(self.NUM_COLUMNS):
            self.columns.append([])

    def dealDeck(self, deck):
        max = 1
        for i in range(self.NUM_COLUMNS):
            for j in range(max):
                self.columns[i].append(deck.pickCard())
            self.columns[i][max-1].faceUp = True
            max += 1

    def printBoard(self):
        k = 1
        for i in self.columns:
            print("Column " + str(k) + ": ")
            k += 1
            for j in i:
                j.printCard()
    
    def moveCard(self, sourceCol, targetCol):
        sourceColumn = self.columns[sourceCol]
        targetColumn = self.columns[targetCol]
        
