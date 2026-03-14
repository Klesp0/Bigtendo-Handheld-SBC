import pygame

# display set
WIDTH = 1024
HEIGHT = 600
FPS = 60
DPI = 170

GPIO_ENABLED = True

# Button indices match btn_pins order in the original code.py:
# board.D5, board.D6, board.D9, board.D10,
# board.D11, board.D12, board.D13, board.D24,
# board.D25, board.SCK, board.MOSI, board.MISO,
# board.RX, board.TX, board.SDA, board.SCL,
# board.D4
#
# Index  GPIO  Pin        Button
#   0    05    D5         (unassigned - spare)
#   1    06    D6         LEFT
#   2    09    D9         B
#   3    10    D10        X
#   4    11    D11        Y
#   5    12    D12        START
#   6    13    D13        HOME
#   7    24    D24        JOYSTICK_BUTTON_L
#   8    25    D25        L2 lower left
#   9    18    SCK        L1 upper left
#  10    19    MOSI       MENU_L
#  11    20    MISO       DOWN
#  12    01    RX         UP
#  13    00    TX         RIGHT
#  14    02    SDA        R1 upper right
#  15    03    SCL        R2 lower right
#  16    04    D4         (unassigned - spare)
#
# NOTE: A (GPIO08) and JOYSTICK_BUTTON_R (GPIO07) are NOT wired
# in the original code.py — add them if you extend btn_pins later.

GAMEPAD_BUTTON_MAP = {
    "B":                    1,   # GPIO09 / D9
    "X":                    2,   # GPIO10 / D10
    "Y":                    3,   # GPIO11 / D11
    "LEFT":                 0,   # GPIO06 / D6   (index 1, but kept 0-based = 1 in gp.press_buttons)
    "START":                4,   # GPIO12 / D12
    "HOME":                 5,   # GPIO13 / D13
    "JOYSTICK_BUTTON_L":    6,   # GPIO24 / D24
    "L2":                   7,   # GPIO25 / D25
    "L1":                   8,   # GPIO18 / SCK
    "MENU_L":               9,   # GPIO19 / MOSI
    "DOWN":                10,   # GPIO20 / MISO
    "UP":                  11,   # GPIO01 / RX
    "RIGHT":               12,   # GPIO00 / TX
    "R1":                  13,   # GPIO02 / SDA
    "R2":                  14,   # GPIO03 / SCL
}

# Axis indices match move_joysticks() call in original code.py:
#   gp.move_joysticks(x=x1, y=y1, z=x2, r_z=y2)
# where jx1=A0(GPIO26), jy1=A1(GPIO27), jx2=A2(GPIO29), jy2=A3(GPIO28)
#
# From wiring: GPIO26=A0=Right VRy, GPIO27=A1=Right VRx
#              GPIO29=A2=Left  VRy, GPIO28=A3=Left  VRx  (best guess from pinout)
GAMEPAD_AXIS_MAP = {
    "RIGHT_Y": 0,  # x   - A0 (GPIO26)
    "RIGHT_X": 1,  # y   - A1 (GPIO27)
    "LEFT_Y":  2,  # z   - A2 (GPIO29)
    "LEFT_X":  3,  # r_z - A3 (GPIO28)
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
SAVE_PATH = r"C:\Users\Lukáš\Desktop\Github\Programovanie\Bigtendo-Handheld-SBC\Games\saves"
HIGHSCORES_TIME_FILE = SAVE_PATH + "\highscores.json"
SETTINGS_FILE = SAVE_PATH + "\settings"

if __name__ == "__main__":
    print(f"Screen: {WIDTH}x{HEIGHT}")
    print(f"FPS: {FPS}")
    print(f"Save path: {SAVE_PATH}")