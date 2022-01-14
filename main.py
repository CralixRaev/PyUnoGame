import os
import random
import pygame


pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)


pygame.display.set_caption('PyUnoGame')
running = True
fps = 120
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
