# neni este dorobene, nechytat sa
# dorobit just_press a is_pressed, nefunguju
# opytat sa clauda na adafruit
# opytat sa clauda preco moj test nefunguje a od gemini funguje, ci to iba mosim pouzit v hre alebo nieco ine

try:
    from gpiozero import Button, MCP3001
    GPIO = True

except ImportError as e:
    GPIO = False
    print(f"Keyboard: {e}")
    
import pygame
from config import *
import time
# ked sa neprida debouncing tak odstranit


class InputHandler:
    def __init__(self, debouncing_time = 0.05):
        # je to v sekundach, je to na eliminaciu falosnych signalov
        
        self.GPIO = GPIO
        self.debouncing_time = debouncing_time
        self.buttons = {}
        self.joysticks = {}
        self.last_press = {}
        self.last_state = {}
        
        # tlacidla a joystick, nastavenie
        try:
            if self.GPIO and GPIO_ENABLED:
                self.GPIO1 = True
                for button, pin in GPIO_PINS.items():
                    if button != "ON_OFF":
                        
                        self.buttons[button] = Button(pin, pull_up=True ,bounce_time= 0.5)
                        self.last_press[button] = 0

                    else:
                        pass
                    
                self.joysticks["LEFT_X"] = MCP3001(channel = GPIO_PINS["JOYSTICKL_X"])
                self.joysticks["LEFT_Y"] = MCP3001(channel = GPIO_PINS["JOYSTICKL_Y"])
                self.joysticks["RIGHT_X"] = MCP3001(channel = GPIO_PINS["JOYSTICKR_X"])
                self.joysticks["RIGHT_Y"] = MCP3001(channel = GPIO_PINS["JOYSTICKR_Y"])
                
        except Exception as e:
            print(f"Keyboard: {e}")
            self.GPIO1 = False
        
        if KEYBOARD_ENABLED:
            if WASD:
                self.keyboard = KEYBOARD_WASD
            
            else:
                self.keyboard = KEYBOARD_SIPKY
                
            pygame.init()
        
    def is_pressed(self, button_name):
        # skontroluje GPIO alebo klavesnicu
        # skontroluje ci sa tlacidlo stlaci a drzi, bez debouncingu

        if self.GPIO and GPIO_ENABLED and self.GPIO1:
            return self.buttons[button_name].is_pressed
        
        if KEYBOARD_ENABLED:
            b = pygame.key.get_pressed()
            
            # fallback na klavesnicu     
            if button_name in self.keyboard:   
                button = self.keyboard[button_name]
                
                # vypere bool hodnotu pre danu klavesu            
                return b[button]
            
        else:
            button = None 
            return False
    
    def just_pressed(self, button_name):
        # skontroluje iba stlacenie tlacitla
        # debouncing, pridat podla potreby, pouzit time
        
        current = self.is_pressed(button_name)
        last = self.last_state.get(button_name, False)
        
        self.last_state[button_name] = current
        
        return current and not last
    
    # aplikuje deadzone a centrovanie joysticku
    def dead_zone(self, value):
        
        c = value - JOYSTICK_CENTER
        
        if abs(c) < JOYSTICK_DEADZONE:
            return 0.0
        
        if c > 0:
            maxr = JOYSTICK_MAX -JOYSTICK_CENTER - JOYSTICK_DEADZONE
            result = (c - JOYSTICK_DEADZONE) / maxr
        
        else:
            maxr = JOYSTICK_CENTER - JOYSTICK_MIN - JOYSTICK_DEADZONE
            result = (c + JOYSTICK_DEADZONE) / maxr
        
        # pohybovanie hodnoty od -1 po 1
        result = max(-1.0, min(1.0, result))
        result = result * JOYSTICK_SENSITIVITY
        
        # upravit, opytat clauda
        return max(-1.0, min(1.0, result))
    
    # vrati iba x alebo y
    def get_axis(self, joystick, a):
        # joysticky
        joystick_a = f"{joystick}_{a}"
        
        if self.GPIO and GPIO_ENABLED and joystick_a in self.joysticks:
            try:
                value = self.joysticks[joystick_a].value
                value = int(value * JOYSTICK_MAX)
                
                return self.dead_zone(value)
                    
            except Exception as e:
                print(f"{e}")
                return 0.0  
        
        if KEYBOARD_ENABLED:
            # speci tuple
            keys = pygame.key.get_pressed()
            
            if joystick_a == "RIGHT_X":
                if keys[self.keyboard["JOYSTICKR_X"]["+"]]:
                    return 1.0
                
                elif keys[self.keyboard["JOYSTICKR_X"]["-"]]:
                    return -1.0
            
            elif joystick_a == "RIGHT_Y":
                if keys[self.keyboard["JOYSTICKR_Y"]["+"]]:
                    return 1.0
                
                elif keys[self.keyboard["JOYSTICKR_Y"]["-"]]:
                    return -1.0
            
            elif joystick_a == "LEFT_X":
                if keys[self.keyboard["JOYSTICKL_X"]["+"]]:
                    return 1.0
                
                elif keys[self.keyboard["JOYSTICKL_X"]["-"]]:
                    return -1.0
            
            elif joystick_a == "LEFT_Y":
                if keys[self.keyboard["JOYSTICKL_Y"]["+"]]:
                    return 1.0
                
                elif keys[self.keyboard["JOYSTICKL_Y"]["-"]]:
                    return -1.0
        
        return 0.0
        
    # vrati tuple(x, y), daneho joysticku   
    def left_joystick(self):
        x = self.get_axis("LEFT", "X")
        y = self.get_axis("LEFT", "Y")
        
        return (x, y)
    
    def right_joystick(self):
        x = self.get_axis("RIGHT", "X")
        y = self.get_axis("RIGHT", "Y")
        
        return (x, y)
            
    # vrati tuple(x, y) podla stlacenej sipky
    def krizik_direction(self):
        dx, dy = 0,0
        
        if self.is_pressed("UP"):
            dy = -1  
            
        elif self.is_pressed("DOWN"):
            dy = 1
            
        if self.is_pressed("RIGHT"):
            dx = 1
            
        elif self.is_pressed("LEFT"):
            dx = -1
        
        return (dx, dy)
            
    def cleanup(self):
        # ked je koniec vymaze objekty button
        
        if self.GPIO and GPIO_ENABLED and self.GPIO1:
            for button in self.buttons.values():
                button.close()
                    
            for joystick in self.joysticks.values():
                joystick.close()   
    
if __name__ == "__main__":            
    # i = InputHandler()
    
    # print(i.is_pressed("UP"))
    # print(i.just_pressed("UP"))
    # print(i.left_joystick())
    # print(i.right_joystick())
    # print(i.get_axis("RIGHT", "X"))
    # i.cleanup()
    
    # while True:
    #     a = i.is_pressed("A")
    #     b = i.just_pressed("B")
    #     print(a)
    #     print(b)
        
    #     if a:
    #         print(a)
    #         break
        
    #     if b:
    #         print(b)
    #         break
    
    i = InputHandler()
    
    # Ďalšia potrebná inicializácia:
    # 1. Pygame vyžaduje okno, aby správne čítal vstup klávesnice na niektorých OS.
    # 2. Musíme spustiť event loop.
    
    if KEYBOARD_ENABLED:
        screen = pygame.display.set_mode((100, 100)) # Vytvoríme minimálne okno
        pygame.display.set_caption("Input Test")
        
    print("--- Test Start ---")
    
    while True:
        # 1. KĽÚČOVÝ KROK: Spracovanie udalostí Pygame
        # Toto aktualizuje stav klávesnice, ktorý číta get_pressed()
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                i.cleanup()
                pygame.quit()
                exit()
        
        # 2. Čítanie vstupu
        a = i.is_pressed("A")
        b = i.just_pressed("B")
        
        if a or b: # Aby to neflushovalo obrazovku tisíckami False
            print(f"is_pressed('A'): {a}, just_pressed('B'): {b}")
        
        # 3. Pridanie časového limitu, aby sa CPU nepreťažovalo
        time.sleep(1 / 60) # Spomalenie na 60 FPS
        
        # Prípadné ukončenie testu (ako si chcel Ty)
        if a or b:
            # Ak sa zaregistruje stlačenie, test skončí, aby si videl výstup.
            # Zmenil som to, aby program nepadol pri cleanup pred break.
            pass

        i.cleanup()
        pygame.quit()