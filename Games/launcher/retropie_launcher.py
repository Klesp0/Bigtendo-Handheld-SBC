# """
# RetroPie Launcher - Single Controller
# Launches games from EmulationStation
# Returns to EmulationStation on exit
# """
# retropie menu budeme robit ako prve
# import sys
# import os

# # Add paths
# sys.path.insert(0, '/home/pi/RetroPie/roms/ports/')
# sys.path.insert(0, '/home/pi/RetroPie/roms/ports/SW/')

# def launch_game(game_name):
#     """Launch game by name"""
    
#     # Import game class
#     if game_name == "snake":
#         from games.Pygame.snake.snake import SnakeGame
#         game_class = SnakeGame
    
#     elif game_name == "tetris":
#         from games.Pygame.tetris.tetris import TetrisGame
#         game_class = TetrisGame
    
#     elif game_name == "pong":
#         from games.Pygame.pong.pong import PongGame
#         game_class = PongGame
    
#     elif game_name == "breakout":
#         from games.Pygame.breakout.breakout import BreakoutGame
#         game_class = BreakoutGame
    
#     elif game_name == "space_invaders":
#         from games.Pygame.space_invaders.invaders import SpaceInvadersGame
#         game_class = SpaceInvadersGame
    
#     elif game_name == "memory":
#         from games.Pygame.memory.memory import MemoryGame
#         game_class = MemoryGame
    
#     # Add Godot games when ready
#     # elif game_name == "flappy":
#     #     import subprocess
#     #     subprocess.call("/home/pi/RetroPie/roms/ports/games/Godot/flappy/flappy.x86_64")
#     #     return
    
#     else:
#         print(f"Unknown game: {game_name}")
#         print("Available games: snake, tetris, pong, breakout, space_invaders, memory")
#         sys.exit(1)
    
#     # Launch game
#     try:
#         game = game_class(fullscreen=True)
#         game.run()
    
#     except Exception as e:
#         print(f"Error launching {game_name}: {e}")
#         import traceback
#         traceback.print_exc()
#         sys.exit(1)

# def show_usage():
#     """Show usage info"""
#     print("RetroPie Game Launcher")
#     print("Usage: retropie_launcher.py <game_name>")
#     print("")
#     print("Available games:")
#     print("  snake")
#     print("  tetris")
#     print("  pong")
#     print("  breakout")
#     print("  space_invaders")
#     print("  memory")

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         show_usage()
#         sys.exit(1)
    
#     game_name = sys.argv[1].lower()
#     launch_game(game_name)
    
# vysvetlenie od gemini
# Ahoj, tento kód je v podstate spúšťač hier (Game Launcher), ktorý je navrhnutý pre prostredie RetroPie a jej grafické rozhranie EmulationStation.

# Hlavným účelom skriptu je prijať názov hry ako argument z príkazového riadku a následne túto hru spustiť. Po skončení hry sa očakáva, že sa vráti späť do EmulationStation.

# Tu je podrobné vysvetlenie, čo robia jednotlivé časti:

# 1. 📂 Importy a Nastavenie Ciest (import sys, import os, sys.path.insert)
# Importy: Importujú sa základné moduly sys (pre prácu so systémovými parametrami, ako sú argumenty príkazového riadku a ukončenie skriptu) a os (pre prácu s operačným systémom, aj keď sa tu priamo nepoužíva, je dobrý zvyk).

# Pridanie ciest:

# Python

# sys.path.insert(0, '/home/pi/RetroPie/roms/ports/')
# sys.path.insert(0, '/home/pi/RetroPie/roms/ports/SW/')
# Tieto riadky pridávajú špecifické adresáre do systémovej cesty, ktorú Python prehľadáva pri hľadaní modulov. To je nevyhnutné na to, aby mohol skript úspešne importovať triedy hier z adresárov, ako sú games.Pygame.snake.snake.

# 2. 🚀 Funkcia launch_game(game_name)
# Toto je jadro programu, ktoré sa stará o spustenie konkrétnej hry.

# Identifikácia hry a import:

# Python

# if game_name == "snake":
#     from games.Pygame.snake.snake import SnakeGame
#     game_class = SnakeGame
# # ... ďalšie elif bloky pre tetris, pong, breakout, space_invaders, memory
# Na základe vstupného argumentu (game_name) kód dynamicky importuje príslušnú triedu hry (napr. SnakeGame, TetrisGame) z jej umiestnenia v súborovom systéme a priradí ju premennej game_class.

# Neexistujúca hra:

# Python

# else:
#     print(f"Unknown game: {game_name}")
#     # ... a ukončí skript
#     sys.exit(1)
# Ak je zadaný názov hry, ktorý nie je na zozname, kód vypíše chybu a ukončí sa.

# Spustenie hry:

# Python

# try:
#     game = game_class(fullscreen=True)
#     game.run()
# except Exception as e:
#     # ... vypíše chybu a ukončí sa
#     sys.exit(1)
# Vytvorí inštanciu triedy hry (game_class) a zvyčajne jej odovzdá parameter fullscreen=True.

# Zavolá metódu game.run(), ktorá spúšťa hlavnú hernú slučku.

# Blok try...except zabezpečuje, že ak počas spúšťania alebo behu hry nastane chyba, program ju zachytí, vypíše informácie o chybe (traceback) a elegantne sa ukončí.

# 3. ℹ️ Funkcia show_usage()
# Táto funkcia slúži len na zobrazenie informácií o tom, ako skript používať (správny formát spustenia) a aké hry sú k dispozícii.

# 4. 🏁 Hlavný Blok Spustenia (if __name__ == "__main__":)
# Toto je štandardný spôsob, ako sa spúšťa kód v Pythone, keď sa súbor spustí priamo.

# Kontrola argumentov:

# Python

# if len(sys.argv) < 2:
#     show_usage()
#     sys.exit(1)
# Skontroluje, či bol zadaný aspoň jeden argument (názov hry). Ak nie, zavolá show_usage() a ukončí sa.

# Spustenie:

# Python

# game_name = sys.argv[1].lower()
# launch_game(game_name)
# Vezme prvý argument príkazového riadku (sys.argv[1]), prevedie ho na malé písmená a priradí ho premennej game_name.

# Zavolá funkciu launch_game(), čím sa spustí celá logika spúšťania hry.

# Zhrnutie a Kontext RetroPie
# RetroPie: Je to softvérová knižnica na Raspberry Pi, ktorá umožňuje premeniť ho na retro hernú konzolu.

# EmulationStation: Je to grafické rozhranie (menu), ktoré RetroPie používa na prechádzanie zoznamom hier.

# Tento Skript: V EmulationStation je tento skript pravdepodobne nakonfigurovaný ako "emulátor" pre sekciu "Ports" (Porty). Keď používateľ v EmulationStation vyberie napríklad Snake, EmulationStation v skutočnosti zavolá tento skript s argumentom retropie_launcher.py snake, čo potom spustí hru Snake.

# "Single Controller": Z komentára vyplýva, že kód je navrhnutý tak, aby pracoval s ovládaním pre jedného hráča.

# Chceli by ste vedieť, ako sa podobný skript používa v kontexte EmulationStation, alebo by ste sa chceli pozrieť na ukážku kódu jednej z hier (napr. Snake)?