````markdown
# 🟦 Tetris

## Overview
Classic Tetris. Rotate and place falling blocks, clear lines.

## Gameplay
- **Objective**: Clear as many lines as possible
- **Controls**: 
  - **Arrow keys / D-Pad**: Move left/right/down
  - **UP / A button**: Rotate clockwise
  - **SPACE**: Hard drop
  - **C**: Hold piece (swap with hold box)
- **Scoring**:
  - 1 line: 100 points
  - 2 lines: 300 points
  - 3 lines: 500 points
  - 4 lines (Tetris): 800 points
- **Level**: Increases every 10 lines

## Features
- ✅ 7 tetromino types (I, O, T, S, Z, J, L)
- ✅ SRS rotation system
- ✅ Wall kicks
- ✅ Ghost piece (preview)
- ✅ Hold piece
- ✅ Next piece preview
- ✅ Line clearing animation
- ✅ Level progression (speed increase)
- ✅ High score

## Technical Details
- **Grid**: 10 wide x 20 tall (blocks = 20x20 pixels)
- **Rotation System**: Super Rotation System (SRS) with wall kicks

## Tetromino Types
```python
SHAPES = {
    'I': [[1,1,1,1]],                      # Cyan
    'O': [[1,1],[1,1]],                    # Yellow
    'T': [[0,1,0],[1,1,1]],                # Purple
    'S': [[0,1,1],[1,1,0]],                # Green
    'Z': [[1,1,0],[0,1,1]],                # Red
    'J': [[1,0,0],[1,1,1]],                # Blue
    'L': [[0,0,1],[1,1,1]]                 # Orange
}
```

## Rotation System (SRS)
```python
def rotate(piece):
    rotated = rotate_matrix(piece)
    
    # Try 5 wall kick positions
    for offset in wall_kick_offsets:
        if not collides(rotated, offset):
            return rotated, offset
    
    return piece, (0, 0)  # Can't rotate
```

## Scoring Formula
```python
def calculate_score(lines_cleared, level):
    base_points = {1: 100, 2: 300, 3: 500, 4: 800}
    return base_points[lines_cleared] * (level + 1)
```

## Assets Required
- Blocks: 7 colors (20x20 each) - I, O, T, S, Z, J, L
- Ghost block: semi-transparent version
- Grid: background with lines
- UI panels: next piece, hold piece, score, level, lines
- Line clear effect: flash/particle animation

## Development Time
**Estimated**: 6-8 hours
- Grid & basic falling: 1h
- Rotation logic: 2h
- Wall kicks: 1h
- Line clearing: 1h
- Hold & next piece: 1h
- Scoring & levels: 1h
- Polish: 1h

## Testing Checklist
- [ ] Pieces fall at correct speed
- [ ] Left/right movement works
- [ ] Rotation works in all positions
- [ ] Wall kicks work
- [ ] Can't rotate into blocks
- [ ] Lines clear when full
- [ ] Score calculates correctly
- [ ] Level increases
- [ ] Speed increases with level
- [ ] Hold piece works
- [ ] Next piece preview shows
- [ ] Ghost piece shows
- [ ] Hard drop works
- [ ] Game over when blocks reach top

## Known Issues
- Wall kicks near edges can be tricky (test extensively)