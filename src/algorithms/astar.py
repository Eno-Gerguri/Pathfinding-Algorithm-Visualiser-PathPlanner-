from queue import PriorityQueue

import pygame

from node.node_states import NodeStates


def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(path_history, current, draw):
    while current in path_history:
        current = path_history[current]
        current.set_state(NodeStates.ISPATH)
        draw()


def astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    path_history = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

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
                f_score[neighbor] = temp_g_score + heuristic(
                        neighbor.get_pos(), end.get_pos()
                )
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.set_state(NodeStates.ISOPEN)

        draw()

        if current != start:
            current.set_state(NodeStates.ISBLOCKED)
