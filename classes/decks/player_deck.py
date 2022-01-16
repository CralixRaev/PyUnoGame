# здесь использую то же название "колода" для удобства, хотя у игрока нет как таковой колоды
from classes.cards.card import Card
from utilities.card_utility import random_cards


class PlayerDeck:
    def __init__(self):
        self.cards: list[Card] = []
        self.init_random()

    def append(self, card: Card):
        self.cards.append(card)
        self.cards.sort()  # намного быстрее отсортировать один раз при добавлении,
        # чем много раз при каждой отрисовки

    def init_random(self):
        self.cards = random_cards(amount=7)

    def pop(self, index: int) -> Card:
        return self.cards.pop(index)

    def __len__(self) -> int:
        return len(self.cards)

    def __str__(self) -> str:
        return f'PlayerDeck(cards={self.cards})'

    def __repr__(self) -> str:
        return f'PlayerDeck(cards={self.cards})'
