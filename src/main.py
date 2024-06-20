import pygame

from config import WIDTH, HEIGHT, ROWS
from database_manager import create_database
from event_handlers.keyboard_handler import handle_keyboard_events
from event_handlers.mouse_handler import handle_mouse_events
from grid_manager import *
from user_authentication.login_system import handle_login


def visualiser(visualiser_window, WIDTH, user_id):
    grid = make_grid(ROWS, WIDTH)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(visualiser_window, grid, ROWS, WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:  # User cannot change grid during visualisation
                continue

            start, end = handle_mouse_events(grid, start, end)
            grid, start, end = handle_keyboard_events(
                    visualiser_window, user_id, event, grid, start, end
            )

    pygame.quit()


if __name__ == "__main__":
    create_database()
    user_id = handle_login()

    if user_id:  # In case the user does not log in but just closes the window
        visualiser_window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pathfinding Visualiser")
        visualiser(visualiser_window, WIDTH, user_id)
