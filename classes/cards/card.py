from __future__ import annotations  # вроде 3.10, а эту хрень так и не добавили в импорт по умолчанию

from dataclasses import dataclass, field

from classes.enums.colors import Colors


@dataclass
class Card:
    color: Colors
    nominal: int = field(init=False)

    def possible_move(self, card: Card) -> bool:
        if card.color == self.color:
            return True
        else:
            return False

    @staticmethod
    def move(game):
        pass
