import pygame
import serial
import json
import threading
from config import *
import time


def find_feather_port():
    """Automaticky najde Feather podla VID/PID."""
    for port in serial.tools.list_ports.comports():
        # Adafruit Feather RP2040 VID:PID
        if "239A" in port.hwid.upper():
            return port.device
    return None


class InputHandler:
    def __init__(self):
        self._state = {}
        self._last_state = {}
        self._lock = threading.Lock()

        self.feather = None
        self._reader_thread = None

        port = find_feather_port()
        if port:
            try:
                self.feather = serial.Serial(port, baudrate=115200, timeout=1)
                # citanie v osobnom threade aby neblokovalo hlavny loop
                self._reader_thread = threading.Thread(
                    target=self._read_loop, daemon=True
                )
                self._reader_thread.start()
                print(f"Feather pripojeny na {port}")
            except Exception as e:
                print(f"Feather sa nepodarilo pripojit: {e}")
                self.feather = None
        else:
            print("Feather nenajdeny, pouzivam klavesnicu")

        if KEYBOARD_ENABLED:
            self.keyboard = KEYBOARD_WASD if WASD else KEYBOARD_SIPKY
            pygame.init()

    def _read_loop(self):
        """Bezi v osobnom threade, cita JSON zo serioveho portu."""
        while True:
            try:
                line = self.feather.readline().decode().strip()
                if not line:
                    continue

                data = json.loads(line)

                with self._lock:
                    self._state = data

            except (json.JSONDecodeError, UnicodeDecodeError):
                pass  # poskodeny packet, preskocit
            except Exception as e:
                print(f"Serial chyba: {e}")
                break

    # --- Public API (rovnake ako predtym, hry sa nemusia menit) ---

    def is_pressed(self, button_name):
        if self.feather:
            with self._lock:
                return bool(self._state.get(button_name, False))

        if KEYBOARD_ENABLED:
            keys = pygame.key.get_pressed()
            button = self.keyboard.get(button_name)
            if isinstance(button, int):
                return bool(keys[button])

        return False

    def just_pressed(self, button_name):
        """True iba v prvom frame stlacenia."""
        current = self.is_pressed(button_name)
        last = self._last_state.get(button_name, False)
        self._last_state[button_name] = current
        return current and not last

    def _dead_zone(self, value):
        c = value - JOYSTICK_CENTER
        if abs(c) < JOYSTICK_DEADZONE:
            return 0.0
        if c > 0:
            maxr = JOYSTICK_MAX - JOYSTICK_CENTER - JOYSTICK_DEADZONE
            result = (c - JOYSTICK_DEADZONE) / maxr
        else:
            maxr = JOYSTICK_CENTER - JOYSTICK_MIN - JOYSTICK_DEADZONE
            result = (c + JOYSTICK_DEADZONE) / maxr
        return max(-1.0, min(1.0, result * JOYSTICK_SENSITIVITY))

    def get_axis(self, joystick, axis):
        key = f"JOYSTICK{joystick}_{axis}"

        if self.feather:
            with self._lock:
                raw = self._state.get(key, JOYSTICK_CENTER)
            return self._dead_zone(int(raw))

        if KEYBOARD_ENABLED:
            keys = pygame.key.get_pressed()
            kb_key = f"JOYSTICK{joystick}_{axis}"
            mapping = self.keyboard.get(kb_key, {})
            if keys[mapping.get("+", 0)]:
                return 1.0
            if keys[mapping.get("-", 0)]:
                return -1.0

        return 0.0

    def left_joystick(self):
        return (self.get_axis("L", "X"), self.get_axis("L", "Y"))

    def right_joystick(self):
        return (self.get_axis("R", "X"), self.get_axis("R", "Y"))

    def krizik_direction(self):
        dx = int(self.is_pressed("RIGHT")) - int(self.is_pressed("LEFT"))
        dy = int(self.is_pressed("DOWN")) - int(self.is_pressed("UP"))
        return (dx, dy)

    def cleanup(self):
        if self.feather and self.feather.is_open:
            self.feather.close()
            
if __name__ == "__main__":            
    
    i = InputHandler()
    
    if KEYBOARD_ENABLED:
        screen = pygame.display.set_mode((100, 100))
        pygame.display.set_caption("Input Test")
        
    print("--- Test Start ---")
    
    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                i.cleanup()
                pygame.quit()
                exit()
        
        a = i.is_pressed("A")
        b = i.just_pressed("B")
        
        if a or b:
            print(f"is_pressed('A'): {a}, just_pressed('B'): {b}")
        
        time.sleep(1 / 60)
        
        
        if a or b:
            pass

        i.cleanup()
        pygame.quit()