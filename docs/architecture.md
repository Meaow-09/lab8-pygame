# Project Architecture

This document describes the architecture of the `lab8-pygame` project based on `main.py`.

## 1) Module Dependency Graph

```mermaid
flowchart LR
    subgraph "Project Module"
        M["main.py"]
    end

    subgraph "Standard Library"
        R["random"]
        T["math"]
    end

    subgraph "Third-Party"
        P["pygame"]
    end

    M --> R
    M --> T
    M --> P
```

`main.py` imports only `random`, `math`, and `pygame`.

## 2) High-Level Runtime Flow

```mermaid
flowchart TD
    A["Program Start"] --> B["main()"]
    B --> C["init_game()"]
    B --> D["create_squares(SQUARE_COUNT)"]
    C --> E["run_loop(screen, clock, squares)"]
    D --> E

    subgraph "Per Frame"
        F["clock.get_fps()"] --> G["handle_events()"]
        G --> H["update_squares(squares)"]
        H --> I["draw_scene(screen, squares, hud_font, fps)"]
        I --> J["clock.tick(FPS)"]
    end

    E --> F
    J --> K{"running == True?"}
    K -->|"Yes"| F
    K -->|"No"| L["pygame.quit()"]
    L --> M["Program End"]
```

The frame loop continues while `handle_events()` keeps `running` true.

## 3) Function-Level Call Graph

```mermaid
flowchart TD
    A["main"] --> B["init_game"]
    A --> C["create_squares"]
    A --> D["run_loop"]
    A --> E["pygame.quit"]

    C --> F["speed_from_size"]
    C --> G["random.randint"]
    C --> H["random.uniform"]
    C --> I["math.cos"]
    C --> J["math.sin"]

    D --> K["pygame.font.SysFont"]
    D --> L["clock.get_fps"]
    D --> M["handle_events"]
    D --> N["update_squares"]
    D --> O["draw_scene"]
    D --> P["clock.tick"]

    M --> Q["pygame.event.get"]

    N --> R["flee"]
    R --> S["find_flee_direction"]

    O --> T["screen.fill"]
    O --> U["hud_font.render"]
    O --> V["screen.blit"]
    O --> W["pygame.Rect"]
    O --> X["pygame.draw.rect"]
    O --> Y["pygame.display.flip"]
```

Internal logic centers around movement (`update_squares`) and behavior (`flee`/`find_flee_direction`).

## 4) Primary Execution Sequence Diagram

```mermaid
sequenceDiagram
    participant U as "User"
    participant App as "Python Process"
    participant Main as "main()"
    participant Init as "init_game()"
    participant Create as "create_squares()"
    participant Loop as "run_loop()"
    participant Events as "handle_events()"
    participant Update as "update_squares()"
    participant Flee as "flee()"
    participant Find as "find_flee_direction()"
    participant Draw as "draw_scene()"
    participant PG as "pygame"

    U->>App: "Run script"
    App->>Main: "Enter main()"
    Main->>Init: "Initialize display + clock"
    Init->>PG: "init, set_mode, set_caption, Clock"
    PG-->>Init: "screen, clock ready"
    Init-->>Main: "screen, clock"

    Main->>Create: "Create squares"
    Create->>PG: "No direct call"
    Create-->>Main: "squares list"

    Main->>Loop: "Start frame loop"

    loop "While running is True"
        Loop->>Events: "Poll input"
        Events->>PG: "event.get()"
        alt "QUIT or ESC/Q pressed"
            Events-->>Loop: "False"
        else "No exit event"
            Events-->>Loop: "True"
        end

        Loop->>Update: "Move and bounce squares"
        loop "For each square"
            Update->>Update: "Apply velocity + boundary checks"
        end
        loop "For each square (behavior pass)"
            Update->>Flee: "Adjust velocity when threatened"
            Flee->>Find: "Find nearest larger square in range"
            Find-->>Flee: "direction or None"
            Flee-->>Update: "updated velocity"
        end
        Update-->>Loop: "state updated"

        Loop->>Draw: "Render frame"
        Draw->>PG: "fill, text render, rect draw, display.flip"
        Draw-->>Loop: "frame presented"

        Loop->>PG: "clock.tick(FPS)"
    end

    Loop-->>Main: "Exit loop"
    Main->>PG: "pygame.quit()"
    Main-->>App: "Process exits"
```

## Assumptions

- Architecture is inferred from `main.py` only.
- There are no additional local modules involved in runtime flow.
- The primary path is normal startup, repeated frame loop, and graceful quit via window close or `Esc`/`Q`.

