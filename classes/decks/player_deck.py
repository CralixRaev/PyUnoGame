# здесь использую то же название "колода" для удобства, хотя у игрока нет как таковой колоды
from classes.cards.card import Card
from utilities.card_utility import random_cards


class PlayerDeck:
    def __init__(self):
        self.cards: list[Card] = []
        self.uno_said = False
        self.init_random()

    def append(self, card: Card):
        self.uno_said = False
        self.cards.append(card)

    def init_random(self):
        self.cards = random_cards(amount=2)

    def pop(self, index: int) -> Card:
        return self.cards.pop(index)

    def random_cards(self, amount: int = 1):
        self.uno_said = False
        self.cards += random_cards(amount=amount)

    def __len__(self) -> int:
        return len(self.cards)

    def __str__(self) -> str:
        return f'PlayerDeck(cards={self.cards})'

    def __repr__(self) -> str:
        return f'PlayerDeck(cards={self.cards})'
