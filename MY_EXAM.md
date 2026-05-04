# Exam

## 7: Trails Specs

<img src="./assets/image-20260504111022834.png" alt="image-20260504111022834" style="zoom:50%;" />

- When square "Screen Warpping", the trail go through the whole screen
  - Fix: While drawing the line , ignore the line that's too long

## 8 Speed Test

```python
# What's "correct speed"?

if TEST_MODE_ON:
    if (square["vx"] ** 2 + square["vy"] ** 2) ** 0.5 == square["correct_speed"]:
        pass
    else:
        # if not correct
        square["color"] = (255,0,0) # RED
        # or pygame.draw.xxx
```

## 10: Screen Wrapping

