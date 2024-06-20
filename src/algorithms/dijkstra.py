import pygame
from queue import PriorityQueue

from node.node_states import NodeStates


def dijkstra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    path_history = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]

        if current == end:
            reconstruct_path(path_history, end, draw)
            start.set_state(NodeStates.ISSTART)
            end.set_state(NodeStates.ISTARGET)
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                path_history[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in [item[2] for item in open_set.queue]:
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))
                    neighbor.set_state(NodeStates.ISOPEN)

        draw()

        if current != start:
            current.set_state(NodeStates.ISBLOCKED)

    return False

def reconstruct_path(path_history, current, draw):
    while current in path_history:
        current = path_history[current]
        current.set_state(NodeStates.ISPATH)
        draw()
