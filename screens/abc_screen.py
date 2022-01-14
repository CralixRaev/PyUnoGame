from __future__ import annotations

import pygame_gui
from pygame.surface import Surface
from pygame.event import Event


class Screen:
    def __init__(self, surface: Surface, manager: pygame_gui.UIManager):
        self.surface = surface
        self.manager = manager
        self.is_running = True
        self.next_screen = None

    def run(self, events: list[Event]) -> bool:
        pass
