import pygame

from config import ROWS, WIDTH
from node.node_states import NodeStates


def handle_mouse_events(grid, start, end):
    pos = pygame.mouse.get_pos()
    row, col = get_clicked_pos(pos, ROWS, WIDTH)
    node = grid[row][col]

    mouse_events = pygame.mouse.get_pressed()
    if mouse_events[0]:
        if not start and node != end:
            start = node
            start.set_state(NodeStates.ISSTART)
        elif not end and node != start:
            end = node
            end.set_state(NodeStates.ISTARGET)
        elif node != start and node != end:
            node.set_state(NodeStates.ISBARRIER)
    elif mouse_events[2]:
        node.set_state(NodeStates.ISEMPTY)
        if node == start:
            start = None
        elif node == end:
            end = None

    return start, end


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col
