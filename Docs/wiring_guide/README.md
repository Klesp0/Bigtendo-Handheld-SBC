# Wiring Guide

Every wire connection in the Bigtendo console.

## Feather RP2040

Solder all the jumper wires exactly like in the table below - the result should look like the image.

![Feather wiring](/Media/photos/wiring/feather_wiring.jpg)

| Feather Pins | Wire Color |
|---|---|
| `board.D12` \| `board.D13` \| `board.MOSI` | Purple |
| `board.D11` \| `board.D10` \| `board.D9` \| `board.D6` | White |
| `board.D5` \| `board.D24` | Green |
| `board.SDA` \| `board.SCL` | Brown |
| 3.3V | Red |
| GND | Black |
| `board.A0` \| `board.A1` \| `board.A2` \| `board.A3` | Yellow |
| `board.D25` \| `board.SCK` | Blue |
| `board.MISO` \| `board.RX` \| `board.TX` \| `board.D4` | Orange |

## Buttons

All buttons use the Feather's internal pull-up resistors. One leg connects to the Feather GPIO pin, the other to GND.

### Button Pin Assignments

| Physical Button | CircuitPython Pin | Wire Color |
|---|---|---|
| Left Joystick Click | `board.D5` | Green |
| A | `board.D6` | White |
| B | `board.D9` | White |
| X | `board.D10` | White |
| Y | `board.D11` | White |
| Start | `board.D12` | Purple |
| Select | `board.D13` | Purple |
| Right Joystick Click | `board.D24` | Green |
| Left Trigger (lower) | `board.D25` | Blue |
| Left Trigger (upper) | `board.SCK` | Blue |
| Home | `board.MOSI` | Purple |
| Arrow Down | `board.MISO` | Orange |
| Arrow Up | `board.RX` | Orange |
| Arrow Right | `board.TX` | Orange |
| Right Trigger (upper) | `board.SDA` | Brown |
| Right Trigger (lower) | `board.SCL` | Brown |
| Arrow Left | `board.D4` | Orange |

## Joysticks

Each joystick has 5 pins: VCC (3.3V), GND, VRx (analog X), VRy (analog Y), and SW (click button).

### Right Joystick

| Joystick Pin | Feather Pin | Wire Color |
|---|---|---|
| VRy | `board.A0` | Yellow |
| VRx | `board.A1` | Yellow |
| SW (button) | `board.D5` | Green |
| VCC | 3.3V | Red |
| GND | GND | Black |

### Left Joystick

| Joystick Pin | Feather Pin | Wire Color |
|---|---|---|
| VRy | `board.A2` | Yellow |
| VRx | `board.A3` | Yellow |
| SW (button) | `board.D24` | Green |
| VCC | 3.3V | Red |
| GND | GND | Black |

## Audio Schematic

**Signal path:** Pi 5 → PCM5122 I2S DAC → PAM8403 Stereo Class D Amplifier → Speakers

![Audio Schematic](/Media/images/audio_wiring.png)

### Pi 5 → PCM5122 DAC

| Pi 5 Pin | PCM5122 Pin | Wire Color | Purpose |
|---|---|---|---|
| 3V (Pin 17) | VIN | Pink/Red | DAC power |
| GND | GND | Grey | Ground  |
| GPIO18 (Pin 12) | BCK | Green | I2S bit clock |
| GPIO19 (Pin 35) | WSEL | Grey/White | I2S word select |
| GPIO21 (Pin 40) | DIN | Orange | I2S audio data |
| GPIO3 / SCL (Pin 5) | SCL | Yellow | I2C clock |
| GPIO2 / SDA (Pin 3) | SDA | Blue | I2C data |
| 3V (Pin 1) | MOD2 | Pink | Enables I2C control mode |

### PCM5122 DAC → PAM8403 Amplifier

| PCM5122 Output | PAM8403 Input |
|---|---|
| LOUT | L (left channel audio in) |
| GND | GND |
| ROUT | R (right channel audio in) |

### PAM8403 Amplifier — Power

| Source | PAM8403 Pin |
|---|---|
| Pi 5V | VCC 5V |
| Pi GND | GND |

### PAM8403 Amplifier → Speakers

| PAM8403 Output | Speaker |
|---|---|
| L+ / L- | Left 2030 cavity speaker (8Ω, 2W) |
| R+ / R- | Right 2030 cavity speaker (8Ω, 2W) |
