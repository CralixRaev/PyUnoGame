from dataclasses import dataclass, field

from classes.cards.card import Card
from classes.enums.colors import Colors
from utilities.player_utility import next_player_index


@dataclass
class WildCard(Card):
    color: Colors = field(init=False, default=Colors.BLACK)

    def __post_init__(self):
        self.nominal = 50

    def possible_move(self, card: Card) -> bool:
        return True  # дикой картой мы можем сходить всегда


@dataclass
class WildGetFourCard(WildCard):
    @staticmethod
    def move(game):
        game.users[next_player_index(game.cur_user_index, game.direction)].deck.random_cards(4)


@dataclass
class WildChangeColorCard(WildCard):
    pass
