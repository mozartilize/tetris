import sys
import pygame

from .grid import TetrisGrid, GriddedShape, Point
from .shape import Shape
from .graphic import GameGraphic
from .helpers import get_font
from .consts import *


def valid_space(shape, grid):
    return not any(
        p not in grid.available_points and p.y > -1 for p in shape.positions
    )


def get_shape(grid_width):
    return GriddedShape(Point(grid_width // 2, 0), Shape.new_shape())


def draw_text_middle(surface, text, size, color):
    font = get_font("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(
        label,
        (
            top_left_x + play_width / 2 - (label.get_width() / 2),
            top_left_y + play_height / 2 - label.get_height() / 2,
        ),
    )


def clear_rows(grid, locked):
    inc = 0
    for y in range(grid.height - 1, -1, -1):
        row = grid[y]
        if (0, 0, 0) not in row:
            inc += 1
            ind = y
            for x in range(grid.width):
                try:
                    del locked[Point(x, y)]
                except KeyError:
                    continue

    if inc > 0:
        for point in sorted(list(locked), key=lambda point: point.y)[::-1]:
            if point.y < ind:
                newpoint = Point(point.x, point.y + inc)
                locked[newpoint] = locked.pop(point)

    return inc


def update_score(nscore):
    score = max_score()

    with open("scores.txt", "w") as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    with open("scores.txt", "r") as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


def run(win):  # *
    last_score = max_score()
    locked_points = {}

    running = True
    current_piece = get_shape(GRID_WIDTH)
    next_piece = get_shape(GRID_WIDTH)
    clock = pygame.time.Clock()
    fall_time1 = 0
    one_point_fall_time = 0.27
    # level_time = 0
    score = 0

    grid = TetrisGrid(GRID_WIDTH, GRID_HEIGHT, locked_points)
    graphic = GameGraphic(win, grid)
    graphic.draw(next_piece, last_score, score)
    while running:
        grid.update(locked_points)  # reset grid

        fall_time1 += clock.get_rawtime()
        # level_time += clock.get_rawtime()
        clock.tick()

        # if level_time / 1000 > 5:
        #     level_time = 0
        #     if level_time > 0.12:
        #         level_time -= 0.005

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.go_left(1)
                    if not valid_space(current_piece, grid):
                        current_piece.go_right(1)
                if event.key == pygame.K_RIGHT:
                    current_piece.go_right(1)
                    if not valid_space(current_piece, grid):
                        current_piece.go_left(1)
                if event.key == pygame.K_DOWN:
                    current_piece.go_down(1)
                    if not valid_space(current_piece, grid):
                        current_piece.go_up(1)
                if event.key == pygame.K_UP:
                    current_piece.shape.rotate_right()
                    if not valid_space(current_piece, grid):
                        current_piece.shape.rotate_left()

        # 30 pixels per 0.27 secs
        if fall_time1 / 1000 > one_point_fall_time:
            fall_time1 = 0
            current_piece.go_down(1)
            if not valid_space(current_piece, grid) \
                    and current_piece.point.y > 0:
                current_piece.go_up(1)

                for point in current_piece.positions:
                    locked_points[point] = current_piece.color
                grid.update(locked_points, True)                
                earn_score = clear_rows(grid, locked_points) * 10
                if earn_score > 0:
                    score += earn_score
                    graphic.draw_score(score)

                if grid.check_lost():
                    draw_text_middle(win, "YOU LOST!", 80, (255, 255, 255))
                    pygame.display.update()
                    pygame.time.delay(1500)
                    running = False
                    update_score(score)
                    pygame.event.clear()                
                else:
                    current_piece = next_piece
                    next_piece = get_shape(grid.width)
                    graphic.draw_next_shape(next_piece)
        tmp_points = dict(locked_points)
        for point in current_piece.positions:
            if point.y > -1:
                tmp_points[point] = current_piece.color
        grid.update(tmp_points)

        graphic.draw_grid()


def draw_main_menu(win):
    win.fill((0, 0, 0))
    draw_text_middle(win, "Press Any Key To Play", 60, (255, 255, 255))
    pygame.display.update()


def main_menu(win):
    draw_main_menu(win)
    while True:
        pygame.display.update()
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN and event.mod == pygame.KMOD_NONE:
            run(win)
            draw_main_menu(win)

    pygame.display.quit()


def main():
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption("Tetris")
    pygame.font.init()
    main_menu(win)


if __name__ == '__main__':
    main()
