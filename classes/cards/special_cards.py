from dataclasses import dataclass

from classes.cards.card import Card


@dataclass
class SpecialCard(Card):
    def __post_init__(self):
        self.nominal = 20


@dataclass
class GetTwoCard(SpecialCard):
    pass


@dataclass
class ReverseCard(SpecialCard):
    pass


@dataclass
class SkipCard(SpecialCard):
    pass
