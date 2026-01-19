# 🐦 Flappy Bird

## Overview
Classic Flappy Bird clone with pixel art style. Tap to flap through pipes.

## Gameplay
- **Objective**: Pass through as many pipes as possible
- **Controls**: 
  - **SPACE / A button**: Flap wings
- **Scoring**: 1 point per pipe passed
- **Difficulty**: Fixed pipe speed, tight gaps

## Features
- ✅ Simple one-button control
- ✅ Smooth gravity physics
- ✅ Procedural pipe generation
- ✅ Parallax clouds
- ✅ Wing flapping animation
- ✅ Medal system (bronze/silver/gold)
- ✅ High score

## Technical Details
- **Engine**: Godot 4.3
- **Physics**: Custom gravity (980 units/s²)
- **Key Scripts**:
  - Bird.gd (physics + animation)
  - Pipe.gd (scrolling + collision)
  - GameManager.gd (scoring + game state)

## Assets Required
- Bird: 3 frame flapping animation
- Pipes: top and bottom segments
- Background: sky gradient, clouds, ground
- UI: medal icons, game over screen

## Development Time
**Estimated**: 4-5 hours
- Bird physics: 1h
- Pipe spawning: 1.5h
- Collision: 1h
- UI & polish: 1.5h

## Difficulty Tuning
```gdscript
const GRAVITY = 980.0        # Adjust for difficulty
const JUMP_VELOCITY = -600.0 # Lower = harder
const PIPE_SPEED = 200.0     # Higher = harder
const PIPE_GAP = 200.0       # Smaller = harder
```

## Testing Checklist
- [ ] Bird flaps on input
- [ ] Gravity feels natural
- [ ] Pipes scroll smoothly
- [ ] Gap size is fair
- [ ] Collision detection accurate
- [ ] Score increments correctly
- [ ] Game over works
- [ ] Restart works