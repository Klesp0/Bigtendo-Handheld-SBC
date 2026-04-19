import board
import digitalio
import analogio
import usb_hid
from adafruit_hid.gamepad import Gamepad
import time

print("Initializing controller...")

# Initialize Gamepad
gp = Gamepad(usb_hid.devices)
print("Gamepad initialized successfully")

# Setup Joysticks (Analog pins)
jx1 = analogio.AnalogIn(board.A0)
jy1 = analogio.AnalogIn(board.A1)
jx2 = analogio.AnalogIn(board.A2)
jy2 = analogio.AnalogIn(board.A3)
print("Joysticks initialized")

# ===== MANUAL CALIBRATION OVERRIDE =====
MANUAL_CENTER_X1 = None
MANUAL_CENTER_Y1 = None
MANUAL_CENTER_X2 = None
MANUAL_CENTER_Y2 = None
# ========================================

# ===== JOYSTICK CONFIGURATION =====
INVERT_JOY1_X = True
INVERT_JOY1_Y = False
INVERT_JOY2_X = False
INVERT_JOY2_Y = False

SWAP_JOY1_XY = True
SWAP_JOY2_XY = False
# ===================================

# Setup Buttons - 17 buttons configured
# Each button's position in this list = its HID button number (1-indexed)
# So btn_pins[0] = HID Button 1, btn_pins[1] = HID Button 2, etc.
#
# Index  Pin       GPIO  Physical button
#   0    D6        06    Arrow Left
#   1    D8        08    A
#   2    D9        09    B
#   3    D10       10    X
#   4    D11       11    Y
#   5    D12       12    Menu Right Upper (START)
#   6    D13       13    Menu Left Upper (HOME)
#   7    D24       24    Left Joystick Button
#   8    D7        07    Right Joystick Button
#   9    D25       25    L2 (Left Lower Trigger)
#  10    SCK       18    L1 (Left Upper Trigger)
#  11    MOSI      19    Menu Left Bottom (SELECT)
#  12    MISO      20    Arrow Down
#  13    RX        01    Arrow Up
#  14    TX        00    Arrow Right
#  15    SDA       02    R1 (Right Upper Trigger)
#  16    SCL       03    R2 (Right Lower Trigger)
btn_pins = [
    board.D6,                                       # 0:  Arrow Left
    board.D8,                                       # 1:  A          *** NEW ***
    board.D9,                                       # 2:  B
    board.D10,                                      # 3:  X
    board.D11,                                      # 4:  Y
    board.D12,                                      # 5:  Menu Right Upper (START)
    board.D13,                                      # 6:  Menu Left Upper (HOME)
    board.D24,                                      # 7:  Left Joystick Button
    board.D7,                                       # 8:  Right Joystick Button *** NEW ***
    board.D25,                                      # 9:  L2
    board.SCK,                                      # 10: L1
    board.MOSI,                                     # 11: Menu Left Bottom (SELECT)
    board.MISO,                                     # 12: Arrow Down
    board.RX,                                       # 13: Arrow Up
    board.TX,                                       # 14: Arrow Right
    board.SDA,                                      # 15: R1
    board.SCL,                                      # 16: R2
]

buttons = []
for pin in btn_pins:
    b = digitalio.DigitalInOut(pin)
    b.direction = digitalio.Direction.INPUT
    b.pull = digitalio.Pull.UP
    buttons.append(b)
print(f"Initialized {len(buttons)} buttons")

# CALIBRATION
print("\n" + "="*60)
print("CALIBRATING JOYSTICKS...")
print("!!!! IMPORTANT: RELEASE ALL JOYSTICKS NOW !!!!")
print("Calibrating in 5 seconds...")
for i in range(5, 0, -1):
    print(f"  {i}...")
    time.sleep(1)

print("\nCalibrating... (taking 20 samples)")

center_x1, center_y1 = 0, 0
center_x2, center_y2 = 0, 0

for i in range(20):
    center_x1 += jx1.value
    center_y1 += jy1.value
    center_x2 += jx2.value
    center_y2 += jy2.value
    time.sleep(0.05)
    if (i + 1) % 5 == 0:
        print(f"  Sample {i+1}/20...")

center_x1 //= 20
center_y1 //= 20
center_x2 //= 20
center_y2 //= 20

print("\n" + "-"*60)
print("CALIBRATION RESULTS:")
print(f"  Joystick 1 (Top):    X = {center_x1:5}  Y = {center_y1:5}")
print(f"  Joystick 2 (Bottom): X = {center_x2:5}  Y = {center_y2:5}")
print("-"*60)

if center_x1 < 20000 or center_x1 > 45000:
    print("WARNING: Joystick 1 X center looks wrong!")
if center_y1 < 20000 or center_y1 > 45000:
    print("WARNING: Joystick 1 Y center looks wrong!")
if center_x2 < 20000 or center_x2 > 45000:
    print("WARNING: Joystick 2 X center looks wrong!")
if center_y2 < 20000 or center_y2 > 45000:
    print("WARNING: Joystick 2 Y center looks wrong!")

print("\nCalibration complete!")

if MANUAL_CENTER_X1 is not None:
    center_x1 = MANUAL_CENTER_X1
    print(f"  -> Using MANUAL override for Joystick 1 X: {center_x1}")
if MANUAL_CENTER_Y1 is not None:
    center_y1 = MANUAL_CENTER_Y1
    print(f"  -> Using MANUAL override for Joystick 1 Y: {center_y1}")
if MANUAL_CENTER_X2 is not None:
    center_x2 = MANUAL_CENTER_X2
    print(f"  -> Using MANUAL override for Joystick 2 X: {center_x2}")
if MANUAL_CENTER_Y2 is not None:
    center_y2 = MANUAL_CENTER_Y2
    print(f"  -> Using MANUAL override for Joystick 2 Y: {center_y2}")

print("="*60 + "\n")

prev_button_states = [True] * len(buttons)

def map_joystick_calibrated(value, center, invert=False):
    offset = value - center
    if invert:
        offset = -offset
    scaled = int((offset / 32768.0) * 127)
    return max(-127, min(127, scaled))

def add_deadzone(value, deadzone=20):
    if abs(value) < deadzone:
        return 0
    return value

print("Controller Ready!")
print(f"Buttons: {len(buttons)}")
if INVERT_JOY1_X or INVERT_JOY1_Y or INVERT_JOY2_X or INVERT_JOY2_Y:
    print("NOTE: Some axes are inverted")
if SWAP_JOY1_XY or SWAP_JOY2_XY:
    print("NOTE: Some joystick axes are swapped")
print("-"*60)

last_joy_print = 0

while True:
    try:
        raw_x1 = jx1.value
        raw_y1 = jy1.value
        raw_x2 = jx2.value
        raw_y2 = jy2.value

        x1 = add_deadzone(map_joystick_calibrated(raw_x1, center_x1, INVERT_JOY1_X))
        y1 = add_deadzone(map_joystick_calibrated(raw_y1, center_y1, INVERT_JOY1_Y))
        x2 = add_deadzone(map_joystick_calibrated(raw_x2, center_x2, INVERT_JOY2_X))
        y2 = add_deadzone(map_joystick_calibrated(raw_y2, center_y2, INVERT_JOY2_Y))

        if SWAP_JOY1_XY:
            x1, y1 = y1, x1
        if SWAP_JOY2_XY:
            x2, y2 = y2, x2

        gp.move_joysticks(x=x1, y=y1, z=x2, r_z=y2)

        current_time = time.monotonic()
        if current_time - last_joy_print > 1.0:
            print(f"RAW: JX1={raw_x1:5} JY1={raw_y1:5} JX2={raw_x2:5} JY2={raw_y2:5} | Mapped: L({x1:4},{y1:4}) R({x2:4},{y2:4})")
            last_joy_print = current_time

        for i in range(len(buttons)):
            current_state = buttons[i].value
            if current_state != prev_button_states[i]:
                if not current_state:
                    gp.press_buttons(i + 1)
                    print(f">>> Button {i+1} PRESSED <<<")
                else:
                    gp.release_buttons(i + 1)
                    print(f">>> Button {i+1} RELEASED <<<")
                prev_button_states[i] = current_state

        time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nStopping controller...")
        gp.reset_all()
        break
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(0.1)
