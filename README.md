# lab8-pygame

Simple Pygame animation with randomly sized, randomly colored squares that move around the screen with autonomous behavior.

## Features

- **20 squares spawn** at random positions by default.
- **Random properties:** Each square gets a random size, color, speed, and lifespan.
- **Size-speed correlation:** Smaller squares move faster than bigger squares.
- **Autonomous behavior:**
  - **Fleeing:** Smaller squares flee away from nearby larger squares (threats).
  - **Chasing:** Larger squares chase nearby smaller squares (prey).
  - **Detection range:** Behavior triggers only when other squares are within `MIN_DETECTION_RANGE`.
- **Lifespan:** Each square has a limited lifespan (`MIN_LIFE_TIME` to `MAX_LIFE_TIME` seconds); when expired, a new square spawns.
- **Physics:** Squares bounce off window edges, keeping their speed and reversing direction.
- **Time-based movement:** Velocity is scaled by elapsed time, ensuring consistent motion regardless of frame rate.

## How it works

- `init_game()` sets up Pygame, the window, frame clock, and HUD font.
- `create_squares()` builds the initial square list.
- `create_square()` generates a single square with random properties.
- `find_closest_square()` detects the nearest threat (larger square) or prey (smaller square) within range.
- `calculate_new_direction()` balances fleeing and chasing forces, combining both behaviors when both apply.
- `run_loop()` drives the frame cycle: input, update, draw, and timing.
- `update_squares()` moves each square, manages lifetimes, and applies flee/chase behavior.
- `draw_scene()` clears the screen, draws the FPS text, and renders every square.

## Constants

- `WIDTH`, `HEIGHT`: Window dimensions (2000×1500).
- `FPS`: Target frame rate (60 FPS).
- `SQUARE_COUNT`: Initial number of squares (20).
- `MIN_SPEED`, `MAX_SPEED`: Speed range in pixels per second (60–300).
- `MIN_SQUARE_SIZE`, `MAX_SQUARE_SIZE`: Square size range (15–75 pixels).
- `MIN_LIFE_TIME`, `MAX_LIFE_TIME`: Lifespan range in seconds (10–60).
- `CHASING_FACTOR`: Multiplier for chase direction intensity (2.0).
- `MIN_DETECTION_RANGE`: Extra distance for behavior detection (40 pixels).

## Requirements

- Python 3.10+
- `pygame`

## Setup

```bash
python3 -m pip install pygame
```

## Run

```bash
python3 main.py
```

## Controls

- Close window to quit.
- Press `Esc` or `q` to quit.

## Notes

- The window size (1200×900) ensures motion is easy to observe.
- The square count and lifespan can be tuned in `main.py` constants.
- Smaller squares are more vulnerable (flee behavior); larger squares are predatory (chase behavior).
- Behavior is continuous throughout each square's lifespan.

