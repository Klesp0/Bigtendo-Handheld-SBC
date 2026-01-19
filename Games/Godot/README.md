# Games

## Structure
Each game has its own folder:
```
games/
├── Pygame/
│   ├── snake/
│   ├── tetris/
│   ├── pong/
│   └── ...
└── Godot/
    ├── flappy/
    ├── platformer/
    └── ...
```

## Pygame Games
Located in `Pygame/` folder:
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

## Testing
```bash
# Test Pygame game:
python3 Pygame/snake/snake.py --windowed

# Test Godot game:
# Open in Godot Editor → Press F5
```

## Adding New Game
See [game_development_guide.md](../docs/game_development_guide.md)