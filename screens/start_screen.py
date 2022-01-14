import pygame
import pygame_gui
from pygame.surface import Surface
from pygame.event import Event
import pygame.freetype
from pygame_gui.elements import UITextEntryLine, UIButton

from screens.abc_screen import Screen
from screens.main_screen import MainScreen
from utilities.utility import load_image


class StartScreen(Screen):
    def __init__(self, surface: Surface, manager: pygame_gui.UIManager):
        super().__init__(surface, manager)
        self.next_screen = MainScreen

        self.background = Surface((1280, 720))
        pygame.transform.scale(load_image('images/background.jpg'), (1280, 720), self.background)

        self.big_font = pygame.freetype.Font('./assets/fonts/Roboto-Regular.ttf', 35)
        self.big_font.fgcolor = pygame.color.Color('White')
        self.main_font = pygame.freetype.Font('./assets/fonts/Roboto-Regular.ttf', 20)
        self.main_font.fgcolor = pygame.color.Color('White')

        rect = pygame.Rect((0, 300), (250, 50))
        self._center_rect(rect)
        self.login_input = UITextEntryLine(relative_rect=rect, manager=self.manager)
        rect.y = 375
        self.password_input = UITextEntryLine(relative_rect=rect, manager=self.manager)
        rect.y = 450
        self.login_button = UIButton(relative_rect=rect, text='Войти', manager=self.manager)
        rect.y = 525
        self.register_button = UIButton(relative_rect=rect, text='Зарегистрироваться', manager=self.manager)

    def _handle_events(self, events: list[Event]):
        for event in events:
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self.is_running = False

    def _text_on_center(self, font: pygame.freetype.Font, text: str, y: int):
        text_rect = font.get_rect(text)
        self._center_rect(text_rect)
        text_rect.centery = y
        font.render_to(self.surface, text_rect, text)

    def _center_rect(self, rect: pygame.rect.Rect):
        rect.centerx = self.surface.get_width() // 2

    def run(self, events: list[Event]) -> bool:
        self.surface.blit(self.background, dest=(0, 0))
        self._text_on_center(self.big_font, 'Добро пожаловать в игру PyGameUno!', 100)
        self._text_on_center(self.main_font, 'Пожалуйста, войдите или зарегистрируйтесь, ',
                             200)
        self._text_on_center(self.main_font, 'введя свой логин и пароль и нажав на кнопки '
                                             'ниже', 220)
        self._handle_events(events)
        return self.is_running

    def __del__(self):
        self.manager.clear_and_reset()
