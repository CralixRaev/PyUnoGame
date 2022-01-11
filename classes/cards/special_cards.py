from dataclasses import dataclass

from classes.cards.card import Card


@dataclass
class SpecialCard(Card):
    def __post_init__(self):
        self.nominal = 20

    def possible_move(self, card: Card) -> bool:
        if super().possible_move(card) or card.__class__ == self.__class__:
            return True
        else:
            return False


@dataclass
class GetTwoCard(SpecialCard):
    pass


@dataclass
class ReverseCard(SpecialCard):
    pass


@dataclass
class SkipCard(SpecialCard):
    pass
