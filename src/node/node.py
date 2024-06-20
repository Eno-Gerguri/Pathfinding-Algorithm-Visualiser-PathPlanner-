import pygame

from src.node.node_states import NodeStates
from src.config import Colors


class Node:
    def __init__(self, row, col, width, height, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * height
        self.width = width
        self.height = height
        self.total_rows = total_rows
        self.color = Colors.ISEMPTY_COLOR
        self.neighbors = []
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def get_state(self):
        match self.color:
            case Colors.ISEMPTY_COLOR:
                return NodeStates.ISEMPTY
            case Colors.ISBLOCKED_COLOR:
                return NodeStates.ISBLOCKED
            case Colors.ISOPEN_COLOR:
                return NodeStates.ISOPEN
            case Colors.ISBARRIER_COLOR:
                return NodeStates.ISBARRIER
            case Colors.ISSTART_COLOR:
                return NodeStates.ISSTART
            case Colors.ISTARGET_COLOR:
                return NodeStates.ISTARGET
            case Colors.ISPATH_COLOR:
                return NodeStates.ISPATH
            case _:
                raise ValueError(f"Invalid color: {self.color}")

    def set_state(self, state):
        match state:
            case NodeStates.ISEMPTY:
                self.color = Colors.ISEMPTY_COLOR
            case NodeStates.ISBLOCKED:
                self.color = Colors.ISBLOCKED_COLOR
            case NodeStates.ISOPEN:
                self.color = Colors.ISOPEN_COLOR
            case NodeStates.ISBARRIER:
                self.color = Colors.ISBARRIER_COLOR
            case NodeStates.ISSTART:
                self.color = Colors.ISSTART_COLOR
            case NodeStates.ISTARGET:
                self.color = Colors.ISTARGET_COLOR
            case NodeStates.ISPATH:
                self.color = Colors.ISPATH_COLOR
            case _:
                raise ValueError(f"Invalid state: {state}")

    def draw(self, win):
        pygame.draw.rect(
                win, self.color, (self.x, self.y, self.width, self.height)
        )

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 \
                and grid[self.row + 1][self.col].get_state() \
                != NodeStates.ISBARRIER:  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 \
                and grid[self.row - 1][self.col].get_state() \
                != NodeStates.ISBARRIER:  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 \
                and grid[self.row][self.col + 1].get_state() \
                != NodeStates.ISBARRIER:  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 \
                and grid[self.row][self.col - 1].get_state() \
                != NodeStates.ISBARRIER:  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False
