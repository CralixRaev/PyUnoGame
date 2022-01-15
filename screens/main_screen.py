import pygame
import pygame_gui
from pygame.surface import Surface
from pygame.event import Event

from screens.abc_screen import Screen


class MainScreen(Screen):
    def __init__(self, surface: Surface, manager: pygame_gui.UIManager):
        super().__init__(surface, manager)

    def run(self, events: list[Event]) -> bool:
        self.surface.fill(pygame.Color('RED'))
        return self.is_running