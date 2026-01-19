# Software

## Structure
- `/games` - Individual game folders
- `/launcher` - Main menu system
- `/retropie_integration` - RetroPie launcher scripts
- `/standalone` - Standalone launcher (no RetroPie)

## Setup
```bash
pip3 install pygame
python3 -m pytest tests/
```

## Adding New Game
1. Create folder: `games/tool/your_game/`
2. Inherit from `shared.game_base.Game`
3. Implement: `handle_input()`, `update()`, `draw()`
4. Create launcher: `retropie_integration/YourGame.sh`
5. Add to menu: `launcher/main_menu.py`

## Testing
```bash
python3 games/snake/snake.py --windowed
python3 tests/test_all.py
```

## **📦 DEVELOPMENT ORDER & FILE DESCRIPTIONS**

### **Development Order (Priority)**

1. config.py           ← Start here (30 min) hotove, pise ze je ale je to ok AI
2. input_handler.py     ← Essential for input (1h) hotove, pise ze neni AI
3. save_system.py      ← Needed for high scores (1h) hotove, pise ze je AI na 60%
4. game_base.py        ← Foundation for all games (1.5h) hotove, pise ze neni AI
7. main_menu.py        ← Launcher system (2h)
8. retropie_launcher.py ← RetroPie integration (30 min)