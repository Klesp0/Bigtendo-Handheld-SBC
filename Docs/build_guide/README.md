# 🛠 Bigtendo Assembly Guide
This guide covers the initial hardware setup, operating system installation, and firmware configuration for the Bigtendo handheld.

##🔌 Phase 1: Core Hardware Assembly
* **UPS Mounting:** Secure the Subtronics X1201 UPS Shield directly onto the Raspberry Pi 5 GPIO pins.

* **Cooling:** Install the official Raspberry Pi Active Cooler. Ensure the heatsink and fan have enough clearance under the UPS shield.

* **Power:** Connect your Li-ion batteries to the UPS shield.

>[!WARNING] 
>Double-check battery polarity before connecting. Reversed polarity can permanently damage the Pi and the shield.

* **Display:** Mount the 7-inch display into the front frame of your shell and connect the DSI ribbon cable to the Pi 5.

## 💾 Phase 2: OS & Emulation Setup
* **Imaging:** Download the Raspberry Pi Imager and flash Raspberry Pi OS (64-bit) onto your microSD card.

* **Initial Boot:** Insert the card, connect your monitor, and plug the USB-C power cable into the UPS shield connector (not the Pi 5's USB-C port).

* **Connectivity:** Boot the system and connect to Wi-Fi.

>[!TIP] 
>If you encounter errors while updating or downloading files from GitHub, connect via Ethernet for a more stable connection.

* **RetroPie Installation:** Open the terminal and follow the Subtronics installation scripts for the X1201.

* **Emulation Layer:** To run RetroPie on top of Raspberry Pi OS, follow this  guide starting at [03:40]:
[![Watch the video](https://img.youtube.com/vi/AaseHnf0k2o/0.jpg)](https://www.youtube.com/watch?v=AaseHnf0k2o)

## 🕹 Phase 3: Controller Firmware & Wiring
* **Prepare the Feather:** Plug your Adafruit Feather RP2040 into your PC.

* **CircuitPython:** Download the latest UF2 file and drop it onto the RPI-RP2 drive. The board will reboot as CIRCUITPY.

* **Upload Firmware:** Copy the whole firmware from the [Firmware folder](/Firmware) onto your Feather.

* **Soldering & Controls:** Unplug the Feather and begin soldering the cables for the 20 tactile buttons and 2 joysticks.

Refer to the Wiring Guide for the specific pinout.

[diagram](/Docs/wiring_guide)