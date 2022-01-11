from dataclasses import dataclass

from classes.cards.card import Card


@dataclass
class NumericCard(Card):
    number: int

    def __post_init__(self):
        self.nominal = self.number
