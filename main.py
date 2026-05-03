import math
import random
import pygame

WIDTH = 1200
HEIGHT = 900
FPS = 60
SQUARE_COUNT = 20
BACKGROUND_COLOR = (20, 20, 20)
# Speed is now in pixels per second (multiplied by FPS to convert from frame-rate dependent).
MIN_SPEED = 60.0  # 1.0 pixels/frame * 60 fps = 60 pixels/second
MAX_SPEED = 300.0  # 5.0 pixels/frame * 60 fps = 300 pixels/second
MIN_LIFE_TIME = 10
MAX_LIFE_TIME = 60
MIN_SQUARE_SIZE = 10
MAX_SQUARE_SIZE = 75
MIN_FLEE_DISTANCE = 30


def init_game() -> tuple[pygame.Surface, pygame.time.Clock, pygame.font.Font]:
    """Initialize Pygame and return the screen surface and frame clock."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Squares Skeleton")
    clock = pygame.time.Clock()
    hud_font = pygame.font.SysFont(None, 28)
    return screen, clock, hud_font


def speed_from_size(size: int) -> float:
    """Map a square size to a speed value: smaller squares move faster."""
    size_range = MAX_SQUARE_SIZE - MIN_SQUARE_SIZE
    if size_range <= 0:
        return MIN_SPEED

    normalized = (size - MIN_SQUARE_SIZE) / size_range
    return MAX_SPEED - normalized * (MAX_SPEED - MIN_SPEED)


def create_squares(count: int) -> list[dict]:
    """Create square dictionaries with random size, color, position, and velocity."""
    squares = []

    for _ in range(count):
        square = create_square()
        squares.append(square)

    return squares


def create_square() -> dict:
    """Create a square dictionary with random size, color, position, and velocity."""
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
    life_time = random.randint(MIN_LIFE_TIME, MAX_LIFE_TIME)

    square = {
        "x": x,
        "y": y,
        "size": size,
        "vx": vx,
        "vy": vy,
        "color": color,
        "life_time": life_time,
    }
    return square


def bounce_square_on_edges(square: dict) -> None:
    """Keep a square inside the window and reverse direction on collision."""
    size = int(square["size"])

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


def handle_events() -> bool:
    """Process user input and return False when the user asks to quit."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
            return False

    return True


def find_flee_direction(square: dict, square_snapshots: list, square_index: int) -> tuple[float, float] | None:
    """Return a vector pointing away from the closest larger square nearby."""
    square_center_x = square["x"] + square["size"] / 2
    square_center_y = square["y"] + square["size"] / 2
    direction = None
    min_distance = (WIDTH ** 2 + HEIGHT ** 2) ** 0.5

    for other_index, other in enumerate(square_snapshots):
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


def flee(square: dict, square_snapshots: list, square_index: int):
    """Adjust a square's velocity so it keeps its speed while fleeing."""
    speed = (square["vx"] ** 2 + square["vy"] ** 2) ** 0.5
    direction = find_flee_direction(square, square_snapshots, square_index)
    if direction is not None:
        speed_direction = (direction[0] ** 2 + direction[1] ** 2) ** 0.5

        if speed_direction > 0:
            square["vx"] = direction[0] / speed_direction * speed
            square["vy"] = direction[1] / speed_direction * speed


def update_squares(squares: list[dict], delta_time: float) -> None:
    """Move the squares, bounce on edges, then apply flee behavior.

    delta_time: elapsed time in seconds since last frame.
    Movement is scaled by delta_time to ensure consistent speed regardless of frame rate.
    """
    # Snapshot the current positions first so flee checks use the same frame state.
    square_snapshots = [(square["x"], square["y"], square["size"]) for square in squares]

    for square in squares:
        # Update movement first so the frame has a single, predictable order of changes.
        square["life_time"] -= delta_time
        if square["life_time"] <= 0:
            squares.remove(square)
            new = create_square()
            squares.append(new)
        else:
            # Multiply velocity by delta_time to make movement independent of frame rate.
            square["x"] += square["vx"] * delta_time
            square["y"] += square["vy"] * delta_time
            bounce_square_on_edges(square)

    for square_index, square in enumerate(squares):
        flee(square, square_snapshots, square_index)


def draw_scene(screen: pygame.Surface, squares: list[dict], hud_font, fps) -> None:
    """Clear the screen, draw the HUD, and render every square."""
    screen.fill(BACKGROUND_COLOR)
    text = hud_font.render(f"FPS: {fps:.1f}", True, (240, 240, 240))
    screen.blit(text, (10, 10))

    for square in squares:
        # Use a descriptive name here because this rectangle is only for rendering.
        square_rect = pygame.Rect(int(square["x"]), int(square["y"]), int(square["size"]), int(square["size"]))
        pygame.draw.rect(screen, square["color"], square_rect)

    pygame.display.flip()


def run_loop(screen: pygame.Surface, clock: pygame.time.Clock, hud_font: pygame.font.Font, squares: list[dict]) -> None:
    """Run the main frame loop: input, update, draw, then tick the clock.

    Time-based movement: delta_time ensures movement is frame-rate independent.
    """
    running = True
    while running:
        # Calculate elapsed time in seconds since last frame (clock.tick returns milliseconds).
        delta_time = clock.tick(FPS) / 1000.0

        # The loop stays in this exact order so the current frame can be read, updated, and rendered clearly.
        fps = clock.get_fps()
        running = handle_events()
        update_squares(squares, delta_time)  # Pass delta_time for time-based movement.
        draw_scene(screen, squares, hud_font, fps)
        # Note: clock.tick is now called above to get delta_time, not at the end.


def main() -> None:
    """Program entrypoint for the square animation demo."""
    # Initialize the window and frame clock once before creating the animated squares.
    screen, clock, hud_font = init_game()
    squares = create_squares(SQUARE_COUNT)

    run_loop(screen, clock, hud_font, squares)

    pygame.quit()


if __name__ == "__main__":
    main()
