import sys

import pygame
import pygame_gui

from networking import Networking
from screens.start_screen import StartScreen

FETCH_RATE = 30
SERVER_IP = "192.168.2.59"


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
size = width, height = 1280, 720

screen = pygame.display.set_mode(size)
manager = pygame_gui.UIManager(size)


def main(start_auth: tuple[str, str] | None = None):
    networking = Networking(SERVER_IP)

    pygame.display.set_caption('PyUnoGame')

    running = True
    fps = 120
    clock = pygame.time.Clock()

    current_screen = StartScreen(screen, manager, networking)

    if start_auth:
        networking.login(*start_auth)
        current_screen.is_running = False

    fetched_ticks = 0
    while running:
        if fetched_ticks == FETCH_RATE:
            fetched_ticks = 0
            networking.fetch()
        fetched_ticks += 1
        time_delta = clock.tick(fps) / 1000.0
        events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                events.append(event)
            manager.process_events(event)

        manager.update(time_delta)
        # если по итогам отрисовки экрана мы решили перейти на следующий
        if hasattr(current_screen, 'run'):
            if not current_screen.run(events):
                current_screen = current_screen.next_screen(screen, manager, networking)
                manager.clear_and_reset()
        else:
            terminate()  # будем считать, что если следующий экран не указан, то пора закрываться

        manager.draw_ui(screen)
        pygame.display.flip()
    terminate()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main((sys.argv[1], sys.argv[2]))
    else:
        main()
