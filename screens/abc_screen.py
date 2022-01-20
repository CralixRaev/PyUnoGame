from __future__ import annotations

import pygame_gui
from pygame.surface import Surface
from pygame.event import Event

from client.networking import Networking


class Screen:
    def __init__(self, surface: Surface, manager: pygame_gui.UIManager, networking: Networking):
        self.surface = surface
        self.manager = manager
        self.is_running = True
        self.next_screen = None
        self.networking = networking

    def _handle_events(self, events: list[Event]):
        for event in events:
            pass

    def run(self, events: list[Event]) -> bool:
        pass
