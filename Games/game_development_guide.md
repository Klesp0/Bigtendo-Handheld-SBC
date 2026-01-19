# Game Development Guide

## Adding a New Game

### 1. Create Game File
```python
#!/usr/bin/env python3
"""
Your Game - Description
"""
import pygame
import sys
import os

# Add parent to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.game_base import Game
from shared.config import *
from shared.save_system import save_system
from shared.gpio_handler import input_handler

class YourGame(Game):
    def __init__(self, screen=None, fullscreen=True):
        super().__init__(screen, fullscreen)
        # Your initialization
        self.player_x = 100
        self.score = 0
    
    def handle_input(self):
        """Handle keyboard/GPIO"""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or input_handler.is_pressed('LEFT'):
            self.player_x -= 5
        
        if keys[pygame.K_RIGHT] or input_handler.is_pressed('RIGHT'):
            self.player_x += 5
    
    def update(self):
        """Update game logic"""
        # Collision detection
        # Score calculation
        # Game over check
        pass
    
    def draw(self):
        """Draw to screen"""
        self.screen.fill(BLACK)
        
        # Draw player
        pygame.draw.rect(self.screen, GREEN, (self.player_x, 240, 50, 50))
        
        # Draw score
        font = pygame.font.Font(None, 48)
        text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(text, (10, 10))

if __name__ == "__main__":
    game = YourGame(fullscreen=False)
    game.run()
```

### 2. Test Standalone
```bash
python3 your_game.py --windowed
```

### 3. Create RetroPie Launcher
```bash
# SW/retropie_integration/YourGame.sh
#!/bin/bash
cd /home/pi/RetroPie/roms/ports/games/your_game/
python3 your_game.py
exit 0
```

### 4. Add to Menu
Edit `SW/launcher/main_menu.py`:
```python
games = [
    {"name": "Snake", "class": SnakeGame},
    {"name": "Your Game", "class": YourGame},  # ADD THIS
]
```

## Best Practices
- Always inherit from `Game` base class
- Use `shared.config` for constants
- Support both keyboard AND GPIO
- Save high scores with `save_system`
- Test standalone before RetroPie
- Keep FPS at 60
- Add `--windowed` flag for PC testing