# 🐍 Snake

## Overview
Classic Snake. Eat food, grow longer, don't hit yourself or walls.

## Gameplay
- **Objective**: Get highest score
- **Controls**: 
  - **Arrow keys / D-Pad**: Change direction
- **Scoring**: 10 points per food
- **Difficulty**: Speed increases as you grow

## Features
- ✅ Smooth snake movement
- ✅ Food spawning
- ✅ Self-collision detection
- ✅ Wall collision (or wrap-around)
- ✅ Score display
- ✅ High score
- ✅ Speed scaling

## Technical Details
- **Grid**: 20x20 pixels per cell
- **Movement Speed**: 8-20 cells/second (scales with score)

## Snake Logic
```python
# Move snake
head = snake[0] + direction
snake.insert(0, head)

if head == food:
    score += 10
    spawn_food()
else:
    snake.pop()  # Remove tail

# Check collision
if head in snake[1:] or out_of_bounds(head):
    game_over()
```

## Assets Required
- Snake head: 20x20 (green, with eyes in direction)
- Snake body: 20x20 (dark green)
- Food: 20x20 (red apple/circle)
- Background: grid optional

## Development Time
**Estimated**: 3-4 hours
- Snake movement: 1h
- Food & growth: 1h
- Collision: 1h
- UI & polish: 1h

## Testing Checklist
- [ ] Snake moves in 4 directions
- [ ] Can't reverse direction instantly
- [ ] Eats food and grows
- [ ] Self-collision works
- [ ] Wall collision works
- [ ] Score increments
- [ ] Speed increases
- [ ] Game over works
- [ ] High score saves