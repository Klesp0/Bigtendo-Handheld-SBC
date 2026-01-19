from pathlib import Path
import pygame

# display set
WIDTH = 1024
HEIGHT = 600
FPS = 60
DPI = 170

# 90- place holder
# GPIO pins
GPIO_ENABLED = True

GPIO_PINS = {
    # pismenka
    "A": 90,
    "X": 90,
    "B": 90,
    "Y": 90,
    
    # sipky
    "DOWN": 90,
    "LEFT": 90,
    "RIGHT": 90,
    "UP": 90,
    
    # packy, nakonci
    "R2": 90,
    "R1": 90,
    "L2": 90,
    "L1": 90,
        
    # menu
    "START": 90,
    "HOME": 90,
            
    # joysticky
    "JOYSTICK_BUTTON_R": 90,
    "JOYSTICK_BUTTON_L": 90,
    
    "JOYSTICKR_X": 90,
    "JOYSTICKL_X": 90,
    
    "JOYSTICKR_Y": 90,
    "JOYSTICKL_Y": 90,
        
    # vibrovac
    "VIBRATION_MOTOR": 90,
        
    # ON/OFF
    "ON_OFF": 90,
        
    # volume
    "VOLUME_UP": 90,
    "VOLUME_DOWN": 90
}

# JOYSTICKY
# analogovy joystick 0-1023
JOYSTICK_DEADZONE = 50 # kolko nereaguje, ignoruje small movements
JOYSTICK_MAX = 1023
JOYSTICK_CENTER = 512
JOYSTICK_MIN = 0
JOYSTICK_SENSITIVITY = 1.0 # ked stihneme tak bude v nastaveniach

# KLAVESNICA
WASD = False
KEYBOARD_ENABLED = True

# MOZNO UROBIT CUSTOM BINDY
# napisat nejake dobre default bindy

KEYBOARD_SIPKY = {
    # sipky
    "UP": pygame.K_UP,
    "DOWN" : pygame.K_DOWN,
    "RIGHT": pygame.K_RIGHT,
    "LEFT": pygame.K_LEFT,
    
    # pismenka
    "A": pygame.K_SPACE,
    "B": pygame.K_b,
    "X": pygame.K_x,
    "Y": pygame.K_y,
    
    # menu
    "START": pygame.K_RETURN, # enter
    "HOME": pygame.K_ESCAPE,
    
    # packy
    "L1": pygame.K_q,          
    "R1": pygame.K_e,           
    "L2": pygame.K_1,          
    "R2": pygame.K_2,
    
    # joystick button
    "JOYSTICK_BUTTON_R": pygame.K_b,
    "JOYSTICK_BUTTON_L": pygame.K_n,
    
    "JOYSTICKR_X": {
        "+": pygame.K_o,
        "-": pygame.K_o
        },
    "JOYSTICKL_X": {
        "+": pygame.K_o,
        "-": pygame.K_o
        },
    
    "JOYSTICKR_Y": {
        "+": pygame.K_o,
        "-": pygame.K_o
        },
    "JOYSTICKL_Y": {
        "+": pygame.K_o,
        "-": pygame.K_o
        },
    
    # on/off
    "ON_OFF": pygame.K_F12,
    
    # volume
    "VOLUME_UP": pygame.K_MINUS,
    "VOLUME_DOWN": pygame.K_PLUS
    
}

# tiez urobit nejake dobre default bindy
KEYBOARD_WASD = {
    # wasd
    "UP": pygame.K_w,
    "DOWN": pygame.K_s,
    "LEFT": pygame.K_a,
    "RIGHT" : pygame.K_d,
    
    # pismenka
    "A": pygame.K_SPACE,
    "B": pygame.K_j,
    "X": pygame.K_k,
    "Y": pygame.K_l,
    
    # menu
    "START": pygame.K_RETURN, # enter
    "HOME": pygame.K_ESCAPE,
    
    # packy
    "L1": pygame.K_q,          
    "R1": pygame.K_e,           
    "L2": pygame.K_1,          
    "R2": pygame.K_2,
    
    # joystick button
    "JOYSTICK_BUTTON_R": pygame.K_b,
    "JOYSTICK_BUTTON_L": pygame.K_n,
    
    "JOYSTICKR_X": {
        "+": pygame.K_o,
        "-": pygame.K_o
        },
    "JOYSTICKL_X": {
        "+": pygame.K_o,
        "-": pygame.K_o
        },
    
    "JOYSTICKR_Y": {
        "+": pygame.K_o,
        "-": pygame.K_o
        },
    "JOYSTICKL_Y": {
        "+": pygame.K_o,
        "-": pygame.K_o
        },
    
    # on/off
    "ON_OFF": pygame.K_F12,
    
    # volume
    "VOLUME_UP": pygame.K_MINUS,
    "VOLUME_DOWN": pygame.K_PLUS
    
}

# FPS
# ked bude cas urobit
SHOW_FPS = False 

# AUDIO
# ked bude cas
SOUND_ENABLED = True
MUSIC_VOLUME = 0.5  
SFX_VOLUME = 0.7

# batery managment
# ked bude cas
BATTERY_WARNING_LEVEL = 15  
BATTERY_CRITICAL_LEVEL = 5  
AUTO_SLEEP_TIMEOUT = 300 #sekundy

# console info
CONSOLE_NAME = "Bigtendo"
CONSOLE_VERSION = "1.0"
TEAM_NAME = "Majstri Kresťania"

# Game dict
# NoHit bude mat 5 hviezd inej farby pre extra difficulty

GAMES = {
    "Snake": {"engine": "Pygame", "difficulty": 2},
    "Pong": {"engine": "Pygame", "difficulty": 2},
    "Breakout": {"engine": "Pygame", "difficulty": 3},
    "Tetris": {"engine": "Pygame", "difficulty": 4},
    "Pexeso": {"engine": "Pygame", "difficulty": 2},
    "Space Invaders": {"engine": "Pygame", "difficulty": 4},
    
    "Flappy Bird": {"engine": "Godot", "difficulty": 3},
    "Endless Runner": {"engine": "Godot", "difficulty": 3},
    "Platformer": {"engine": "Godot", "difficulty": 4},
    "Pac-Man": {"engine": "Godot", "difficulty": 5},
    "Rhythm Game": {"engine": "Godot", "difficulty": 4},
    "Top-Down Shooter": {"engine": "Godot", "difficulty": 4},
    "Tower Defense": {"engine": "Godot", "difficulty": 5},
    "NoHit": {"engine": "Godot", "difficulty": 6},
    
}

# potrebne paths

# k priecinku, abs
PROJECT_PATH = Path(__file__).parent.parent

# k assets(relative podla Poject path)
ASSETS_PATH = PROJECT_PATH / "Design" / "assets"
IMAGES_PATH = ASSETS_PATH / "images"
SOUNDS_PATH = ASSETS_PATH / "sounds"
FONTS_PATH = ASSETS_PATH / "fonts"

# Game paths
GAMES_PATH = PROJECT_PATH / "SW" / "games"
PYGAME_GAMES_PATH = GAMES_PATH / "Pygame"
GODOT_GAMES_PATH = GAMES_PATH / "Godot"

# Save data path
SAVE_PATH = PROJECT_PATH / "saves"
HIGHSCORES_TIME_FILE = SAVE_PATH / "highscores_times.json"
SETTINGS_FILE = SAVE_PATH / "settings"

# Test
if __name__ == "__main__":
    print(f"Screen: {WIDTH}x{HEIGHT}")
    print(f"FPS: {FPS}")
    print(f"Controller UP pin: {GPIO_PINS['UP']}")
    print(f"Save path: {SAVE_PATH}")