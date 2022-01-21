from typing import Any

import pygame
import pygame.freetype
import pygame_gui
from pygame.event import Event
from pygame.sprite import AbstractGroup
from pygame.surface import Surface

from classes.enums.directions import Directions
from classes.game.game import Game
from client.networking import Networking
from screens.abc_screen import Screen
from utilities.card_utility import card_image
from utilities.image_utility import load_image


class EventGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def handle_events(self, events):
        for sprite in self.sprites():
            if hasattr(sprite, 'handle_events'):
                sprite.handle_events(events)


class UserInfo(pygame.sprite.Sprite):
    def __init__(self, x, y, networking: Networking, user_index: int, *groups: AbstractGroup):
        super().__init__(*groups)
        self.networking = networking
        self.user_index = user_index
        self.font = pygame.freetype.Font('../assets/fonts/Roboto-Regular.ttf', 20)
        self.font.fgcolor = pygame.color.Color('White')
        self.font.bgcolor = pygame.color.Color('Black')
        self.image = pygame.surface.Surface((200, 100), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.networking.current_game.cur_user_index == self.user_index:
            self.font.bgcolor = pygame.color.Color('BLUE')
        else:
            self.font.bgcolor = pygame.color.Color('Black')
        self.image.fill((0, 0, 0, 0))
        self.font.render_to(self.image, (0, 0),
                            self.networking.current_game.users[self.user_index].name)


class CardGiver(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, networking: Networking, *groups: AbstractGroup):
        super().__init__(*groups)
        self.networking = networking
        self.rect = pygame.rect.Rect(x, y, 150, 150)
        self.image = Surface((150, 150))
        pygame.draw.rect(self.image, (0, 0, 0), self.rect, 1)

    def handle_events(self, events):
        for event in events:
            match event.type:
                case pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(pygame.mouse.get_pos()):
                        game = self.networking.current_game
                        if game.cur_user_index == self.networking.user_id(
                                self.networking.get_user_from_game()):
                            self.networking.get_card()


class Cards(pygame.sprite.Sprite):
    def __init__(self, user_id: int, x, y, networking: Networking, *groups: AbstractGroup,
                 max_width: int = 600, is_blank: bool = True, rotation: int = 0):
        super().__init__(*groups)
        self.networking = networking
        self.user_id = user_id
        self.max_width = max_width
        self.is_blank = is_blank
        self.image = pygame.transform.rotate(
            Surface((self.max_width + 120, 180), pygame.SRCALPHA, 32), rotation)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.card_set = load_image('images/cards.png')
        self._active_card_index = -1
        self.rotation = rotation

    def handle_events(self, events):
        for event in events:
            match event.type:
                case pygame.MOUSEBUTTONDOWN:
                    if self._active_card_index >= 0 and \
                            self.networking.current_game.cur_user_index == self.user_id:
                        print(self.networking.throw_card(self._active_card_index))
                    else:
                        pass  # TODO: play some sound when you cant throw a card
                        # (cause it is not your way)

    def update(self, *args: Any, **kwargs: Any) -> None:
        deck = self.networking.current_game.users[self.user_id].deck
        self.networking.get_user_from_game()
        self.image.fill((0, 0, 0, 0))
        if not self.is_blank:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # this is the most elegant solution what i can think of (and very fast solution too)
            if self.rect.collidepoint(mouse_x, mouse_y):
                # coordinates regarding our sprite
                mouse_x -= self.rect.x
                self._active_card_index = int(mouse_x // (self.max_width / len(deck.cards)))
            else:
                self._active_card_index = -1
        for i, card in enumerate(deck.cards):
            image = pygame.transform.rotate(
                card_image(self.card_set, card) if not self.is_blank else load_image(
                    'images/blank_card.png'), self.rotation)
            x, y = (self.max_width / len(deck.cards)) * i, 60 if not self.is_blank else 0
            if not self.is_blank and self._active_card_index == i:
                y -= 60
            if self.rotation // 90 % 2 != 0:
                x, y = y, x
            self.image.blit(image, (x, y))


class GameCards(pygame.sprite.Sprite):
    def __init__(self, networking: Networking, x, y, *groups: AbstractGroup):
        super().__init__(*groups)
        self.networking = networking
        self.rect = pygame.rect.Rect(x, y, 120, 180)
        self.card_set = load_image('images/cards.png')
        self.image = self.card_set

    def update(self, *args: Any, **kwargs: Any) -> None:
        deck = self.networking.current_game.deck
        # TODO: draw multiple cards, with various rotation and another pretty things
        self.image = card_image(self.card_set, deck.cards[0])


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

        self._miscellaneous_group = EventGroup()
        DirectionSprite(self.networking.current_game, self._miscellaneous_group)

        self._all_cards = EventGroup()
        self._game_deck = pygame.sprite.Group()

        self._card_giver = CardGiver(100, 100, self.networking, self._miscellaneous_group)

        self._player_indexes = _PLAYER_INDEXES[self.networking.current_game.users.index(
            self.networking.get_user_from_game())]

        self._cards = {
            'self': Cards(self._player_indexes['self'], (1280 / 2) - 300, 600, self.networking,
                          self._all_cards, is_blank=False),
            'right': Cards(self._player_indexes['right'], 1160, 160, self.networking,
                           self._all_cards, rotation=270, max_width=320),
            'left': Cards(self._player_indexes['left'], -60, 160, self.networking, self._all_cards,
                          rotation=90, max_width=320),
            'opposite': Cards(self._player_indexes['opposite'], (1280 / 2) - 195, -60,
                              self.networking, self._all_cards, rotation=180, max_width=320)
        }
        self._users_names = {
            'self': UserInfo(300, 500, self.networking, self._player_indexes['self'],
                             self._miscellaneous_group),
            'right': UserInfo(1000, 120, self.networking, self._player_indexes['right'],
                              self._miscellaneous_group),
            'left': UserInfo(60, 120, self.networking, self._player_indexes['left'],
                             self._miscellaneous_group),
            'opposite': UserInfo(300, 50, self.networking, self._player_indexes['opposite'],
                                 self._miscellaneous_group),
        }
        self._game_cards = GameCards(self.networking, 640 - 60, 360 - 90,
                                     self._all_cards)

        self.background = load_image('images/main.png')
        self.error_font = pygame.freetype.Font('../assets/fonts/Roboto-Regular.ttf', 20)
        self.error_font.fgcolor = pygame.color.Color('White')

    def _handle_events(self, events: list[Event]):
        pass

    def run(self, events: list[Event]) -> bool:
        self.surface.blit(self.background, dest=(0, 0))
        self._all_cards.draw(self.surface)
        self._all_cards.update()
        self._all_cards.handle_events(events)
        self._miscellaneous_group.draw(self.surface)
        self._miscellaneous_group.update()
        self._miscellaneous_group.handle_events(events)
        self._handle_events(events)
        return self.is_running
