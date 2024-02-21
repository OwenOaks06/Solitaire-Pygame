class Card:
    
    def __init__(self, suit, num):
        """Initialize a card

        Args:
            suit (String): "Diamonds" | "Clubs" | "Hearts" | "Spades"
            num (int): Ace: 1 | Numbers: 2-10 | J,Q,K: 11-13
        """
        self.suit = suit
        self.number = num