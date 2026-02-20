````markdown
# 🟦 Tetris

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