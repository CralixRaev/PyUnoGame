import pygame
import pygame.freetype
import pygame_gui
from pygame.surface import Surface
from pygame.event import Event

from classes.cards.card import Card
from classes.cards.numeric_card import NumericCard
from classes.cards.special_cards import SkipCard, GetTwoCard, ReverseCard
from classes.cards.wild_cards import WildChangeColorCard, WildGetFourCard
from classes.decks.player_deck import PlayerDeck
from classes.enums.colors import Colors
from client.networking import Networking
from screens.abc_screen import Screen
from utilities.image_utility import load_image


class CardSprite(pygame.sprite.Sprite):
    def __init__(self, represent_card: Card, rect: pygame.Rect, group):
        super().__init__(group)
        self.cards = load_image("images/cards.png")
        if represent_card.__class__ == NumericCard:
            self.image = self.cards.subsurface(represent_card.number * 120, 0, 120, 180)
        elif represent_card.__class__ == SkipCard:
            self.image = self.cards.subsurface(10 * 120, 0, 120, 180)
        elif represent_card.__class__ == ReverseCard:
            self.image = self.cards.subsurface(11 * 120, 0, 120, 180)
        elif represent_card.__class__ == GetTwoCard:
            self.image = self.cards.subsurface(12 * 120, 0, 120, 180)
        elif represent_card.__class__ == WildChangeColorCard:
            self.image = self.cards.subsurface(13 * 120, 0, 120, 180)
        elif represent_card.__class__ == WildGetFourCard:
            self.image = self.cards.subsurface(14 * 120, 0, 120, 180)
        img_copy = self.image.copy()
        pygame.transform.threshold(self.image, img_copy, pygame.color.Color(255, 0, 0),
                                   set_color=represent_card.color.value, inverse_set=True,
                                   threshold=100)
        self.rect = rect

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.image, self.rect)


class MainScreen(Screen):
    def __init__(self, surface: Surface, manager: pygame_gui.UIManager, networking: Networking):
        super().__init__(surface, manager, networking)
        self.next_screen = None
        self.background = load_image('images/main.jpg')
        self.cards = []
        self.player_group = pygame.sprite.Group()
        for i, card in enumerate(self.networking.get_user_from_game().deck.cards):
            self.cards.append(CardSprite(card, pygame.rect.Rect((80 * i + 200, 625, 0, 0)),
                                         self.player_group))
        self.error_font = pygame.freetype.Font('../assets/fonts/Roboto-Regular.ttf', 20)
        self.error_font.fgcolor = pygame.color.Color('White')

    def run(self, events: list[Event]) -> bool:
        self.surface.blit(self.background, dest=(0, 0))
        self.player_group.draw(self.surface)
        return self.is_running
