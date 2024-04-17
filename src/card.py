import pygame.sprite
import pygame.image
import os

class Card(pygame.sprite.Sprite):
    def __init__(self, suit, num):
        """Initialize a card

        Args:
            suit (String): "Diamonds" | "Clubs" | "Hearts" | "Spades"
            num (int): Ace: 1 | Numbers: 2-10 | J,Q,K: 11-13
        """
        super().__init__()
        self.suit = suit
        self.number = num
        if self.suit == "Diamonds" or self.suit == "Hearts": self.color = "red"
        else: self.color = "black"
        self.faceUp = False

        self.locked = False
        self.moving = False
        self.img_faceUp = pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets', 'cards', self.suit, str(self.number)+'.png')).convert_alpha()
        self.img_faceDown = pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets', 'cards', 'backs', 'card_back.png')).convert_alpha()
        self.image = self.img_faceDown
        self.rect = self.image.get_rect()

    def printCard(self):
        print(str(self.number) + " of " + self.suit + " " + str(self.faceUp))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)