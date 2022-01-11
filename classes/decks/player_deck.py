# здесь использую то же название "колода" для удобства, хотя у игрока нет как таковой колоды
from classes.cards.card import Card


class PlayerDeck:
    def __init__(self):
        self.cards: list[Card] = []

    def append(self, card: Card):
        self.cards.append(card)
        self.cards.sort()  # намного быстрее отсортировать один раз при добавлении,
        # чем много раз при каждой отрисовки

    def pop(self, index: int) -> Card:
        return self.cards.pop(index)

    def __len__(self) -> int:
        return len(self.cards)
