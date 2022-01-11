from dataclasses import dataclass, field

from classes.enums.colors import Colors


@dataclass
class Card:
    color: Colors
    nominal: int = field(init=False)
