from typing import Any

import pygame
import pygame.freetype
import pygame_gui
from pygame.event import Event
from pygame.sprite import AbstractGroup
from pygame.surface import Surface

from classes.cards.wild_cards import WildChangeColorCard, WildGetFourCard
from classes.enums.colors import Colors
from classes.enums.directions import Directions
from client.networking import Networking
from screens.abc_screen import Screen
from screens.end_screen import EndScreen
from utilities.card_utility import card_image, random_cards
from utilities.image_utility import load_image
from utilities.text_utility import truncate


class EventGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def handle_events(self, events):
        for sprite in self.sprites():
            if hasattr(sprite, 'handle_events'):
                sprite.handle_events(events)


class UnoButton(pygame.sprite.Sprite):
    def __init__(self, x, y, networking, *groups: AbstractGroup):
        super().__init__(*groups)
        self.frames = []
        self.cut_sheet(load_image('images/uno_animation.png'), 5, 1)
        self.cur_frame = 0
        self._directions = False
        self.networking = networking
        self.rect.move(x, y)
        self.image = self.frames[self.cur_frame]

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.cur_frame != 25:
            self.cur_frame += 1
        else:
            self.cur_frame = 0
        self.image = self.frames[5 % self.cur_frame]


class UserInfo(pygame.sprite.Sprite):
    def __init__(self, x, y, networking: Networking, user_index: int, *groups: AbstractGroup):
        super().__init__(*groups)
        self.networking = networking
        self.user_index = user_index
        self.name_font = pygame.freetype.Font('../assets/fonts/Roboto-Regular.ttf', 20)
        self.name_font.fgcolor = pygame.color.Color('White')
        self.cards_amount_font = pygame.freetype.Font('../assets/fonts/Roboto-Regular.ttf', 20)
        self.cards_amount_font.fgcolor = pygame.color.Color('Black')
        # self.font.bgcolor = pygame.color.Color('Black')
        self._background = load_image('images/player_info.png')
        self._active_background = load_image('images/player_info_active.png')
        size = self._background.get_width() + 100, self._background.get_height()
        self.image = Surface(size, pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.rect = pygame.rect.Rect(x, y, *size)

    def update(self):
        self.image.fill((0, 0, 0, 0))
        if self.networking.current_game.cur_user_index == self.user_index:
            self.image.blit(self._active_background, (0, 0))
        else:
            self.image.blit(self._background, (0, 0))
        self.name_font.render_to(self.image, (5, 102),
                                 truncate(self.networking.current_game.users[self.user_index].name))
        self.cards_amount_font.render_to(self.image, (110, 102),
                                         str(len(self.networking.current_game.users[
                                                     self.user_index].deck.cards)))


class CardGiver(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, networking: Networking, *groups: AbstractGroup):
        super().__init__(*groups)
        self.networking = networking
        self._active = load_image('images/deck_active.png')
        self._non_active = load_image('images/deck.png')
        self.image = self._active
        self.rect = self.image.get_rect()
        self.is_active = False
        self.rect.x = x
        self.rect.y = y

    def handle_events(self, events):
        for event in events:
            match event.type:
                case pygame.MOUSEBUTTONDOWN:
                    if self.is_active:
                        if self.networking.is_our_move:
                            self.networking.get_card()

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self._active
            self.is_active = True
        else:
            self.is_active = False
            self.image = self._non_active


class ColorChooser(pygame.sprite.Sprite):
    def __init__(self, x, y, networking: Networking, *groups: AbstractGroup):
        super().__init__(*groups)
        self.networking = networking
        self.rect = pygame.rect.Rect(x, y, 206, 206)
        self.image = pygame.surface.Surface((206, 206), pygame.SRCALPHA, 32)
        self._active_color = None
        self._colors = {
            (0, 0): (load_image('images/color_chooser/red.png'),
                     load_image('images/color_chooser/red_active.png')),
            (1, 0): (load_image('images/color_chooser/green.png'),
                     load_image('images/color_chooser/green_active.png')),
            (0, 1): (load_image('images/color_chooser/yellow.png'),
                     load_image('images/color_chooser/yellow_active.png')),
            (1, 1): (load_image('images/color_chooser/blue.png'),
                     load_image('images/color_chooser/blue_active.png')),
        }

    def handle_events(self, events: list[Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                card = None
                if self._active_color == (0, 0):
                    card = random_cards(color=Colors.RED)[0]
                if self._active_color == (1, 0):
                    card = random_cards(color=Colors.GREEN)[0]
                if self._active_color == (0, 1):
                    card = random_cards(color=Colors.YELLOW)[0]
                if self._active_color == (1, 1):
                    card = random_cards(color=Colors.BLUE)[0]
                self.networking.throw_card(card, ignore=True)
                self.networking.current_game.next_player()

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.image.fill((0, 0, 0, 0))
        for x in range(2):
            for y in range(2):
                rect = pygame.rect.Rect(self.rect.x + x * 103, self.rect.y + y * 103, 103, 103)
                if rect.collidepoint(pygame.mouse.get_pos()):
                    self.image.blit(self._colors[(x, y)][1], dest=(x * 103, y * 103))
                    self._active_color = (x, y)
                else:
                    self.image.blit(self._colors[(x, y)][0], dest=(x * 103, y * 103))


class Cards(pygame.sprite.Sprite):
    CARD_END = pygame.event.custom_type()

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
                            self.networking.is_our_move:
                        self.networking.throw_card(self._active_card_index)
                    else:
                        pass  # TODO: play some sound when you cant throw a card
                        # (because it is not your way)

    def update(self, *args: Any, **kwargs: Any):
        deck = self.networking.current_game.users[self.user_id].deck
        self.image.fill((0, 0, 0, 0))
        try:
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
            if not deck.cards:
                raise ValueError
        except (ZeroDivisionError, ValueError):
            # this exception will happen ONLY ONCE, when somebody has 0 cards
            # i know, that is strange solution, but trust me
            # this is just prototype, hehehe
            pygame.event.post(Event(self.CARD_END))


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
    def __init__(self, networking: Networking, *groups: AbstractGroup):
        super().__init__(*groups)
        self.networking = networking
        self._clockwise = load_image('images/main_direction_clockwise.png')
        self._counterclockwise = load_image('images/main_direction_counterclockwise.png')
        self.image = self._clockwise
        self.rect = self.image.get_rect()
        self.rect.center = (640, 360)

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.networking.current_game.direction == Directions.CLOCKWISE:
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
        self.next_screen = EndScreen

        self._miscellaneous_group = EventGroup()
        DirectionSprite(self.networking, self._miscellaneous_group)

        self._all_cards = EventGroup()
        self._game_deck = pygame.sprite.Group()
        self._color_chooser = ColorChooser(540, 260, networking, self._miscellaneous_group)
        self._card_giver = CardGiver(175, 20, self.networking, self._miscellaneous_group)
        self._uno_button = UnoButton(1060, 560, self.networking, self._miscellaneous_group)
        self._player_indexes = _PLAYER_INDEXES[
            self.networking.user_id(self.networking.get_user_from_game())]

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
            'self': UserInfo(169, 533, self.networking, self._player_indexes['self'],
                             self._miscellaneous_group),
            'right': UserInfo(927, 294, self.networking, self._player_indexes['right'],
                              self._miscellaneous_group),
            'left': UserInfo(274, 170, self.networking, self._player_indexes['left'],
                             self._miscellaneous_group),
            'opposite': UserInfo(907, 41, self.networking, self._player_indexes['opposite'],
                                 self._miscellaneous_group),
        }
        self._game_cards = GameCards(self.networking, 640 - 60, 360 - 90,
                                     self._all_cards)

        self.background = load_image('images/main.png')
        self.error_font = pygame.freetype.Font('../assets/fonts/Roboto-Regular.ttf', 20)
        self.error_font.fgcolor = pygame.color.Color('White')

    def _handle_events(self, events: list[Event]):
        for event in events:
            if event.type == Cards.CARD_END:
                self.is_running = False

    def run(self, events: list[Event]) -> bool:
        self.surface.blit(self.background, dest=(0, 0))
        if (isinstance(self.networking.current_game.deck.cards[0], WildChangeColorCard) or
            isinstance(self.networking.current_game.deck.cards[0], WildGetFourCard)) and \
                self.networking.is_our_move:
            self._color_chooser.add(self._miscellaneous_group)
        else:
            self._color_chooser.remove(self._miscellaneous_group)
        self._all_cards.draw(self.surface)
        self._all_cards.update()
        self._all_cards.handle_events(events)
        self._miscellaneous_group.draw(self.surface)
        self._miscellaneous_group.update()
        self._miscellaneous_group.handle_events(events)
        self._handle_events(events)
        return self.is_running
