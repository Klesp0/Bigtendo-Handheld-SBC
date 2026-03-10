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
# Left joystick:  A1=VRx (X-os),  A0=VRy (Y-os)
# Right joystick: A2=VRx (X-os),  A3=VRy (Y-os)
jx1 = analogio.AnalogIn(board.A1)  # lavy joystick X
jy1 = analogio.AnalogIn(board.A0)  # lavy joystick Y
jx2 = analogio.AnalogIn(board.A2)  # pravy joystick X
jy2 = analogio.AnalogIn(board.A3)  # pravy joystick Y
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

# Osi su spravne priradene podla zapojenia, swap nie je potrebny
SWAP_JOY1_XY = True
SWAP_JOY2_XY = False

btn_pins = [
    board.D6,    
    board.D9,    
    board.D10,   
    board.D11,   
    board.RX,    
    board.MISO,  
    board.D4,    
    board.TX,    
    board.SCK,   
    board.SDA,   
    board.D24,   
    board.SCL,   
    board.D12,   
    board.D13,   
    board.MOSI,  
    board.D5,    
    board.D25,   
]

buttons = []
for pin in btn_pins:
    b = digitalio.DigitalInOut(pin)
    b.direction = digitalio.Direction.INPUT
    b.pull = digitalio.Pull.UP
    buttons.append(b)
print(f"Initialized {len(buttons)} buttons")

# KALIBRÁCIA joystickov
print("\n" + "="*60)
print("CALIBRATING JOYSTICKS...")
print("!!!! DOLEZITE: PUST JOYSTICKY !!!!")
print("Joysticky musia byt VYCENTROVANE (ruky prec!)")
print("Kalibracia za 5 sekund...")
for i in range(5, 0, -1):
    print(f"  {i}...")
    time.sleep(1)

print("\nKalibrujem... (20 vzoriek)")

center_x1, center_y1 = 0, 0
center_x2, center_y2 = 0, 0

for i in range(20):
    center_x1 += jx1.value
    center_y1 += jy1.value
    center_x2 += jx2.value
    center_y2 += jy2.value
    time.sleep(0.05)
    if (i + 1) % 5 == 0:
        print(f"  Vzorka {i+1}/20...")

center_x1 //= 20
center_y1 //= 20
center_x2 //= 20
center_y2 //= 20

print("\n" + "-"*60)
print("VYSLEDKY KALIBRACIE:")
print(f"  Lavy joystick:  X = {center_x1:5}  Y = {center_y1:5}")
print(f"  Pravy joystick: X = {center_x2:5}  Y = {center_y2:5}")
print("-"*60)

if center_x1 < 20000 or center_x1 > 45000:
    print("VAROVANIE: Lavy joystick X center vyzera zle!")
if center_y1 < 20000 or center_y1 > 45000:
    print("VAROVANIE: Lavy joystick Y center vyzera zle!")
if center_x2 < 20000 or center_x2 > 45000:
    print("VAROVANIE: Pravy joystick X center vyzera zle!")
if center_y2 < 20000 or center_y2 > 45000:
    print("VAROVANIE: Pravy joystick Y center vyzera zle!")

print("\nKalibracia hotova!")

if MANUAL_CENTER_X1 is not None:
    center_x1 = MANUAL_CENTER_X1
    print(f"  -> Pouzivam MANUAL override pre lavy X: {center_x1}")
if MANUAL_CENTER_Y1 is not None:
    center_y1 = MANUAL_CENTER_Y1
    print(f"  -> Pouzivam MANUAL override pre lavy Y: {center_y1}")
if MANUAL_CENTER_X2 is not None:
    center_x2 = MANUAL_CENTER_X2
    print(f"  -> Pouzivam MANUAL override pre pravy X: {center_x2}")
if MANUAL_CENTER_Y2 is not None:
    center_y2 = MANUAL_CENTER_Y2
    print(f"  -> Pouzivam MANUAL override pre pravy Y: {center_y2}")

print("="*60 + "\n")

prev_button_states = [True] * len(buttons)

def map_joystick_calibrated(value, center, invert=False):
    """
    Mapuje 16-bit ADC hodnotu (0-65535) na -127 az 127 pomocou kalibrovaného stredu.
    """
    offset = value - center
    if invert:
        offset = -offset
    scaled = int((offset / 32768.0) * 127)
    return max(-127, min(127, scaled))

def add_deadzone(value, deadzone=20):
    """Aplikuje deadzone pre znizenie driftu joysticku."""
    if abs(value) < deadzone:
        return 0
    return value

print("Kontroler pripraveny!")
print("Pohni joysticky a stlac tlacidla pre test")
print("-"*60)
print("TIP: Sleduj hodnoty 'RAW' nizsie.")
print("     Ked su joysticky vycentrovane, poznac si hodnoty.")
print("     Ak osa neukazuje 0 v strede, zadaj hodnotu do MANUAL_CENTER_XX.")
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
                    print(f">>> Button {i+1} STLACENE <<<")
                else:
                    gp.release_buttons(i + 1)
                    print(f">>> Button {i+1} PUSTENE <<<")
                prev_button_states[i] = current_state

        time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nZastavujem kontroler...")
        gp.reset_all()
        break
    except Exception as e:
        print(f"Chyba: {e}")
        time.sleep(0.1)