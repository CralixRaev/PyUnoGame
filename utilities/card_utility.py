from random import choice

from pygame.surface import Surface

from classes.cards.card import Card
from classes.cards.numeric_card import NumericCard
from classes.cards.special_cards import SkipCard, ReverseCard, GetTwoCard
from classes.cards.wild_cards import WildChangeColorCard, WildGetFourCard
from classes.enums.colors import Colors
from classes.enums.directions import Directions

_CARD_ID = {
    SkipCard: 10,
    ReverseCard: 11,
    GetTwoCard: 12,
    WildChangeColorCard: 13,
    WildGetFourCard: 14,
}

_CARD_COLOR = {
    Colors.RED: 0,
    Colors.YELLOW: 1,
    Colors.GREEN: 2,
    Colors.BLUE: 3,
}

COLOR_CARDS = []
OTHER_CARDS = []

for i in range(2):
    for color in [Colors.BLUE, Colors.RED, Colors.GREEN, Colors.YELLOW]:
        # карты с номерами
        for num in range(0, 10) if i == 0 else range(1, 10):
            COLOR_CARDS.append(NumericCard(color, num))
        # специальные карты
        for card in [SkipCard, ReverseCard, GetTwoCard]:
            OTHER_CARDS.append(card(color))
# дикие карты
for i in range(4):
    OTHER_CARDS.append(WildChangeColorCard())
    OTHER_CARDS.append(WildGetFourCard())


def random_cards(amount=1, color=None) -> list[Card]:
    if not color:
        return [choice(COLOR_CARDS + OTHER_CARDS) for _ in range(amount)]
    else:
        return [choice([card for card in COLOR_CARDS if card.color == color]) for _ in range(amount)]


def card_image(card_set: Surface, card) -> Surface:
    if isinstance(card, NumericCard):
        image = card_set.subsurface(120 * card.number,
                                    180 * _CARD_COLOR[card.color],
                                    120, 180)
    elif isinstance(card, WildChangeColorCard):
        image = card_set.subsurface(120 * 13, 0, 120, 180)
    elif isinstance(card, WildGetFourCard):
        image = card_set.subsurface(120 * 13, 180, 120, 180)
    else:
        image = card_set.subsurface(120 * _CARD_ID[card.__class__],
                                    180 * _CARD_COLOR[card.color],
                                    120, 180)
    return image
