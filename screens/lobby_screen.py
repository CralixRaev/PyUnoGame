import pygame
import pygame_gui
from pygame.surface import Surface
from pygame.event import Event

from client.networking import Networking
from screens.abc_screen import Screen
from screens.main_screen import MainScreen
from utilities.utility import load_image


class LobbyScreen(Screen):
    def __init__(self, surface: Surface, manager: pygame_gui.UIManager, networking: Networking):
        super().__init__(surface, manager, networking)
        self.next_screen = None

        self.background = Surface((1280, 720))
        pygame.transform.scale(load_image('images/background.jpg'), (1280, 720), self.background)

        self.overlay = load_image('images/screens/lobby_overlay.png')

    def run(self, events: list[Event]) -> bool:
        self.surface.blit(self.background, dest=(0, 0))
        self.surface.blit(self.overlay, dest=(0, 0))
        print(self.networking.current_game)
        return self.is_running
