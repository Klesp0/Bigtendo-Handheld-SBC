import pygame
from config import *


class InputHandler:
    def __init__(self):
        self._last_state = {}

        pygame.init()
        pygame.joystick.init()

        self.joystick = None

        for i in range(pygame.joystick.get_count()):
            j = pygame.joystick.Joystick(i)
            j.init()
            print(f"Najdeny gamepad [{i}]: {j.get_name()}")
            if self.joystick is None:
                self.joystick = j

        if self.joystick:
            print(f"Pouzivam: {self.joystick.get_name()}")
            print(f"  Buttony: {self.joystick.get_numbuttons()}")
            print(f"  Osi:     {self.joystick.get_numaxes()}")
        else:
            print("Gamepad nenajdeny! Pouzivam klavesnicu.")

        if KEYBOARD_ENABLED:
            self.keyboard = KEYBOARD_WASD if WASD else KEYBOARD_SIPKY

    def _pump(self):
        pygame.event.pump()

    def is_pressed(self, button_name):
        self._pump()
        result = False

        if self.joystick:
            idx = GAMEPAD_BUTTON_MAP.get(button_name)
            if idx is not None and idx < self.joystick.get_numbuttons():
                return bool(self.joystick.get_button(idx))

        if KEYBOARD_ENABLED and not result:
            keys = pygame.key.get_pressed()
            mapping = self.keyboard.get(button_name)
            if isinstance(mapping, int):
                return bool(keys[mapping])

        return result

    def just_pressed(self, button_name):
        current = self.is_pressed(button_name)
        last = self._last_state.get(button_name, False)
        self._last_state[button_name] = current
        return current and not last

    def get_axis(self, joystick, axis):
        self._pump()
        result = 0.0

        key = f"{joystick}_{axis}"

        if self.joystick:
            idx = GAMEPAD_AXIS_MAP.get(key)
            if idx is not None and idx < self.joystick.get_numaxes():
                return self.joystick.get_axis(idx)  

        if KEYBOARD_ENABLED and result == 0.0:
            keys = pygame.key.get_pressed()
            kb_key = f"JOYSTICK{joystick}_{axis}"
            mapping = self.keyboard.get(kb_key, {})
            if isinstance(mapping, dict):
                if keys[mapping.get("+", 0)]:
                    return 1.0
                if keys[mapping.get("-", 0)]:
                    return -1.0

        return result

    def left_joystick(self):
        return (self.get_axis("LEFT", "X"), self.get_axis("LEFT", "Y"))

    def right_joystick(self):
        return (self.get_axis("RIGHT", "X"), self.get_axis("RIGHT", "Y"))

    def krizik_direction(self):
        dx = int(self.is_pressed("RIGHT")) - int(self.is_pressed("LEFT"))
        dy = int(self.is_pressed("DOWN")) - int(self.is_pressed("UP"))
        return (dx, dy)

    def cleanup(self):
        if self.joystick:
            self.joystick.quit()
        pygame.joystick.quit()