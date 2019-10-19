from functools import lru_cache
import pygame.font


@lru_cache(maxsize=None)
def hashing_point(x, y):
    return hash((x, y))


@lru_cache(maxsize=None)
def get_font(name, size, **kwargs):
    return pygame.font.SysFont(name, size, **kwargs)