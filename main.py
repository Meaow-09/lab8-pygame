import random
import math
import pygame

WIDTH = 1000
HEIGHT = 1000
FPS = 60
SQUARE_COUNT = 20
BACKGROUND_COLOR = (20, 20, 20)
MIN_SPEED = 1.0
MAX_SPEED = 3.0
MIN_SQUARE_SIZE = 20
MAX_SQUARE_SIZE = 70


def speed_from_size(size: int) -> float:
    """Map smaller sizes to faster speed and bigger sizes to slower speed."""
    size_range = MAX_SQUARE_SIZE - MIN_SQUARE_SIZE
    if size_range <= 0:
        return MIN_SPEED

    normalized = (size - MIN_SQUARE_SIZE) / size_range
    return MAX_SPEED - normalized * (MAX_SPEED - MIN_SPEED)


def init_game() -> tuple[pygame.Surface, pygame.time.Clock]:
    """Initialize pygame and create main objects."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Squares Skeleton")
    clock = pygame.time.Clock()
    return screen, clock


def create_squares(count: int) -> list[dict]:
    """Create squares at random positions with random non-zero velocities."""
    squares = []

    for _ in range(count):
        size = random.randint(MIN_SQUARE_SIZE, MAX_SQUARE_SIZE)
        x = random.randint(0, WIDTH - size)
        y = random.randint(0, HEIGHT - size)
        speed = speed_from_size(size)
        angle = random.uniform(0.0, 2 * math.pi)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        color = (
            random.randint(40, 255),
            random.randint(40, 255),
            random.randint(40, 255),
        )

        square = {
            "x": x,
            "y": y,
            "size": size,
            "vx": vx,
            "vy": vy,
            "color": color,
        }
        squares.append(square)

    return squares



def handle_events() -> bool:
    """Process user input and return whether the app should keep running."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
            return False

    return True


def update_squares(squares: list[dict]) -> None:
    """Move each square and bounce it when it reaches a screen edge."""
    for square in squares:
        size = int(square["size"])
        square["x"] += square["vx"]
        square["y"] += square["vy"]

        if square["x"] <= 0:
            square["x"] = 0
            square["vx"] = abs(square["vx"])
        elif square["x"] + size >= WIDTH:
            square["x"] = WIDTH - size
            square["vx"] = -square["vx"]

        if square["y"] <= 0:
            square["y"] = 0
            square["vy"] = abs(square["vy"])
        elif square["y"] + size >= HEIGHT:
            square["y"] = HEIGHT - size
            square["vy"] = -square["vy"]



def draw_scene(screen: pygame.Surface, squares: list[dict]) -> None:
    """Render all game objects."""
    screen.fill(BACKGROUND_COLOR)

    for square in squares:
        rect = pygame.Rect(int(square["x"]), int(square["y"]), int(square["size"]), int(square["size"]))
        pygame.draw.rect(screen, square["color"], rect)

    pygame.display.flip()


def run_loop(screen: pygame.Surface, clock: pygame.time.Clock, squares: list[dict]) -> None:
    """Main loop that coordinates events, updates, and rendering."""
    running = True
    while running:
        running = handle_events()
        update_squares(squares)
        draw_scene(screen, squares)
        clock.tick(FPS)


def main() -> None:
    """Program entrypoint."""
    screen, clock = init_game()
    squares = create_squares(SQUARE_COUNT)

    run_loop(screen, clock, squares)

    pygame.quit()


if __name__ == "__main__":
    main()
