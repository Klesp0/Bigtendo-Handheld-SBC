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
# If automatic calibration doesn't work well, you can manually set center values here
# Set to None to use automatic calibration, or set specific values
MANUAL_CENTER_X1 = None  # e.g., 32768
MANUAL_CENTER_Y1 = None  # e.g., 33450
MANUAL_CENTER_X2 = None  # e.g., 31890
MANUAL_CENTER_Y2 = None  # e.g., 32100
# ========================================

# ===== JOYSTICK CONFIGURATION =====
# Set these to True to invert axis direction if joystick is mounted rotated
INVERT_JOY1_X = True  # Change to True if left joystick X is backwards
INVERT_JOY1_Y = False  # Change to True if left joystick Y is backwards
INVERT_JOY2_X = False  # Change to True if right joystick X is backwards
INVERT_JOY2_Y = False  # Change to True if right joystick Y is backwards

# Top joystick is rotated 90° clockwise, so swap its axes
SWAP_JOY1_XY = True    # Top joystick is rotated
SWAP_JOY2_XY = False   # Bottom joystick is straight
# ===================================

# Setup Buttons - All 17 buttons configured
btn_pins = [
    board.D5, board.D6, board.D9, board.D10,       # Buttons 1-4
    board.D11, board.D12, board.D13, board.D24,    # Buttons 5-8
    board.D25, board.SCK, board.MOSI, board.MISO,  # Buttons 9-12
    board.RX, board.TX, board.SDA, board.SCL,      # Buttons 13-16
    board.D4,                                       # Button 17
]

buttons = []
for pin in btn_pins:
    b = digitalio.DigitalInOut(pin)
    b.direction = digitalio.Direction.INPUT
    b.pull = digitalio.Pull.UP
    buttons.append(b)
print(f"Initialized {len(buttons)} buttons")

# CALIBRATION: Read center position of joysticks
print("\n" + "="*60)
print("CALIBRATING JOYSTICKS...")
print("!!!! IMPORTANT: RELEASE ALL JOYSTICKS NOW !!!!")
print("Make sure joysticks are CENTERED (hands off!)")
print("Calibrating in 5 seconds...")
for i in range(5, 0, -1):
    print(f"  {i}...")
    time.sleep(1)

print("\nCalibrating... (taking 20 samples)")

# Take average of 20 readings for better accuracy
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

# Sanity check - warn if values look wrong
if center_x1 < 20000 or center_x1 > 45000:
    print("⚠ WARNING: Joystick 1 X center looks wrong!")
if center_y1 < 20000 or center_y1 > 45000:
    print("⚠ WARNING: Joystick 1 Y center looks wrong!")
if center_x2 < 20000 or center_x2 > 45000:
    print("⚠ WARNING: Joystick 2 X center looks wrong!")
if center_y2 < 20000 or center_y2 > 45000:
    print("⚠ WARNING: Joystick 2 Y center looks wrong!")

print("\nCalibration complete!")

# Apply manual overrides if set
if MANUAL_CENTER_X1 is not None:
    center_x1 = MANUAL_CENTER_X1
    print(f"  → Using MANUAL override for Joystick 1 X: {center_x1}")
if MANUAL_CENTER_Y1 is not None:
    center_y1 = MANUAL_CENTER_Y1
    print(f"  → Using MANUAL override for Joystick 1 Y: {center_y1}")
if MANUAL_CENTER_X2 is not None:
    center_x2 = MANUAL_CENTER_X2
    print(f"  → Using MANUAL override for Joystick 2 X: {center_x2}")
if MANUAL_CENTER_Y2 is not None:
    center_y2 = MANUAL_CENTER_Y2
    print(f"  → Using MANUAL override for Joystick 2 Y: {center_y2}")

print("="*60 + "\n")

prev_button_states = [True] * len(buttons)

def map_joystick_calibrated(value, center, invert=False):
    """
    Map 16-bit ADC value (0-65535) to -127 to 127 using calibrated center
    Args:
        value: Current ADC reading (0-65535)
        center: Calibrated center value (around 32768 for 16-bit)
        invert: If True, flip the direction
    """
    # Calculate distance from center
    offset = value - center

    # Invert if needed
    if invert:
        offset = -offset

    # Scale to -127 to 127 range
    # For 16-bit ADC, the range from center is about ±32768
    scaled = int((offset / 32768.0) * 127)

    # Clamp to valid range
    return max(-127, min(127, scaled))

def add_deadzone(value, deadzone=20):
    """Apply deadzone to reduce joystick drift - increased from 15 to 20"""
    if abs(value) < deadzone:
        return 0
    return value

print("Controller Ready!")
print("Move joysticks and press buttons to test")
if INVERT_JOY1_X or INVERT_JOY1_Y or INVERT_JOY2_X or INVERT_JOY2_Y:
    print("NOTE: Some axes are inverted based on configuration")
if SWAP_JOY1_XY or SWAP_JOY2_XY:
    print("NOTE: Some joystick axes are swapped based on configuration")
print("-"*60)
print("\nTIP: Watch the 'RAW' values in the output below.")
print("     When joysticks are centered, note those values.")
print("     If an axis doesn't read 0 on gamepad tester when centered,")
print("     use that RAW center value in MANUAL_CENTER_XX above.")
print("-"*60)

# Track for debug output
last_joy_print = 0

while True:
    try:
        # Read raw ADC values directly (0-65535 range - native 16-bit)
        raw_x1 = jx1.value
        raw_y1 = jy1.value
        raw_x2 = jx2.value
        raw_y2 = jy2.value

        # Map joystick values with inversion support
        x1 = add_deadzone(map_joystick_calibrated(raw_x1, center_x1, INVERT_JOY1_X))
        y1 = add_deadzone(map_joystick_calibrated(raw_y1, center_y1, INVERT_JOY1_Y))
        x2 = add_deadzone(map_joystick_calibrated(raw_x2, center_x2, INVERT_JOY2_X))
        y2 = add_deadzone(map_joystick_calibrated(raw_y2, center_y2, INVERT_JOY2_Y))

        # Swap axes if needed (for 90° or 270° rotated joysticks)
        if SWAP_JOY1_XY:
            x1, y1 = y1, x1
        if SWAP_JOY2_XY:
            x2, y2 = y2, x2

        # Send joystick data
        gp.move_joysticks(x=x1, y=y1, z=x2, r_z=y2)

        # Debug: Print joystick values occasionally
        current_time = time.monotonic()
        if current_time - last_joy_print > 1.0:  # Every 1 second (changed from 2)
            # Always show RAW values to help with calibration
            print(f"RAW: JX1={raw_x1:5} JY1={raw_y1:5} JX2={raw_x2:5} JY2={raw_y2:5} | Mapped: L({x1:4},{y1:4}) R({x2:4},{y2:4})")
            last_joy_print = current_time

        # Update button states
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
