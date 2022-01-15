import sys
import pygame
import pygame_gui
from networking import Networking
from screens.start_screen import StartScreen


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
size = width, height = 1280, 720

screen = pygame.display.set_mode(size)
manager = pygame_gui.UIManager(size)
networking = Networking("192.168.2.59")

pygame.display.set_caption('PyUnoGame')

running = True
fps = 120
clock = pygame.time.Clock()

current_screen = StartScreen(screen, manager, networking)

while running:
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
    else:
        terminate()  # будем считать, что если следующий экран не указан, то пора закрываться

    manager.draw_ui(screen)
    pygame.display.flip()
terminate()
