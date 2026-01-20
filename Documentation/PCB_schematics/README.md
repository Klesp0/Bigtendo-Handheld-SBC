🛠 Bigtendo Assembly Guide

This document provides the step-by-step instructions for assembling the Bigtendo handheld SBC console.



🔌 Hardware Setup

1\. Power \& Computing

UPS Mounting: Secure the Subtronics X1201 UPS Shield onto the Raspberry Pi 5.



Power Source: Connect your Li-ion batteries to the UPS shield, ensuring the polarity is correct to avoid damaging the Pi.



Cooling: Ensure the Pi 5's active cooler or heatsink has enough clearance under the UPS shield.



2\. Display Assembly

Screen: Mount the 7-inch display into the front frame of your 3D-printed shell.



Connection: Use the DSI ribbon cable to connect the display directly to the Pi 5's dedicated display port.



🕹 Input \& Control Logic

3\. RP2040 Controller Interface

Wiring: Connect the 20 tactile buttons and 2 joysticks to the Adafruit Feather RP2040.



Communication: Plug the RP2040 into one of the Pi 5's USB ports using a short USB cable. This allows the RP2040 to act as a "Plug-and-Play" controller (USB-HID).



🔊 Audio Output

4\. Sound System

DAC \& Amp: Wire the I2S DAC to the Raspberry Pi 5's GPIO pins.



Speakers: Connect the two 2W internal speakers to the amplifier output.



Placement: Secure the speakers into the designated cutouts in the Design/3D\_Models files.



📝 Assembly Checklist

\[ ] Verify all 20 buttons click freely without sticking in the shell.



\[ ] Check that the UPS shield is charging the batteries when plugged in.



\[ ] Ensure the 7" display is recognized by the OS.

