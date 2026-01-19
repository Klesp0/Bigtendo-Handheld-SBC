# kopirovanie game priecinku a shared
# cp kopirovanie suborov alebo priecinkov
# -r zabezpecuje ze sa skopiruje cely priecinok
# /home/pi/RetroPie/roms/ports/SW/ cielova cesta
# ../games zdrojova cesta, predpoklada ze priecinok games je o úroveň vyššie ako priecinok, v ktorom sa spúšťate tento skript
sudo cp -r ../games /home/pi/RetroPie/roms/ports/SW/
sudo cp -r ../shared /home/pi/RetroPie/roms/ports/SW/

# kopirovanie launcher scriptov
# *.sh je zdrojova cesta, znamena ze skopiruje vsetky .sh subory v aktualnom priecinku
# /home/pi/RetroPie/roms/ports/ cielova cesta, .sh sa sem skopiruju
sudo cp *.sh /home/pi/RetroPie/roms/ports/

# chmod prikaz na zmenu prav suboru
# +x pidat spustitelne pravo
# uplatni pravo na vsetky skopirovane .sh subory
sudo chmod +x /home/pi/RetroPie/roms/ports/*.sh

# if [ -d "../../Design/assets/images/icons/" ]; then, kontrola ci existuje adresar, -d testuje, či je cesta adresár
# sudo mkdir -p Vytvorí cieľový adresár pre ikony. -p zabezpečí, že sa vytvoria aj všetky nadradené adresáre, ak neexistujú
# sudo cp skopiruje vsetky png subory zo zdrojoveho do cieloveho adresara
# /home/pi/.emulationstation/downloaded_media/ports/, cielovy adresar
if [ -d "../../Design/assets/images/icons/" ]; then
    sudo mkdir -p /home/pi/.emulationstation/downloaded_media/ports/
    sudo cp ../../Design/assets/images/icons/*.png /home/pi/.emulationstation/downloaded_media/ports/
# ukoncenie if
fi