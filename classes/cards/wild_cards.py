from dataclasses import dataclass, field

from classes.cards.card import Card
from classes.enums.colors import Colors


@dataclass
class WildCard(Card):
    color: Colors = field(init=False, default=Colors.BLACK)

    def __post_init__(self):
        self.nominal = 50

    def possible_move(self, card: Card) -> bool:
        return True  # дикой картой мы можем сходить всегда


@dataclass
class WildGetFourCard(WildCard):
    pass


@dataclass
class WildChangeColorCard(WildCard):
    pass
