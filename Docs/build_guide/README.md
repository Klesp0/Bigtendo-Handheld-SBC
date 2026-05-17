# Build Guide

Step-by-step instructions for building the Bigtendo console. Read the [Wiring Guide](Docs\wiring_guide\README.md) alongside this for detailed connection tables.

---

## Step 1 — Gather Parts

Everything you need is in [BOM.csv](BOM.csv) with purchase links. Before ordering, check component dimensions against the [CAD models](Design\3D_Models\component_models) - the enclosure was designed around specific display size.

---

## Step 2 — Print the Enclosure (Settings)

Download the [STL files](\Design\3D_Models\.stl).

>[!NOTE]
>If you have got a bambulab printer just import the [.3mf models](Design\3D_Models\.3mf_for_printing) into BambuStudio.

### Case settings
- **Print both case halves with the flat exterior face down.**

>[!NOTE]
>Upper part doesn't  need supports!

| Setting | Value |
|---|---|
| Material | PLA |
| Layer height | 0.08mm Extra Fine |
| Infill | 20% Gyroid |
| Walls loops | 4  |
| Supports (lower) | tree(auto) Threshold angle |
| Supports (lower) | Top Z distance 0.28mm |
| Bed | Textured PEI |
| Skirt loop (others)|  1 | 
| Print time (lower) | 9h42m |
| Print time (upper) | 4h31m  |
| Filament | 250g total |

### Button settings
- **Button caps print flat side down, no supports.**

| Setting | Value |
|---|---|
| Material | PLA |
| Layer height | 0.08mm Extra Fine |
| Infill | 40% Gyroid |
| Walls loops | 4  |
| Bed | Textured PEI |
| Skirt loop (others)|  1 | 
| Print time | 1h31m |
| Filament | 15g total |

| | |
|:---:|:---:|
| ![case](/Media/photos/wiring/print_case.jpg) | ![buttons](/Media/photos/wiring/print_buttons.jpg) |

---

## Step 3 — Flash the Feather RP2040

1. Download the CircuitPython `.uf2` for the Feather RP2040 from [circuitpython.org](https://circuitpython.org/board/adafruit_feather_rp2040/)
2. Plug the feather into your PC

![button](/Media/photos/wiring/highlighted.jpg)

3. To enter the bootloader, hold down BOOTSEL (highlighted in `red` above), and while continuing to hold it (**`don't let go!`**), press and release the reset button (highlighted in `blue` above). Continue to hold the BOOT/BOOTSEL button until the `RPI-RP2` drive appears!
4. Drag the `.uf2` onto it — the Feather reboots and `CIRCUITPY` appears
5. Copy the firmware files onto `CIRCUITPY`:

```
CIRCUITPY/
├── boot.py
├── code.py
└── lib/
    └── adafruit_hid/
        └── gamepad.py
```

The D13 LED should stay **`blinking`** after reboot. **blinking** = running. **Solid** = error.

---

## Step 4 — Install RetroPie

1. Download the [Raspberry Pi Imager](https://circuitpython.org/board/adafruit_feather_rp2040/) and flash Raspberry Pi OS (64-bit) onto your microSD card.
2. put the cooler onto the raspberry 5 and screw the Raspberry onto the UPS shield
3. 
![ups](/Media/photos/wiring/x1201v1.1_hardware2.jpg)

>[!NOTE]
>Don't inset the batteries just yet

4. Insert the card, connect your monitor, and plug the USB-C power cable into the UPS shield connector. 

> **`don't`** plug it into the Pi 5's own USB-C port

5. After you have everything ready boot into Raspbian and follow this [guide](https://www.youtube.com/watch?v=AaseHnf0k2o), to set up Raspbian and RetroPie on top of it

[![Watch the video](https://img.youtube.com/vi/AaseHnf0k2o/0.jpg)](https://www.youtube.com/watch?v=AaseHnf0k2o)

---

## Step 5 — Load the Games

Download the Roms(games) and continue watching the [guide](https://www.youtube.com/watch?v=AaseHnf0k2o) from 10:15 to add the Roms to the Retropie. 

---

# Step 6 — Set Up the Audio

See the [Wiring Guide](wiring_guide.md) for the full audio schematic and connection tables.

The Pi 5 has no headphone jack, so the PCM5122 DAC is required to convert the digital I2S signal to analog audio. Wire the DAC to the Pi over I2S and I2C (8 wires total), connect the DAC outputs to the PAM8403 inputs, and the amp outputs to the speakers. Make sure MOD2 is pulled to 3.3V.

### Configure the Pi

```
sudo nano /boot/firmware/config.txt
```

Find or add these lines:

```
dtparam=i2c_arm=on        <- Add this line
# dtparam=i2s=on          <- Comment this out or remove it entirely
dtparam=audio=off         <- Disable onboard audio
```

add the DAC overlay at the bottom of the file :

```
dtoverlay=iqaudio-dac
```

> [!IMPORTANT]
> Do **not** leave `dtparam=i2s=on` enabled. RetroPie adds this line, and it causes the kernel to claim GPIO18 (the I2S bit clock) before the `iqaudio-dac` overlay can use it. The DAC will appear in `aplay -l` and respond on I2C, but no audio will actually reach it. Commenting out `dtparam=i2s=on` and letting the overlay manage I2S on its own is the fix.

After rebooting, verify the DAC is detected:

```
aplay -l                         # Should show: card 2: IQaudIODAC
play something on youtube        # Should hear something from both speakers
```

### Make the Config Survive Reboots

RetroPie overwrites the ALSA config on every boot. To prevent this, write the ALSA configuration into the root-level system files where RetroPie can't touch it:

```
sudo nano /etc/alsa/config.txt/bigtendo.conf
```

```
defaults.pcm.card 2
defaults.ctl.card 2
```

This makes the DAC the default audio device system-wide and survives RetroPie reboots.

### If It Doesn't Work

- **No DAC in `aplay -l`:** Run `sudo i2cdetect -y 1` - look for address `4c`.
- **GPIO18 conflict:** Run `dmesg | grep -i i2s` - if you see a conflict, `dtparam=i2s=on` is still enabled. Comment it out.
- **Audio works in Raspbian but not in EmulationStation or games:** The ALSA root-level config above fixes this.

---

## Step 7 — Solder Buttons and Joysticks

See the [Wiring Guide](wiring_guide.md) for the full pin tables.

Each button connects between one Feather GPIO pin and GND, with the internal pull-up resistor enabled in firmware. Getting buttons to sit in exactly the right spots on the perfboard, so they line up with the holes in the 3D-printed enclosure, is the hardest part of the whole assembly.

The technique that worked for me:

1. Tape the button caps tightly in place on the upper shell
2. Put buttons into the caps

![tape](/Media/photos/wiring/tape.jpg)

3. Place the upper shell onto the lower half so the buttons touch the perfboard
4. Press the buttons down gently
5. Lift the shell carefully without shifting anything 
6. Mark where their pins land on the perfboard and solder the buttons at those positions
7. Test fit before moving on to the next set

Repeat this for each button. Shoulder buttons don't need precise positioning - they are hot-glued to their pillar anyway, so just solder them wherever they reach and glue them in place.

Each joystick has 5 wires: VCC (3.3V), GND, VRx, VRy, and SW (click). Screw the joysticks into their pillars before soldering the wires. The right joystick is mounted 90° clockwise in the enclosure - don't try to compensate it in wiring, the firmware handles it with `SWAP_JOY1_XY = True` and `INVERT_JOY1_X = True`.

| | |
|:--:|:--:|
| ![joystick wiring](/Media/photos/wiring/joystick_wiring.jpg) | ![joystick wiring](/Media/photos/wiring/joystick_wiring1.jpg)

To verify, plug it into any PC and open [hardwaretester.com](https://hardwaretester.com/gamepad) - all 17 buttons and both joystick axes should register.

---

## Step 8 — Final Assembly

### Bottom shell (install in this order)

1. 18650 cells into the battery holders

> [!WARNING]
> Double-check battery polarity before connecting. Reversed polarity can permanently damage the Pi and the UPS shield.

2. PCM5122 DAC and PAM8403 amp into their mounts
3. Speakers on top of the honeycomb grilles
4. screw perfboards and joysticks in position
5. Route all wires flat — pinched wires are the main reason the case won't close

### Top shell

1. Display in its cutout, DSI ribbon cable connected to the Pi
2. Button caps through the shell holes

> [!TIP]
> Tape the back of the UPS shield with electric tape, just to be sage.

![tape](/Media/photos/wiring/tape_ups.jpg)

### Close it up

Connect the HDMI ribbon, Feather USB cable, and all remaining wires. Align the two halves and press them together. Screw the 2 halves together. Power on and START PLAYING! 
