from random import choice

from pygame.color import Color
from pygame.surface import Surface

from classes.cards.card import Card
from classes.cards.numeric_card import NumericCard
from classes.enums.colors import Colors
from classes.cards.special_cards import SkipCard, ReverseCard, GetTwoCard, SpecialCard
from classes.cards.wild_cards import WildChangeColorCard, WildGetFourCard

CARDS = []

for i in range(2):
    for color in [Colors.BLUE, Colors.RED, Colors.GREEN, Colors.YELLOW]:
        # карты с номерами
        for num in range(0, 10) if i == 0 else range(1, 10):
            CARDS.append(NumericCard(color, num))
        # специальные карты
        for card in [SkipCard, ReverseCard, GetTwoCard]:
            CARDS.append(card(color))
# дикие карты
for i in range(4):
    CARDS.append(WildChangeColorCard())
    CARDS.append(WildGetFourCard())


def random_cards(amount=1) -> list[Card]:
    return [choice(CARDS) for _ in range(amount)]
