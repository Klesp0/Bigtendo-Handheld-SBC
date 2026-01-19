# RetroPie Integration

## Setup Instructions

### 1. Transfer Games to RPi
```bash
# On PC:
cd ~/hellathon-console
tar -czf games.tar.gz SW/games/ SW/shared/

# Transfer:
scp games.tar.gz pi@retropie:~

# On RPi:
ssh pi@retropie
tar -xzf games.tar.gz
sudo mv games /home/pi/RetroPie/roms/ports/
sudo mv shared /home/pi/RetroPie/roms/ports/
```

### 2. Install Launcher Scripts
```bash
# Transfer .sh scripts:
scp *.sh pi@retropie:/home/pi/RetroPie/roms/ports/

# Set permissions:
ssh pi@retropie "chmod +x /home/pi/RetroPie/roms/ports/*.sh"
```

### 3. Add Game Icons
```bash
# Transfer icons:
scp icons/*.png pi@retropie:/home/pi/.emulationstation/downloaded_media/ports/

# Icon naming: Must match .sh filename
# Snake.sh → Snake.png
```

### 4. Restart EmulationStation
```bash
ssh pi@retropie "killall emulationstation"
# ES will auto-restart
```

## Launcher Script Format
```bash
#!/bin/bash
# GameName.sh

cd /home/pi/RetroPie/roms/ports/games/gamename/
python3 gamename.py

# Return to ES
exit 0
```

## Troubleshooting

**Game doesn't appear in Ports:**
- Check .sh file has execute permission: `chmod +x`
- Verify file location: `/home/pi/RetroPie/roms/ports/GameName.sh`
- Restart EmulationStation

**Game crashes:**
- Test standalone first: `python3 gamename.py`
- Check dependencies: `pip3 install pygame`
- View logs: Check terminal output

**Icon doesn't show:**
- Verify path: `/home/pi/.emulationstation/downloaded_media/ports/GameName.png`
- Name must match exactly (case-sensitive)
- Restart ES after adding icons