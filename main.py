import random

import pygame

WIDTH = 800
HEIGHT = 800
FPS = 60
SQUARE_COUNT = 10
SQUARE_SIZE = 30
BACKGROUND_COLOR = (20, 20, 20)
SQUARE_COLOR = (80, 200, 255)


def init_game() -> tuple[pygame.Surface, pygame.time.Clock]:
    """Initialize pygame and create main objects."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Squares Skeleton")
    clock = pygame.time.Clock()
    return screen, clock


def create_squares(count: int) -> list[dict[str, int]]:
    """Build square data with placeholder values.

    TODO: How can you assign each square a random (x, y) and a random (vx, vy)
    so they start in different places and move in different directions?
    """
    squares: list[dict[str, int]] = []

    for i in range(count):
        # Placeholder layout so all 10 squares are visible in the skeleton.
        x = random.randint(0, WIDTH - SQUARE_SIZE)
        y = random.randint(0, HEIGHT - SQUARE_SIZE)
        vx = random.uniform(-1.0, 1.0)
        vy = random.uniform(-1.0, 1.0)

        square = {
            "x": x,
            "y": y,
            "size": SQUARE_SIZE,
            "vx": vx,
            "vy": vy,
        }
        squares.append(square)

    return squares


def handle_events() -> bool:
    """Process user input.

    TODO: What additional keyboard controls would help you debug movement speed?
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def update_squares(squares: list[dict[str, int]]) -> None:
    """Update square positions.

    TODO:
    1) Add velocity to position each frame.
    2) Reverse velocity when hitting a screen edge.
    3) Optionally randomize direction every N frames.
    """
    for square in squares:
        # Placeholder update so skeleton runs before movement logic is implemented.
        square["x"] += square["vx"]
        square["y"] += square["vy"]

        if square["x"] <= 0 or square["x"] + SQUARE_SIZE > WIDTH:
            square["vx"] = -square["vx"]
        if square["y"] <= 0 or square["y"] + SQUARE_SIZE > HEIGHT:
            square["vy"] = -square["vy"]


def draw_scene(screen: pygame.Surface, squares: list[dict[str, int]]) -> None:
    """Render all game objects."""
    screen.fill(BACKGROUND_COLOR)

    for square in squares:
        rect = pygame.Rect(square["x"], square["y"], square["size"], square["size"])
        pygame.draw.rect(screen, SQUARE_COLOR, rect)

    pygame.display.flip()


def run_loop(screen: pygame.Surface, clock: pygame.time.Clock, squares: list[dict[str, int]]) -> None:
    """Main loop that coordinates events, updates, and rendering."""
    running = True
    while running:
        running = handle_events()
        update_squares(squares)
        draw_scene(screen, squares)
        clock.tick(FPS)


def main() -> None:
    """Program entrypoint.

    TODO: Before implementing random movement, what variable values do you want to
    print each frame to verify your assumptions?
    """
    screen, clock = init_game()
    squares = create_squares(SQUARE_COUNT)

    run_loop(screen, clock, squares)

    pygame.quit()


if __name__ == "__main__":
    main()
