import pygame
import pygame.freetype
import pygame_gui
from pygame.surface import Surface
from pygame.event import Event

from client.networking import Networking
from screens.abc_screen import Screen
from utilities.image_utility import load_image
from utilities.text_utility import truncate


class EndScreen(Screen):
    def __init__(self, surface: Surface, manager: pygame_gui.UIManager, networking: Networking):
        super().__init__(surface, manager, networking)
        self.next_screen = None

        total = 0
        self.win_user = None
        for user in self.networking.current_game.users:
            if len(user.deck.cards) != 0:
                total += sum([card.nominal for card in user.deck.cards])
            else:
                self.win_user = user
        if self.win_user.address == self.networking.get_user_from_game().address:
            self.networking.add_points(total)

        self.background = Surface((1280, 720))
        pygame.transform.scale(load_image('images/background.jpg'), (1280, 720), self.background)

        self.overlay = load_image('images/screens/lobby_overlay.png')

        self.name_font = pygame.freetype.Font('../assets/fonts/Roboto-Regular.ttf', 20)
        self.name_font.fgcolor = pygame.color.Color('White')
        self.points_font = pygame.freetype.Font('../assets/fonts/Roboto-Regular.ttf', 20)
        self.points_font.fgcolor = pygame.color.Color('White')
        self.points_font.bgcolor = pygame.color.Color('Black')

    def run(self, events: list[Event]) -> bool:
        self.surface.blit(self.background, dest=(0, 0))
        self.surface.blit(self.overlay, dest=(0, 0))
        for i, user in enumerate(self.networking.current_game.users):
            name = user.name
            if self.networking.get_user_from_game().address == user.address:
                name += ' (Вы)'
            if self.win_user.address == user.address:
                name += ' (Победитель)'
            self.name_font.render_to(self.surface, (345 * i + 45, 465), truncate(name, max_len=18))
            self.points_font.render_to(self.surface,
                                (345 * i + 45, 510), str(user.points))
        return self.is_running
