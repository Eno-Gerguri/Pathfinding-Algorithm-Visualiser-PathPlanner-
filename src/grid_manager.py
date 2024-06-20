import pygame

from node.node import Node
from config import Colors


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(
                win, Colors.GRIDLINES_COLOR, (0, i * gap), (width, i * gap)
        )
        for j in range(rows):
            pygame.draw.line(
                    win, Colors.GRIDLINES_COLOR, (j * gap, 0), (j * gap, width)
            )


def draw(win, grid, rows, width):
    win.fill(Colors.ISEMPTY_COLOR)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()
