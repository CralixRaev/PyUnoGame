from dataclasses import dataclass

from classes.cards.card import Card


@dataclass
class NumericCard(Card):
    number: int

    def __post_init__(self):
        self.nominal = self.number

    def possible_move(self, card: Card) -> bool:
        # именно тут мы нарушим все аннотации типов, ведь это самый настоящий костыль
        if super().possible_move(card) or (hasattr(card, 'number') and card.number == self.number):
            return True
        else:
            return False
