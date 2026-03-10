# SPDX-FileCopyrightText: 2018 Dan Halbert for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
`Gamepad`
====================================================
* Modified for 24 buttons and 4 axes (7-byte report)
* Report ID is handled automatically by CircuitPython
"""
import struct
import time
from adafruit_hid import find_device

class Gamepad:
    """Emulate a generic gamepad controller with 24 buttons (1-24)
    and two joysticks (x, y, z, r_z) in the range -127 to 127."""

    def __init__(self, devices):
        """Create a Gamepad object that will send USB gamepad HID reports."""
        self._gamepad_device = find_device(devices, usage_page=0x1, usage=0x05)

        # 7-byte report (Report ID is handled separately by CircuitPython)
        # report[0] = buttons 1-8
        # report[1] = buttons 9-16
        # report[2] = buttons 17-24
        # report[3] = joystick 0 x
        # report[4] = joystick 0 y
        # report[5] = joystick 1 x (z)
        # report[6] = joystick 1 y (r_z)
        self._report = bytearray(7)
        self._last_report = bytearray(7)

        self._buttons_state = 0
        self._joy_x = 0
        self._joy_y = 0
        self._joy_z = 0
        self._joy_r_z = 0

        try:
            self.reset_all()
        except OSError:
            time.sleep(1)
            self.reset_all()

    def press_buttons(self, *buttons):
        """Press and hold the given buttons."""
        for button in buttons:
            self._buttons_state |= 1 << (self._validate_button_number(button) - 1)
        self._send()

    def release_buttons(self, *buttons):
        """Release the given buttons."""
        for button in buttons:
            self._buttons_state &= ~(1 << (self._validate_button_number(button) - 1))
        self._send()

    def release_all_buttons(self):
        """Release all the buttons."""
        self._buttons_state = 0
        self._send()

    def click_buttons(self, *buttons):
        """Press and release the given buttons."""
        self.press_buttons(*buttons)
        self.release_buttons(*buttons)

    def move_joysticks(self, x=None, y=None, z=None, r_z=None):
        """Set and send the given joystick values (-127 to 127)."""
        if x is not None:
            self._joy_x = self._validate_joystick_value(x)
        if y is not None:
            self._joy_y = self._validate_joystick_value(y)
        if z is not None:
            self._joy_z = self._validate_joystick_value(z)
        if r_z is not None:
            self._joy_r_z = self._validate_joystick_value(r_z)
        self._send()

    def reset_all(self):
        """Release all buttons and set joysticks to zero."""
        self._buttons_state = 0
        self._joy_x = 0
        self._joy_y = 0
        self._joy_z = 0
        self._joy_r_z = 0
        self._send(always=True)

    def _send(self, always=False):
        """Send a report with all the existing settings."""
        # Pack data into 7-byte report (Report ID is added automatically)
        struct.pack_into(
            "<BBBbbbb",
            self._report,
            0,
            (self._buttons_state & 0xFF),          # Buttons 1-8
            (self._buttons_state >> 8) & 0xFF,     # Buttons 9-16
            (self._buttons_state >> 16) & 0xFF,    # Buttons 17-24
            self._joy_x,
            self._joy_y,
            self._joy_z,
            self._joy_r_z,
        )

        if always or self._last_report != self._report:
            self._gamepad_device.send_report(self._report)
            self._last_report[:] = self._report

    @staticmethod
    def _validate_button_number(button):
        if not 1 <= button <= 24:
            raise ValueError("Button number must be in range 1 to 24")
        return button

    @staticmethod
    def _validate_joystick_value(value):
        if not -127 <= value <= 127:
            raise ValueError("Joystick value must be in range -127 to 127")
        return value
