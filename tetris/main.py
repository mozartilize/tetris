import sys, os
import pygame

from .grid import TetrisGrid, GriddedShape, Point, valid_space, clear_rows
from .shape import Shape
from .graphic import GameGraphic, draw_text_middle, draw_main_menu
from .helpers import get_font
from .consts import *


def get_shape(grid_width):
    return GriddedShape(Point(grid_width // 2, 0), Shape.new_shape())


def get_score_file_dir():
    dirpath = os.path.dirname(os.path.abspath(__file__))
    if os.path.expanduser('~') not in dirpath:  # tetris installed in root
        return os.path.expanduser('~')
    return dirpath


def update_score(nscore, dirpath):
    score = max_score(dirpath)

    with open(os.path.join(dirpath, "tetris_score.txt"), "w") as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score(dirpath):
    try:
        with open(os.path.join(dirpath, "tetris_score.txt"), "r") as f:
            lines = f.readlines()
            score = lines[0].strip()
    except FileNotFoundError:
        score = '0'
    return score

dirpath = get_score_file_dir()


def run(win):  # *
    last_score = max_score(dirpath)
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
    graphic.draw_all(next_piece, last_score, score)
    while running:
        grid.update_to_locked_points(locked_points)  # reset grid

        fall_time1 += clock.get_rawtime()
        # level_time += clock.get_rawtime()
        clock.tick()

        # if level_time / 1000 > 5:
        #     level_time = 0
        #     if level_time > 0.12:
        #         level_time -= 0.005

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN and event.mod == pygame.KMOD_NONE:
                if event.key == pygame.K_F9:
                    pause = True
                    sub, rect = graphic.draw_pause()
                    while pause:
                        event = pygame.event.wait()
                        if event.type == pygame.QUIT:
                            pygame.display.quit()
                            sys.exit(0)
                        elif event.type == pygame.KEYDOWN \
                                and event.mod == pygame.KMOD_NONE \
                                and event.key == pygame.K_F9:
                            pause = False
                            graphic.draw_unpause(sub, rect)

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
                grid.update_to_new_locked_points(locked_points)                
                earn_score = clear_rows(grid, locked_points) * 10
                if earn_score > 0:
                    score += earn_score
                    graphic.draw_score(score)

                if grid.check_lost():
                    draw_text_middle(win, "YOU LOST!", 80, TEXT_COLOR)
                    pygame.display.update()
                    pygame.time.delay(1500)
                    running = False
                    update_score(score, dirpath)
                    pygame.event.clear()                
                else:
                    current_piece = next_piece
                    next_piece = get_shape(grid.width)
                    graphic.draw_next_shape(next_piece)
        tmp_points = dict(locked_points)
        for point in current_piece.positions:
            if point.y > -1:
                tmp_points[point] = current_piece.color
        grid.update_to_locked_points(tmp_points)

        graphic.draw_grid()


def main_menu(win):
    draw_main_menu(win)
    while True:
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
