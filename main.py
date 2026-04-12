import random
import math
import pygame

WIDTH = 2000
HEIGHT = 1500
FPS = 60
SQUARE_COUNT = 50
BACKGROUND_COLOR = (20, 20, 20)
MIN_SPEED = 1.0
MAX_SPEED = 3.0
MIN_SQUARE_SIZE = 20
MAX_SQUARE_SIZE = 70
MIN_FLEE_DISTANCE = 20


def init_game() -> tuple[pygame.Surface, pygame.time.Clock]:
    """Initialize pygame and create main objects."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Squares Skeleton")
    clock = pygame.time.Clock()
    return screen, clock


def speed_from_size(size: int) -> float:
    """Map smaller sizes to faster speed and bigger sizes to slower speed."""
    size_range = MAX_SQUARE_SIZE - MIN_SQUARE_SIZE
    if size_range <= 0:
        return MIN_SPEED

    normalized = (size - MIN_SQUARE_SIZE) / size_range
    return MAX_SPEED - normalized * (MAX_SPEED - MIN_SPEED)


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


def calculator(square: dict, list_squares: list, square_index: int):
    """Return the direction vector away from the closest larger square."""
    square_center_x = square["x"] + square["size"] / 2
    square_center_y = square["y"] + square["size"] / 2
    direction = None
    min_distance = WIDTH + HEIGHT

    for other_index, other in enumerate(list_squares):
        if other_index == square_index:
            continue

        other_size = other[2]
        if other_size <= square["size"]:
            continue

        other_center_x = other[0] + other_size / 2
        other_center_y = other[1] + other_size / 2
        x = square_center_x - other_center_x
        y = square_center_y - other_center_y
        distance = (x ** 2 + y ** 2) ** 0.5
        flee_distance = (square["size"] + other_size) / 2 + MIN_FLEE_DISTANCE

        if distance <= flee_distance and distance < min_distance:
            min_distance = distance
            direction = (x, y)

    return direction


def flee(square: dict, list_squares: list, square_index: int):
    if square["size"] > (MAX_SQUARE_SIZE + MIN_SQUARE_SIZE) / 2:
        pass
    else:
        speed = (square["vx"] ** 2 + square["vy"] ** 2) ** 0.5
        direction = calculator(square, list_squares, square_index)
        if direction is not None:
            speed_direction = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
            if speed_direction > 0:
                square["vx"] = direction[0] / speed_direction * speed
                square["vy"] = direction[1] / speed_direction * speed


def update_squares(squares: list[dict]) -> None:
    """Move each square and bounce it when it reaches a screen edge."""
    list_squares = [(square["x"], square["y"], square["size"]) for square in squares]

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
    for square_index, square in enumerate(squares):
        flee(square, list_squares, square_index)


def draw_scene(screen: pygame.Surface, squares: list[dict], hud_font, fps) -> None:
    """Render all game objects."""
    screen.fill(BACKGROUND_COLOR)
    text = hud_font.render(f"FPS: {fps:.1f}", True, (240, 240, 240))
    screen.blit(text, (10, 10))

    for square in squares:
        rect = pygame.Rect(int(square["x"]), int(square["y"]), int(square["size"]), int(square["size"]))
        pygame.draw.rect(screen, square["color"], rect)

    pygame.display.flip()


def run_loop(screen: pygame.Surface, clock: pygame.time.Clock, squares: list[dict]) -> None:
    """Main loop that coordinates events, updates, and rendering."""
    running = True
    while running:
        hud_font = pygame.font.SysFont(None, 28)
        fps = clock.get_fps()

        running = handle_events()
        update_squares(squares)
        draw_scene(screen, squares, hud_font, fps)
        clock.tick(FPS)


def main() -> None:
    """Program entrypoint."""
    screen, clock = init_game()
    squares = create_squares(SQUARE_COUNT)

    run_loop(screen, clock, squares)

    pygame.quit()


if __name__ == "__main__":
    main()
