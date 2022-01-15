import pygame


def center_rect(surface, rect: pygame.rect.Rect):
    rect.centerx = surface.get_width() // 2


def text_on_center(surface: pygame.surface.Surface, font: pygame.freetype.Font, text: str, y: int):
    text_rect = font.get_rect(text)
    center_rect(surface, text_rect)
    text_rect.centery = y
    font.render_to(surface, text_rect, text)
