from typing import Any

import pygame
import pygame.freetype
import pygame_gui
from pygame.event import Event
from pygame.sprite import AbstractGroup
from pygame.surface import Surface

from classes.decks.player_deck import PlayerDeck
from classes.enums.directions import Directions
from classes.game.game import Game
from client.networking import Networking
from screens.abc_screen import Screen
from utilities.image_utility import load_image


class CardsDrawer:
    def __init__(self, deck: PlayerDeck, max_width: int = 600, is_blank: bool = False):
        self.deck = deck
        self.max_width = max_width
        self.is_blank = is_blank
        self.image = Surface((self.max_width, 120))

    def draw(self) -> Surface:
        for i, card in enumerate(self.deck.cards):
            self.image.blit()
        return self.image

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
        self._game_deck = pygame.sprite.Group()

        self.background = load_image('images/main.png')
        self.error_font = pygame.freetype.Font('../assets/fonts/Roboto-Regular.ttf', 20)
        self.error_font.fgcolor = pygame.color.Color('White')

    def run(self, events: list[Event]) -> bool:
        self.surface.blit(self.background, dest=(0, 0))
        self._miscellaneous_group.draw(self.surface)
        self._miscellaneous_group.update()
        # print(self.networking.current_game.deck.cards)
        self._all_cards.draw(self.surface)
        self._all_cards.update()
        return self.is_running
