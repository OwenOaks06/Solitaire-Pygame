from card import Card
from card import cardsGroup
from random import shuffle
from pygame.sprite import Group

class Deck():
    NUM_SUITS = 4
    NUM_PER_SUIT = 13
    NUM_CARDS = NUM_SUITS * NUM_PER_SUIT
    SUITS = ["Diamonds", "Clubs", "Hearts", "Spades"]
    
    def __init__(self):
        """Creates a new deck and stores it in the "cards" attribute
        """
        self.cards = self.createDeck()

    
    def createDeck(self):
        """Creates a deck of cards containing the specified suits and cards and returns it

        Returns:
            list: list containing all cards in deck
        """
        cards = []
        for suit in range(self.NUM_SUITS):
            for number in range(self.NUM_PER_SUIT):
                newCard = Card(self.SUITS[suit], number+1)
                cardsGroup.add(newCard)
                cards.append(newCard)
        return cards

    def shuffle(self):
        """Shuffle the deck
        """
        shuffle(self.cards)
    
    def printDeck(self):
        """Prints a formatted list of all cards in the deck
        """
        cards = ""
        i = 1
        for card in self.cards:
            cards += str(card.number) + " of " + card.suit
            if i % 13 == 0:
                cards += "\n"
            elif i != len(self.cards):
                cards += " | "
            i += 1
        print(cards)

    def pickCard(self):
        return self.cards.pop(len(self.cards)-1)