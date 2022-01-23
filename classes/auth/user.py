from dataclasses import dataclass

from classes.decks.player_deck import PlayerDeck


@dataclass
class User:
    id: int
    name: str
    address: tuple[str, int] = None
    deck: PlayerDeck = None
    points: int = 0
    uno_said: bool = False

    def __post_init__(self):
        self.deck = PlayerDeck()
