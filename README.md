# lab8-pygame

Simple Pygame animation with randomly sized, randomly colored squares that move around the screen.

## Features

re- 25 squares spawn at random positions by default.
- Each square gets a random size.
- Each square gets a different random color.
- Each square starts with a random speed and direction.
- Smaller squares move faster than bigger squares.
- Squares can flee away from nearby larger squares.
- Squares bounce on window edges.

## How it works

- `init_game()` sets up Pygame, the window, and the frame clock.
- `create_squares()` builds the square list with size, position, velocity, and color.
- `run_loop()` drives the frame cycle: input, update, draw, and timing.
- `update_squares()` moves each square, keeps it inside the window, and applies the flee behavior.
- `draw_scene()` clears the screen, draws the FPS text, and renders every square.

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

- The window size is large on purpose (`2000x1500`) so the motion is easy to see.
- The square count is controlled by `SQUARE_COUNT` in `main.py`.

