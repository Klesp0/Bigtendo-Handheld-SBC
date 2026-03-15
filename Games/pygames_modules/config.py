import pygame

# display set
WIDTH = 1024
HEIGHT = 600
FPS = 60
DPI = 170

GPIO_ENABLED = True

# =============================================================================
# GAMEPAD BUTTON MAP
# =============================================================================
# Pygame joystick buttons are 0-indexed.
# The Feather's code.py btn_pins list determines the HID button order:
#   HID Button 1 = btn_pins[0] → pygame index 0
#   HID Button 2 = btn_pins[1] → pygame index 1
#   ... etc.
#
# btn_pins order in code.py:
#   Index  GPIO  Physical
#     0     06   Arrow Left
#     1     08   A
#     2     09   B
#     3     10   X
#     4     11   Y
#     5     12   Menu Right Upper (START)
#     6     13   Menu Left Upper (HOME)
#     7     24   Left Joystick Button
#     8     07   Right Joystick Button
#     9     25   L2 (Left Lower Trigger)
#    10     18   L1 (Left Upper Trigger)
#    11     19   Menu Left Bottom (SELECT)
#    12     20   Arrow Down
#    13     01   Arrow Up
#    14     00   Arrow Right
#    15     02   R1 (Right Upper Trigger)
#    16     03   R2 (Right Lower Trigger)

GAMEPAD_BUTTON_MAP = {
    "LEFT":                 0,   # GPIO 06
    "A":                    1,   # GPIO 08
    "B":                    2,   # GPIO 09
    "X":                    3,   # GPIO 10
    "Y":                    4,   # GPIO 11
    "START":                5,   # GPIO 12
    "HOME":                 6,   # GPIO 13
    "JOYSTICK_BUTTON_L":    7,   # GPIO 24
    "JOYSTICK_BUTTON_R":    8,   # GPIO 07
    "L2":                   9,   # GPIO 25
    "L1":                  10,   # GPIO 18
    "MENU_L":              11,   # GPIO 19
    "DOWN":                12,   # GPIO 20
    "UP":                  13,   # GPIO 01
    "RIGHT":               14,   # GPIO 00
    "R1":                  15,   # GPIO 02
    "R2":                  16,   # GPIO 03
}

# =============================================================================
# GAMEPAD AXIS MAP
# =============================================================================
# Axes match move_joysticks(x=x1, y=y1, z=x2, r_z=y2) in code.py
# After swap: x1=left X, y1=left Y, x2=right X, y2=right Y
#
# Pygame axis indices follow HID descriptor order:
#   0 = x    (Joystick 0 X) → Left X  (after swap in firmware)
#   1 = y    (Joystick 0 Y) → Left Y  (after swap in firmware)
#   2 = z    (Joystick 1 X) → Right X
#   3 = r_z  (Joystick 1 Y) → Right Y

GAMEPAD_AXIS_MAP = {
    "LEFT_X":  0,   # x   axis
    "LEFT_Y":  1,   # y   axis
    "RIGHT_X": 2,   # z   axis
    "RIGHT_Y": 3,   # r_z axis
}

# JOYSTICKY
JOYSTICK_DEADZONE = 50
JOYSTICK_MAX = 1023
JOYSTICK_CENTER = 512
JOYSTICK_MIN = 0
JOYSTICK_SENSITIVITY = 1.0

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
SAVE_PATH = r"C:\Users\Lukáš\Desktop\Github\Programovanie\Bigtendo-Handheld-SBC\Games\saves\highscores.json"
HIGHSCORES_TIME_FILE = SAVE_PATH + "\highscores.json"
SETTINGS_FILE = SAVE_PATH + "\settings"

if __name__ == "__main__":
    print(f"Screen: {WIDTH}x{HEIGHT}")
    print(f"FPS: {FPS}")
    print(f"Save path: {SAVE_PATH}")