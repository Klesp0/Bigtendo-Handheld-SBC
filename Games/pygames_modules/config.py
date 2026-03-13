import pygame

# display set
WIDTH = 1024
HEIGHT = 600
FPS = 60
DPI = 170

GPIO_ENABLED = True

GAMEPAD_BUTTON_MAP = {
    "A":            0,   # GPIO08
    "B":            1,   # GPIO09
    "X":            2,   # GPIO10
    "Y":            3,   # GPIO11
    "UP":           4,   # GPIO01
    "DOWN":         5,   # GPIO20
    "LEFT":         6,   # GPIO06
    "RIGHT":        7,   # GPIO00
    "L1":           8,   # GPIO18 (upper left trigger)
    "R1":           9,   # GPIO02 (upper right trigger)
    "L2":           10,  # GPIO25 (lower left trigger)
    "R2":           11,  # GPIO03 (lower right trigger)
    "START":        12,  # GPIO12 (right upper menu button)
    "HOME":         13,  # GPIO13 (left upper menu button)
    "JOYSTICK_BUTTON_L": 14,  # GPIO24
    "JOYSTICK_BUTTON_R": 15,  # GPIO07
    "MENU_L":       16,  # GPIO19 (left bottom menu button)
}

GAMEPAD_AXIS_MAP = {
    "LEFT_X":  0,  # x   - lavy joystick X  (GPIO29 / A3)
    "LEFT_Y":  1,  # y   - lavy joystick Y  (GPIO28 / A2)
    "RIGHT_X": 2,  # z   - pravy joystick X (GPIO27 / A1)
    "RIGHT_Y": 3,  # r_z - pravy joystick Y (GPIO26 / A0)
}

# JOYSTICKY
# analogovy joystick 0-1023
JOYSTICK_DEADZONE = 50
JOYSTICK_MAX = 1023
JOYSTICK_CENTER = 512
JOYSTICK_MIN = 0
JOYSTICK_SENSITIVITY = 1.0  # ked stihneme tak bude v nastaveniach

# KLAVESNICA
WASD = False
KEYBOARD_ENABLED = True

KEYBOARD_SIPKY = {
    # sipky
    "UP": pygame.K_UP,
    "DOWN": pygame.K_DOWN,
    "RIGHT": pygame.K_RIGHT,
    "LEFT": pygame.K_LEFT,

    # pismenka
    "A": pygame.K_SPACE,
    "B": pygame.K_b,
    "X": pygame.K_x,
    "Y": pygame.K_y,

    # menu
    "START": pygame.K_RETURN,
    "HOME": pygame.K_ESCAPE,
    "MENU_L": pygame.K_TAB,

    # packy
    "L1": pygame.K_q,
    "R1": pygame.K_e,
    "L2": pygame.K_1,
    "R2": pygame.K_2,

    # joystick button
    "JOYSTICK_BUTTON_R": pygame.K_b,
    "JOYSTICK_BUTTON_L": pygame.K_n,

    "JOYSTICKR_X": {"+": pygame.K_o, "-": pygame.K_o},
    "JOYSTICKL_X": {"+": pygame.K_o, "-": pygame.K_o},
    "JOYSTICKR_Y": {"+": pygame.K_o, "-": pygame.K_o},
    "JOYSTICKL_Y": {"+": pygame.K_o, "-": pygame.K_o},

    # on/off
    "ON_OFF": pygame.K_F12,

    # volume
    "VOLUME_UP": pygame.K_MINUS,
    "VOLUME_DOWN": pygame.K_PLUS
}

KEYBOARD_WASD = {
    # wasd
    "UP": pygame.K_w,
    "DOWN": pygame.K_s,
    "LEFT": pygame.K_a,
    "RIGHT": pygame.K_d,

    # pismenka
    "A": pygame.K_SPACE,
    "B": pygame.K_j,
    "X": pygame.K_k,
    "Y": pygame.K_l,

    # menu
    "START": pygame.K_RETURN,
    "HOME": pygame.K_ESCAPE,
    "MENU_L": pygame.K_TAB,

    # packy
    "L1": pygame.K_q,
    "R1": pygame.K_e,
    "L2": pygame.K_1,
    "R2": pygame.K_2,

    # joystick button
    "JOYSTICK_BUTTON_R": pygame.K_b,
    "JOYSTICK_BUTTON_L": pygame.K_n,

    "JOYSTICKR_X": {"+": pygame.K_o, "-": pygame.K_o},
    "JOYSTICKL_X": {"+": pygame.K_o, "-": pygame.K_o},
    "JOYSTICKR_Y": {"+": pygame.K_o, "-": pygame.K_o},
    "JOYSTICKL_Y": {"+": pygame.K_o, "-": pygame.K_o},

    # on/off
    "ON_OFF": pygame.K_F12,

    # volume
    "VOLUME_UP": pygame.K_MINUS,
    "VOLUME_DOWN": pygame.K_PLUS
}

# FPS
SHOW_FPS = False

# AUDIO
SOUND_ENABLED = True
MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.7

# battery management
BATTERY_WARNING_LEVEL = 15
BATTERY_CRITICAL_LEVEL = 5
AUTO_SLEEP_TIMEOUT = 300  # sekundy

# console info
CONSOLE_NAME = "Bigtendo"
CONSOLE_VERSION = "1.0"
TEAM_NAME = "Majstri Kresťania"

GAMES = {
    "Snake":          {"engine": "Pygame", "difficulty": 2},
    "Pong":           {"engine": "Pygame", "difficulty": 2},
    "Breakout":       {"engine": "Pygame", "difficulty": 3},
    "Tetris":         {"engine": "Pygame", "difficulty": 4},
    "Pexeso":         {"engine": "Pygame", "difficulty": 2},
    "Space Invaders": {"engine": "Pygame", "difficulty": 4},

    "Flappy Bird":    {"engine": "Godot", "difficulty": 3},
    "Endless Runner": {"engine": "Godot", "difficulty": 3},
    "Platformer":     {"engine": "Godot", "difficulty": 4},
    "Pac-Man":        {"engine": "Godot", "difficulty": 5},
    "Rhythm Game":    {"engine": "Godot", "difficulty": 4},
    "Top-Down Shooter": {"engine": "Godot", "difficulty": 4},
    "Tower Defense":  {"engine": "Godot", "difficulty": 5}
}

# Save data path
SAVE_PATH = r"C:\Users\Lukáš\Desktop\Github\Programovanie\Bigtendo-Handheld-SBC\Games\saves"
HIGHSCORES_TIME_FILE = SAVE_PATH + "\highscores_times.json"
SETTINGS_FILE = SAVE_PATH + "\settings"

if __name__ == "__main__":
    print(f"Screen: {WIDTH}x{HEIGHT}")
    print(f"FPS: {FPS}")
    print(f"Save path: {SAVE_PATH}")