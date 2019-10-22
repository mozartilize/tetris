import pygame
from .helpers import get_font
from .consts import *


class GameGraphic:
    def __init__(self, surface, grid):
        self.surface = surface
        self.score_rect = None
        self.current_shape_rects = None
        self.grid = grid

    def draw_bg(self):
        self.surface.fill(BG_COLOR)
        pygame.display.update()

    def draw_title(self):
        font = get_font("comicsans", 60)
        label = font.render("Tetris", 1, TEXT_COLOR)

        rect = self.surface.blit(
            label,
            (top_left_x + play_width / 2 - (label.get_width() / 2), 30)
        )
        pygame.display.update(rect)

    def draw_highest_score(self, score):
        font = get_font("comicsans", 30)
        label = font.render("High Score: " + score, 1, TEXT_COLOR)

        sx = top_left_x - 200
        sy = top_left_y + 200

        rect = self.surface.blit(label, (sx + 20, sy + 160))
        pygame.display.update(rect)

    def draw_score(self, score):
        font = get_font("comicsans", 30)
        label = font.render("Score: " + str(score), 1, TEXT_COLOR)

        sx = top_left_x + play_width + 50
        sy = top_left_y + play_height / 2 - 100

        if self.score_rect:
            reset_rect = self.surface.fill(BG_COLOR, self.score_rect)
        else:
            reset_rect = None

        self.score_rect = self.surface.blit(label, (sx + 20, sy + 160))
        pygame.display.update([reset_rect, self.score_rect])

    def draw_next_shape_text(self):
        font = get_font("comicsans", 30)
        label = font.render("Next Shape", 1, TEXT_COLOR)
        sx = top_left_x + play_width + 50
        sy = top_left_y + play_height / 2 - 100
        rect = self.surface.blit(label, (sx + 10, sy - 30))
        pygame.display.update(rect)

    def draw_next_shape(self, shape):
        sx = top_left_x + play_width + 50
        sy = top_left_y + play_height / 2 - 100

        def generate_next_shape_rects():
            for i, line in enumerate(shape.shape.shape):
                for j, column in enumerate(list(line)):
                    if column == "0":
                        yield pygame.draw.rect(
                            self.surface,
                            shape.color,
                            (
                                sx + j * block_size,
                                sy + i * block_size,
                                block_size,
                                block_size
                            ),
                            0,
                        )

        def generate_rects():
            if self.current_shape_rects is not None:
                for rect in self.current_shape_rects:
                    yield self.surface.fill(BG_COLOR, rect)
            yield from generate_next_shape_rects()

        pygame.display.update(list(generate_rects()))

        self.current_shape_rects = generate_next_shape_rects()

    def draw_grid(self):
        sx = top_left_x
        sy = top_left_y

        def generate_rects():
            yield self.surface.fill(
                BG_COLOR,
                (top_left_x, top_left_y, play_width, play_height)
            )
            yield pygame.draw.rect(
                self.surface,
                (255, 0, 0),
                (top_left_x, top_left_y, play_width, play_height),
                5
            )
            for i in range(self.grid.height):
                for j in range(self.grid.width):
                    yield pygame.draw.rect(
                        self.surface,
                        self.grid[i][j],
                        (
                            top_left_x + j * block_size,
                            top_left_y + i * block_size,
                            block_size,
                            block_size,
                        ),
                        0,
                    )
                    yield pygame.draw.line(
                        self.surface,
                        (128, 128, 128),
                        (sx + j * block_size, sy),
                        (sx + j * block_size, sy + play_height),
                    )
                yield pygame.draw.line(
                    self.surface,
                    (128, 128, 128),
                    (sx, sy + i * block_size),
                    (sx + play_width, sy + i * block_size),
                )            
        
        pygame.display.update(list(generate_rects()))

    def draw(self, next_shape, highest_score, score):
        self.draw_bg()
        self.draw_title()
        self.draw_highest_score(highest_score)
        self.draw_score(score)
        self.draw_next_shape_text()
        self.draw_next_shape(next_shape)
        self.draw_grid()