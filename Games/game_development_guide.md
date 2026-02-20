# Adding a New Game

## 2. Test Standalone
```bash
python3 your_game.py --windowed
```

## 3. Create RetroPie Launcher
```bash
# SW/retropie_integration/YourGame.sh
#!/bin/bash
cd /home/pi/RetroPie/roms/ports/games/your_game/
python3 your_game.py
exit 0
```

## 4. Add to Menu
Edit `SW/launcher/main_menu.py`:
```python
games = [
    {"name": "Snake", "class": SnakeGame},
    {"name": "Your Game", "class": YourGame},  # ADD THIS
]
```

## Best Practices
- Add `--windowed` flag for PC testing