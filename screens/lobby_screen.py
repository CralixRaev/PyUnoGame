import pygame
import pygame.freetype
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

        self.error_font = pygame.freetype.Font('../assets/fonts/Roboto-Regular.ttf', 20)
        self.error_font.fgcolor = pygame.color.Color('White')

    def run(self, events: list[Event]) -> bool:
        self.surface.blit(self.background, dest=(0, 0))
        self.surface.blit(self.overlay, dest=(0, 0))
        for i, user in enumerate(self.networking.current_game.users):
            self.error_font.render_to(self.surface,
                                      (340 * i + 45, 465),
                                      f'{user.name} (Вы)'
                                      if self.networking.authorized_user == user else user.name)
        return self.is_running
