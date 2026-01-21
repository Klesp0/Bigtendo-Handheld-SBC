# 🎮 Bigtendo: A Raspberry Pi 5 Handheld Console

A high-performance DIY handheld console powered by the Raspberry Pi 5. This project combines custom 3D design, hardware integration, and original software to create a fully functional portable gaming system.



## 🛠 Hardware Architecture

The Bigtendo is built around a powerful SBC core with custom-programmed input logic for ultra-low latency.

* **Compute:** Raspberry Pi 5
* **Power Management:** Subtronics X1201 UPS Shield (Li-ion battery support)
* **Controller Interface:** Adafruit Feather RP2040 (USB-HID bridge)
* **Inputs:** 2x Analog Joysticks, 20x Physical Tactile Buttons
* **Audio:** I2S DAC + Audio Amplifier + 2x 2W Internal Speakers
* **Enclosure:** Custom 3D printed multi-part shell 
> [!TIP]
> **Project Roadmap:** I am currently designing a custom PCB to replace the breadboard/perfboard wiring. This will integrate the audio DAC, amplifier, and controller logic into a single board—significantly reducing the build cost, size, and assembly complexity while making the internal cable management much cleaner.

## 📂 Repository Structure

### [Design](./Design)
* **3D Models**
    * Finished Console Shell: Design/3D_Models/Bigtendo_Final_Case.stl
    * Assembly Source: Design/3D_Models/Bigtendo_Main_Project.f3d (Fusion 360)
    * Component Reference: Design/3D_Models/Hardware_References/ (Joystick, Raspberry 5, and internal mounts)
* **Assets**
    * Game icons: `Design/Assets/images/icons/`
    * Backgrounds: `Design/Assets/images/backgrounds/`
    * Sprites: `Design/Assets/images/sprites/`
    * Sounds: `Design/Assets/sounds/`

### [Firmware](./Firmware)
* **RP2040 Logic:** Python-based HID firmware for the controller interface.

### [Games](./Games)
* **Games:** Original titles developed in Pygame and Godot.

### Documentation & Media
* **[Docs](./Docs):** Full schematics, pin mapping and guide.
* **[Media](./Media):** Build photos and system screenshots.

## 🚀 Software & Games
The system runs on **RetroPie** with custom optimizations for the Pi 5. We've also included several original games:

* **Pygame Titles:** Custom retro-style games found in `/Games`. Launch via: `python3 games/title_name.py`.
* **Godot Projects:** Linux/ARM exports for the Bigtendo hardware.

> **Note:** We are currently working on a custom menu integration to launch these games directly from EmulationStation without needing the terminal.

## 🔧 How to Build
Detailed assembly instructions, 3D printing settings, and the Hardware can be found in our dedicated guide:

👉 **[Read the Step-by-Step Build Guide here!](./Docs)**

## 📜 License
This project is licensed under the **GNU General Public License v3.0**. See the [LICENSE](LICENSE) file for details.

---
### 🤝 Project Partners
* [@Klesp0](https://github.com/Klesp0) – **Lead Hardware Engineer & CAD Designer:**  Responsible for the hardware system architecture, component integration, power management, and final assembly. Co-designed the 3D console enclosure.
* [@lukas513](https://github.com/lukas513) – **Software Engineer & CAD Designer:**  Developed original games in Pygame and Godot and co-designed the 3D console enclosure and mechanical fitment.
* [@kosec1452](https://github.com/A-Kosec) – **Software & Graphics:**  Handled Pygame development, game design logic, and created the visual assets for the project.
