\# 🛠 Bigtendo Assembly Guide



This document provides the step-by-step instructions for assembling the Bigtendo handheld SBC console.



> \[!IMPORTANT]

> \*\*Safety First:\*\* Always disconnect the Li-ion batteries from the Subtronics X1201 UPS Shield before soldering or moving internal components to prevent short circuits.



---



\## 🔌 Hardware Setup



\### 1. Power \& Computing

\* \*\*UPS Mounting:\*\* Secure the \*\*Subtronics X1201 UPS Shield\*\* onto the Raspberry Pi 5.

\* \*\*Power Source:\*\* Connect your Li-ion batteries to the UPS shield. Double-check the polarity to avoid damaging the Pi.

\* \*\*Cooling:\*\* Ensure the Pi 5's active cooler or heatsink has enough clearance under the UPS shield.



\### 2. Display Assembly

\* \*\*Screen:\*\* Mount the \*\*7-inch display\*\* into the front frame of your 3D-printed shell.

\* \*\*Connection:\*\* Use the DSI ribbon cable to connect the display directly to the Pi 5's dedicated display port.



---



\## 🕹 Input \& Control Logic



\### 3. RP2040 Controller Interface

\* \*\*Wiring:\*\* Connect the \*\*20 tactile buttons\*\* and \*\*2 joysticks\*\* to the Adafruit Feather RP2040.

\* \*\*Communication:\*\* Plug the RP2040 into one of the Pi 5's USB ports. This allows the RP2040 to act as a "Plug-and-Play" controller (USB-HID).



> \[!TIP]

> \*\*Custom PCB Roadmap:\*\* We are currently designing a custom PCB to replace the breadboard wiring. This will integrate the audio DAC and controller logic, making this assembly step much simpler and more compact.



---



\## 🔊 Audio Output



\### 4. Sound System

\* \*\*DAC \& Amp:\*\* Wire the I2S DAC to the Raspberry Pi 5's GPIO pins.

\* \*\*Speakers:\*\* Connect the two 2W internal speakers to the amplifier output.

\* \*\*Placement:\*\* Secure the speakers into the designated cutouts in the 3D-printed shell.

