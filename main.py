import math
import random
import pygame

TEST_MODE_ON: bool = True

WIDTH = 1200
HEIGHT = 900
FPS = 60
SQUARE_COUNT = 20
TRAILS_LENGTH = 35
BACKGROUND_COLOR = (20, 20, 20)
# Speed is now in pixels per second (multiplied by FPS to convert from frame-rate dependent).
MIN_SPEED = 60.0  # 1.0 pixels/frame * 60 fps = 60 pixels/second
MAX_SPEED = 300.0  # 5.0 pixels/frame * 60 fps = 300 pixels/second
MIN_LIFE_TIME = 20
MAX_LIFE_TIME = 120
MIN_SQUARE_SIZE = 15
MAX_SQUARE_SIZE = 75

MIN_DETECTION_RANGE = 40
CHASING_FACTOR = 2
EATING_FACTOR = 0.2
GROWTH_SPEED = 0.5
GROWTH_CACHE = []

MIX_SQUARES = [30] * 4 + [25] * 5 + [10] * 10


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


def create_squares(count=0, mix: list = []) -> list[dict]:
    """Create square dictionaries with random size, color, position, and velocity."""
    squares = []
    if len(mix) == 0:
        for _ in range(count):
            square = create_square()
            squares.append(square)

    elif count == 0:
        for size in mix:
            square = create_square(size)
            squares.append(square)

    return squares


def create_square(size=0) -> dict:
    """Create a square dictionary with random size, color, position, and velocity."""
    if size == 0:
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
        "trail": [(x, y)],
    }
    return square


def bounce_square_on_edges(square: dict) -> None:
    """Keep a square inside the window and reverse direction on collision."""
    size = int(square["size"])

    if square["x"] <= 0:
        # square["x"] = 0
        # square["vx"] = abs(square["vx"])
        square["x"] = WIDTH - square["size"]
    elif square["x"] + size > WIDTH:
        # square["x"] = WIDTH - size
        # square["vx"] = -square["vx"]
        square["x"] = 0

    if square["y"] <= 0:
        # square["y"] = 0
        # square["vy"] = abs(square["vy"])
        square["y"] = HEIGHT - square["size"]
    elif square["y"] + size > HEIGHT:
        # square["y"] = HEIGHT - size
        # square["vy"] = -square["vy"]
        square["y"] = 0


def handle_events() -> bool:
    """Process user input and return False when the user asks to quit."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
            return False

    return True


def find_closest_square(is_threat: bool, square: dict, square_snapshots: list, square_index: int) -> tuple[
                                                                                                         float, float] | None:
    """Find the closest larger square (threat to flee from) or smaller square (prey to chase).

    Args:
        is_threat: If True, find larger squares (flee). If False, find smaller squares (chase).
        square: The square we're evaluating.
        square_snapshots: Snapshot of all square positions for consistent detection.
        square_index: Index of the current square.

    Returns:
        Direction vector pointing away from threat or toward prey, or None if none found.
    """
    square_center_x = square["x"] + square["size"] / 2
    square_center_y = square["y"] + square["size"] / 2
    closest_direction = None
    min_distance = (WIDTH ** 2 + HEIGHT ** 2) ** 0.5

    for other_index, other in enumerate(square_snapshots):
        if other_index == square_index:
            continue

        other_size = other[2]

        # Filter by threat type: larger squares are threats, smaller are prey.
        if is_threat and other_size < square["size"]:
            continue
        if not is_threat and other_size > square["size"]:
            continue

        other_center_x = other[0] + other_size / 2
        other_center_y = other[1] + other_size / 2
        x = square_center_x - other_center_x
        y = square_center_y - other_center_y
        distance = (x ** 2 + y ** 2) ** 0.5
        detection_range = (square["size"] + other_size) / 2 + MIN_DETECTION_RANGE

        if distance <= detection_range and distance < min_distance:
            min_distance = distance
            closest_direction = (x, y)

    # For chasing: invert and amplify direction toward prey.
    if closest_direction and not is_threat:
        closest_direction = (
            closest_direction[0] * CHASING_FACTOR * -1,
            closest_direction[1] * CHASING_FACTOR * -1
        )

    return closest_direction


def calculate_new_direction(square: dict, square_snapshots: list, square_index: int) -> tuple[float, float] | None:
    """Calculate new velocity based on threats to flee from and prey to chase.

    Rules:
    - Flee from larger squares (threats).
    - Chase smaller squares (prey).
    - If both exist, balance both forces.
    - Preserve speed magnitude.

    Returns:
        New (vx, vy) tuple or None if no adjustment needed.
    """
    speed = (square["vx"] ** 2 + square["vy"] ** 2) ** 0.5
    speed_xy = None
    # Find closest threat (larger square) and closest prey (smaller square).
    flee_direction = find_closest_square(True, square, square_snapshots, square_index)
    chase_direction = find_closest_square(False, square, square_snapshots, square_index)

    # If neither exists, no change needed.
    if flee_direction and chase_direction is None:
        speed_xy = (square["vx"], square["vy"])
        return speed_xy
    # If only prey exists, chase it.
    elif flee_direction is None:
        return chase_direction
    # If only threat exists, flee from it.
    elif chase_direction is None:
        return flee_direction
    # If both exist, combine forces: net = flee_vector + chase_vector.
    else:
        vx = flee_direction[0] - chase_direction[0]
        vy = flee_direction[1] - chase_direction[1]
        speed_direction = (vx ** 2 + vy ** 2) ** 0.5
        if speed_direction > 0:
            vx = vx / speed_direction * speed
            vy = vy / speed_direction * speed
            new_speed = (vx ** 2 + vy ** 2) ** 0.5
            # avoid too slow speed
            if new_speed < MIN_SPEED:
                vx = vx / new_speed * MIN_SPEED
                vy = vy / new_speed * MIN_SPEED
            speed_xy = (vx, vy)
    return speed_xy


def check_collision(square: dict, other: dict) -> bool:
    # Detect if squares collision, return true if square and other collide
    dx = abs(square["x"] - other["x"])
    dy = abs(square["y"] - other["y"])
    distance = (dx ** 2 + dy ** 2) ** 0.5
    if distance <= square["size"] + other["size"]:
        return True
    else:
        return False


def update_squares(squares: list[dict], delta_time: float) -> None:
    """Move the squares, bounce on edges, apply behavior, and manage lifetimes.

    delta_time: elapsed time in seconds since last frame.
    Movement is scaled by delta_time to ensure consistent speed regardless of frame rate.

    Behavior:
    - Smaller squares flee from larger squares (threats).
    - Larger squares chase smaller squares (prey).
    - Larger squares eat smaller squares if they collide.
    - Each square has a limited lifespan; when life_time expires, a new square spawns.
    """
    # Snapshot the current positions first so behavior checks use the same frame state.
    square_snapshots = [(square["x"], square["y"], square["size"]) for square in squares]

    for square in squares:
        # Update movement first so the frame has a single, predictable order of changes.
        square["life_time"] -= delta_time

        if square["life_time"] <= 0:
            squares.remove(square)
            new = create_square(int(square["size"]))
            squares.append(new)
        else:
            # Multiply velocity by delta_time to make movement independent of frame rate.
            square["x"] += square["vx"] * delta_time
            square["y"] += square["vy"] * delta_time
            if len(square["trail"]) >= TRAILS_LENGTH:
                square["trail"].pop(0)
            square["trail"].append((square["x"] + (square["size"] / 2), square["y"] + (square["size"] / 2)))
            bounce_square_on_edges(square)
        eat(square, squares)
        growth(square, delta_time)

    # Apply flee/chase behavior based on snapshots (all squares had the same position at frame start).
    for square_index, square in enumerate(squares):
        new_direction = calculate_new_direction(square, square_snapshots, square_index)
        if new_direction is not None:
            square["vx"], square["vy"] = new_direction


def eat(square: dict, squares: list[dict]):
    # Eating feature
    for other in squares:
        if square == other:
            continue
        if check_collision(square, other):
            if other["size"] < square["size"]:
                squares.remove(other)
                new = create_square(int(other["size"]))
                squares.append(new)
                if square["size"] < MAX_SQUARE_SIZE:
                    # save into "cache"
                    growth_cache = {"square": square, "plus": other["size"] * EATING_FACTOR}
                    GROWTH_CACHE.append(growth_cache)


def growth(square: dict, delta_time: float):
    # increase the size of square by time
    for c in GROWTH_CACHE:
        if c["plus"] <= 0.0 or square["size"] >= MAX_SQUARE_SIZE:
            GROWTH_CACHE.remove(c)
        elif square == c["square"]:
            delta_size = c["plus"] / GROWTH_SPEED * delta_time
            square["size"] += delta_size


def draw_trail(square: dict, surface: pygame.Surface):
    color = square["color"]
    for i in range(len(square["trail"]) - 1):
        start_pos = square["trail"][i]
        end_pos = square["trail"][i + 1]
        # remove the lines across the screen
        if ((start_pos[0] - end_pos[0]) ** 2 + (start_pos[1] - end_pos[1]) ** 2) ** 0.5 > square["size"]:
            continue
        width: int = 2
        pygame.draw.line(surface, color, start_pos, end_pos, width)


def draw_scene(screen: pygame.Surface, squares: list[dict], hud_font, fps) -> None:
    """Clear the screen, draw the HUD, and render every square."""
    screen.fill(BACKGROUND_COLOR)
    text = hud_font.render(f"FPS: {fps:.1f}", True, (240, 240, 240))
    screen.blit(text, (10, 10))

    for square in squares:
        # Use a descriptive name here because this rectangle is only for rendering.
        square_rect = pygame.Rect(int(square["x"]), int(square["y"]), int(square["size"]), int(square["size"]))
        draw_trail(square, screen)
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
    # squares = create_squares(count = SQUARE_COUNT)
    squares = create_squares(mix=MIX_SQUARES)

    run_loop(screen, clock, hud_font, squares)

    pygame.quit()


if __name__ == "__main__":
    main()
