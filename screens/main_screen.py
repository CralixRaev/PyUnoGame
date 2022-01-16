from typing import Any

import pygame
import pygame.freetype
import pygame_gui
from pygame.event import Event
from pygame.sprite import AbstractGroup
from pygame.surface import Surface

from classes.cards.card import Card
from classes.cards.numeric_card import NumericCard
from classes.cards.special_cards import SkipCard, ReverseCard, GetTwoCard
from classes.cards.wild_cards import WildChangeColorCard, WildGetFourCard
from classes.enums.colors import Colors
from classes.enums.directions import Directions
from classes.game.game import Game
from client.networking import Networking
from screens.abc_screen import Screen
from utilities.image_utility import load_image


class CardSprite(pygame.sprite.Sprite):
    card_id = {
        SkipCard: 10,
        ReverseCard: 11,
        GetTwoCard: 12,
        WildChangeColorCard: 13,
        WildGetFourCard: 14,
    }

    card_color = {
        Colors.RED: 0,
        Colors.YELLOW: 1,
        Colors.GREEN: 2,
        Colors.BLUE: 3,
    }

    def __init__(self, represent_card: Card, cards: pygame.surface.Surface, x: int, y: int, *groups: AbstractGroup):
        super().__init__(*groups)
        if represent_card.__class__ == NumericCard:
            self.image = cards.subsurface(120 * represent_card.number,
                                          180 * CardSprite.card_color[represent_card.color],
                                          120, 180)
        elif represent_card.__class__ == WildChangeColorCard:
            self.image = cards.subsurface(120 * 14, 0, 120, 180)
        elif represent_card.__class__ == WildGetFourCard:
            self.image = cards.subsurface(120 * 14, 180, 120, 180)
        else:
            self.image = cards.subsurface(120 * CardSprite.card_id[represent_card.__class__],
                                          180 * CardSprite.card_color[represent_card.color],
                                          120, 180)

        self.rect = pygame.Rect(x, y, 0, 0)

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass


class DirectionSprite(pygame.sprite.Sprite):
    def __init__(self, game: Game, *groups: AbstractGroup):
        super().__init__(*groups)
        self._clockwise = load_image('images/main_direction_clockwise.png')
        self._counterclockwise = load_image('images/main_direction_clockwise.png')
        self.image = self._clockwise
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.center = (640, 360)

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.game.direction == Directions.CLOCKWISE:
            self.image = self._clockwise
        else:
            self.image = self._counterclockwise


class MainScreen(Screen):
    def __init__(self, surface: Surface, manager: pygame_gui.UIManager, networking: Networking):
        super().__init__(surface, manager, networking)
        self.next_screen = None

        # self._miscellaneous_group = pygame.sprite.Group()
        # DirectionSprite(self.networking.current_game, self._miscellaneous_group)

        self._all_cards = pygame.sprite.Group()

        cards = load_image('images/cards.png')

        for i, card in enumerate(self.networking.get_user_from_game().deck.cards):
            print(card)
            CardSprite(card, cards, 80 * i, 600, self._all_cards)

        self._player_groups = {'self': pygame.sprite.Group(),
                               'right': pygame.sprite.Group(),
                               'left': pygame.sprite.Group(),
                               'opposite': pygame.sprite.Group()}

        self.background = load_image('images/main.png')
        self.error_font = pygame.freetype.Font('../assets/fonts/Roboto-Regular.ttf', 20)
        self.error_font.fgcolor = pygame.color.Color('White')

    def run(self, events: list[Event]) -> bool:
        self.surface.blit(self.background, dest=(0, 0))
        # self._miscellaneous_group.draw(self.surface)
        # self._miscellaneous_group.update()

        self._all_cards.draw(self.surface)
        self._all_cards.update()
        return self.is_running
