from typing import Any, Union, Sequence

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


class SelfCardsGroup(pygame.sprite.Group):
    def __init__(self, *sprites: Union[pygame.sprite.Sprite, Sequence[pygame.sprite.Sprite]]):
        super().__init__(*sprites)

    def handle_events(self, events: list[Event]):
        for sprite in self.sprites():
            if hasattr(sprite, 'handle_events'):
                sprite.handle_events(events)


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

    def __init__(self, represent_card: Card, cardset: pygame.surface.Surface, x: int, y: int,
                 *groups: AbstractGroup, is_blank: bool = False,
                 rotation: int = 0):
        super().__init__(*groups)
        self.represent_card = represent_card
        if not is_blank:
            if represent_card.__class__ == NumericCard:
                self.image = cardset.subsurface(120 * represent_card.number,
                                                180 * CardSprite.card_color[represent_card.color],
                                                120, 180)
            elif represent_card.__class__ == WildChangeColorCard:
                self.image = cardset.subsurface(120 * 13, 0, 120, 180)
            elif represent_card.__class__ == WildGetFourCard:
                self.image = cardset.subsurface(120 * 13, 180, 120, 180)
            else:
                self.image = cardset.subsurface(120 * CardSprite.card_id[represent_card.__class__],
                                                180 * CardSprite.card_color[represent_card.color],
                                                120, 180)
        else:
            self.image = load_image('images/blank_card.png')
        self.is_blank = is_blank
        self.rect = pygame.Rect(x, y, *self.image.get_size())
        self.image = pygame.transform.rotate(self.image, rotation)
        self._active = self.rect.copy()
        self._non_active = self.rect.copy()
        self._active.y -= 60

    def handle_events(self, events: list[Event]):
        for event in events:
            pass

    def update(self, *args: Any, **kwargs: Any) -> None:
        if not self.is_blank:
            if self.rect.collidepoint(*pygame.mouse.get_pos()):
                self.rect = self._active
            else:
                self.rect = self._non_active


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

        self.cardset = load_image('images/cards.png')

        self._all_cards = pygame.sprite.Group()
        self._game_deck = pygame.sprite.Group()
        self._player_groups = {'self': SelfCardsGroup(),
                               'right': pygame.sprite.Group(),
                               'left': pygame.sprite.Group(),
                               'opposite': pygame.sprite.Group()}

        self.background = load_image('images/main.png')
        self.error_font = pygame.freetype.Font('../assets/fonts/Roboto-Regular.ttf', 20)
        self.error_font.fgcolor = pygame.color.Color('White')

    def _draw_cards(self, player: str, cards: list[Card], max_width: int = 500):
        for i, card in enumerate(cards):
            coords = (0, 0)
            rotation = 0
            match player:
                case 'self':
                    coords = (max_width / len(cards) * i, 620)
                case 'right':
                    coords = (1180, max_width / len(cards))
                    rotation = 270
                case 'left':
                    coords = (100, max_width / len(cards))
                    rotation = 90
                case 'opposite':
                    coords = (max_width / len(cards), 100)
                    rotation = 180
            CardSprite(card, self.cardset, *coords, self._all_cards, self._player_groups[player],
                       is_blank=True if player != 'self' else False, rotation=rotation)

    def _draw_players_cards(self):
        users = self.networking.current_game.users
        our_index = users.index(self.networking.get_user_from_game())
        other_players = _PLAYER_INDEXES[our_index]
        for key, group in self._player_groups.items():
            group.empty()
            self._draw_cards(key, users[other_players[key]].deck.cards)

    def run(self, events: list[Event]) -> bool:
        self.surface.blit(self.background, (0, 0))
        self._draw_players_cards()
        self._miscellaneous_group.draw(self.surface)
        self._miscellaneous_group.update()
        self._all_cards.draw(self.surface)
        self._all_cards.update()
        return self.is_running
