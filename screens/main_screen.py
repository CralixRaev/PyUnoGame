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
from utilities.card_utility import card_image
from utilities.image_utility import load_image


class Cards(pygame.sprite.Sprite):
    def __init__(self, deck: PlayerDeck, x, y, *groups: AbstractGroup, max_width: int = 600,
                 is_blank: bool = False):
        super().__init__(*groups)
        self.deck = deck
        self.max_width = max_width
        self.is_blank = is_blank
        self.rect = pygame.rect.Rect(x, y - 60, self.max_width, 240)
        self.image = Surface((self.max_width + 120, 180), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.card_set = load_image('images/cards.png')

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.image.fill((0, 0, 0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # this is the most elegant solution what i can think of (and very fast solution too)
        if self.rect.collidepoint(mouse_x, mouse_y):
            # coordinates regarding our sprite
            mouse_x -= self.rect.x
            card_index = mouse_x // (self.max_width / len(self.deck.cards))
        else:
            card_index = -1
        for i, card in enumerate(self.deck.cards):
            x, y = (self.max_width / len(self.deck.cards)) * i, 60
            if card_index == i:
                y -= 60
            self.image.blit(card_image(self.card_set, card), (x, y))


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

        self.card_drawer = Cards(self.networking.get_user_from_game().deck, (1280 / 2) - 300,
                                 600, self._all_cards)

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
