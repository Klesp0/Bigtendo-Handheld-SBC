# Software


## Setup
```bash
pip3 install pygame
python3 -m pytest tests/
```
## Games

### Pygame Games
- **Snake** - Classic snake game
- **Tetris** - Block puzzle
- **Pong** - 2-player paddle game
- **Breakout** - Brick breaker
- **Space Invaders** - Retro shooter
- **Memory** - Card matching

### Godot Games
Located in `Godot/` folder:
- **Flappy Bird** - Side-scroller
- **Endless Runner** - Auto-runner
- **Platformer** - Jump & run
- **Pac-Man** - Maze chase
- **Rhythm** - Music timing
- **Top-Down Shooter** - Twin-stick shooter
- **Tower Defense** - Strategy

### Adding New Game
See [game_development_guide.md](../docs/game_development_guide.md)

## **Development Order (Priority)**

1. input_handler.py     ← remake to adafruit input
2. main_menu.py        ← Launcher system
3. retropie_launcher.py ← RetroPie integration