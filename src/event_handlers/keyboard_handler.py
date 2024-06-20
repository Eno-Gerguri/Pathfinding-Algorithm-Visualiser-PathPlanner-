from tkinter import messagebox

import pygame

from algorithms.astar import astar
from algorithms.dijkstra import dijkstra
from database_manager import get_tags, save_screenshot
from grid_manager import draw, make_grid
from config import ROWS, WIDTH
from screenshot_manager.comment_system.make_comment_window import MakeNewCommentWindow
from screenshot_manager.screenshot_system import handle_select_tag


def handle_keyboard_events(
        visualiser_window,
        user_id,
        event,
        grid,
        start,
        end
):
    if event.type != pygame.KEYDOWN:
        return grid, start, end

    match event.key:
        case pygame.K_a:  # Perform astar algorithm
            if start and end:
                for row in grid:
                    for node in row:
                        node.update_neighbors(grid)
                astar(
                        lambda: draw(visualiser_window, grid, ROWS, WIDTH),
                        grid,
                        start,
                        end
                )

        case pygame.K_d:  # Perform Dijkstra's algorithm
            if start and end:
                for row in grid:
                    for node in row:
                        node.update_neighbors(grid)
                dijkstra(
                        lambda: draw(visualiser_window, grid, ROWS, WIDTH),
                        grid,
                        start,
                        end
                )

        case pygame.K_e:  # Empty the grid
            start = None
            end = None
            grid = make_grid(ROWS, WIDTH)

        case pygame.K_s:  # Screenshot the grid
            tags = [tag[1] for tag in get_tags()]
            tag = handle_select_tag(tags)
            if tag:
                screenshot_id = save_screenshot(user_id, tag)
                MakeNewCommentWindow(user_id, screenshot_id).mainloop()
            else:
                messagebox.showerror(
                        "Screenshot Cancelled",
                        "Screenshot was not saved as no tag was provided"
                )

        case pygame.K_c:  # Make a comment on a screenshot the user took
            MakeNewCommentWindow(user_id).mainloop()

    return grid, start, end
