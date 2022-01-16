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


class MainScreen(Screen):
    def __init__(self, surface: Surface, manager: pygame_gui.UIManager, networking: Networking):
        super().__init__(surface, manager, networking)
        self.next_screen = None
        self.background = load_image('images/main.png')
        self.error_font = pygame.freetype.Font('../assets/fonts/Roboto-Regular.ttf', 20)
        self.error_font.fgcolor = pygame.color.Color('White')

    def run(self, events: list[Event]) -> bool:
        self.surface.blit(self.background, dest=(0, 0))
        print()
        return self.is_running
