import pygame
import pygame.freetype
import pygame_gui
from pygame.event import Event
from pygame.surface import Surface
from pygame_gui.elements import UITextEntryLine, UIButton

from client.networking import Networking
from screens.abc_screen import Screen
from screens.lobby_screen import LobbyScreen
from utilities.text_utility import text_on_center, center_rect
from utilities.image_utility import load_image


class StartScreen(Screen):
    def __init__(self, surface: Surface, manager: pygame_gui.UIManager, networking: Networking):
        super().__init__(surface, manager, networking)
        self.next_screen = LobbyScreen

        self.background = Surface((1280, 720))
        pygame.transform.scale(load_image('images/background.jpg'), (1280, 720), self.background)

        self.overlay = load_image('images/screens/start_overlay.png')

        self.error_font = pygame.freetype.Font('../assets/fonts/Roboto-Regular.ttf', 20)
        self.error_font.fgcolor = pygame.color.Color('Red')
        self.error_font.bgcolor = pygame.color.Color('Black')

        rect = pygame.Rect((0, 300), (250, 50))
        center_rect(self.surface, rect)
        self.login_input = UITextEntryLine(relative_rect=rect, manager=self.manager)
        rect.y = 375
        self.password_input = UITextEntryLine(relative_rect=rect, manager=self.manager)
        self.password_input.set_text_hidden()
        rect.y = 450
        self.login_button = UIButton(relative_rect=rect, text='Войти', manager=self.manager)
        rect.y = 525
        self.register_button = UIButton(relative_rect=rect, text='Зарегистрироваться',
                                        manager=self.manager)

        self.error_message = None

    def _handle_events(self, events: list[Event]):
        for event in events:
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                login, password = self.login_input.text, self.password_input.text
                try:
                    if not login or not password:
                        raise ValueError("Нельзя войти или зарегистрировать "
                                         "пользователя с пустым логином/паролем")
                    match event.ui_element:
                        case self.login_button:
                            self.networking.login(login, password)
                        case self.register_button:
                            self.networking.register(login, password)
                    self.is_running = False
                except Exception as e:
                    self.error_message = e
                # self.is_running = False

    def run(self, events: list[Event]) -> bool:
        self.surface.blit(self.background, dest=(0, 0))
        self.surface.blit(self.overlay, dest=(0, 0))
        if self.error_message:
            text_on_center(self.surface, self.error_font, f"Произошла ошибка: {self.error_message}",
                            650)
        self._handle_events(events)
        return self.is_running

