# Games

## Pygame Games
- **Snake** - Classic snake game
- **Tetris** - Block puzzle
- **Pong** - 2-player paddle game
- **Breakout** - Brick breaker
- **Space Invaders** - Retro shooter
- **Memory** - Card matching

## Godot Games
Located in `Godot/` folder:
- **Flappy Bird** - Side-scroller
- **Endless Runner** - Auto-runner
- **Platformer** - Jump & run
- **Pac-Man** - Maze chase
- **Rhythm** - Music timing
- **Top-Down Shooter** - Twin-stick shooter
- **Tower Defense** - Strategy

## Adding New Game
See [game_development_guide.md](../docs/game_development_guide.md)

## Adding a New Game

### 2. Add to Standalone

Edit `SW/launcher/main_menu.py`:
```python
games = [
    {"name": "Snake", "class": SnakeGame},
    {"name": "Your Game", "class": YourGame},  # ADD THIS
]

```
## RetroPie Integration

### Troubleshooting

**Game doesn't appear in Ports:**
- Check .sh file has execute permission: `chmod +x`
- Verify file location: `/home/pi/RetroPie/roms/ports/GameName.sh`
- Restart EmulationStation

**Game crashes:**
- Test standalone first: `python3 gamename.py`
- Check dependencies: `pip3 install pygame`
- View logs: Check terminal output

**Icon doesn't show:**
- Verify path: `/home/pi/.emulationstation/downloaded_media/ports/GameName.png`
- Name must match exactly (case-sensitive)
- Restart ES after adding icons