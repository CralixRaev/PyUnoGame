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

    def __init__(self, represent_card: Card, cards: pygame.surface.Surface, x: int, y: int,
                 *groups: AbstractGroup, is_blank: bool = False, rotation: int = 0):
        super().__init__(*groups)
        if not is_blank:
            if represent_card.__class__ == NumericCard:
                self.image = cards.subsurface(120 * represent_card.number,
                                              180 * CardSprite.card_color[represent_card.color],
                                              120, 180)
            elif represent_card.__class__ == WildChangeColorCard:
                self.image = cards.subsurface(120 * 13, 0, 120, 180)
            elif represent_card.__class__ == WildGetFourCard:
                self.image = cards.subsurface(120 * 14, 180, 120, 180)
            else:
                self.image = cards.subsurface(120 * CardSprite.card_id[represent_card.__class__],
                                              180 * CardSprite.card_color[represent_card.color],
                                              120, 180)
        else:
            self.image = load_image('images/blank_card.png')
            self.image = pygame.transform.scale(self.image, (120, 180))  # TODO: pre-resize a picture
            # pygame image scaling is such a shit

        self.rect = pygame.Rect(x, y, 0, 0)
        pygame.transform.rotate(self.image, rotation)

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


_PLAYER_INDEXES = {
    0: {
        'self': 0,
        'right': 3,
        'left': 1,
        'opposite': 2
    },
    1: {
        'self': 1,
        'right': 0,
        'left': 2,
        'opposite': 3
    },
    2: {
        'self': 2,
        'right': 1,
        'left': 3,
        'opposite': 0
    },
    3: {
        'self': 3,
        'right': 2,
        'left': 0,
        'opposite': 1
    },
}


class MainScreen(Screen):
    def __init__(self, surface: Surface, manager: pygame_gui.UIManager, networking: Networking):
        super().__init__(surface, manager, networking)
        self.next_screen = None

        self._miscellaneous_group = pygame.sprite.Group()
        DirectionSprite(self.networking.current_game, self._miscellaneous_group)

        self._all_cards = pygame.sprite.Group()

        cards = load_image('images/cards.png')

        self._player_groups = {'self': pygame.sprite.Group(),
                               'right': pygame.sprite.Group(),
                               'left': pygame.sprite.Group(),
                               'opposite': pygame.sprite.Group()}
        indexes = _PLAYER_INDEXES[
            self.networking.current_game.users.index(networking.get_user_from_game())]

        for key, value in self._player_groups.items():
            for i, card in enumerate(self.networking.current_game.users[indexes[key]].deck.cards):
                coordinates = {
                    'self': ((80 * i, 600), 0),
                    'right': ((600, 80 * i), 90),
                    'left': ((100, 80 * i), 270),
                    'opposite': ((80 * i, 100), 180),
                }
                CardSprite(card, cards, coordinates[key][0][0], coordinates[key][0][1],
                           self._all_cards, self._player_groups[key],
                           is_blank=True if key != 'self' else False, rotation=coordinates[key][1])

        self.background = load_image('images/main.png')
        self.error_font = pygame.freetype.Font('../assets/fonts/Roboto-Regular.ttf', 20)
        self.error_font.fgcolor = pygame.color.Color('White')

    def run(self, events: list[Event]) -> bool:
        self.surface.blit(self.background, dest=(0, 0))
        self._miscellaneous_group.draw(self.surface)
        self._miscellaneous_group.update()

        self._all_cards.draw(self.surface)
        self._all_cards.update()
        return self.is_running
