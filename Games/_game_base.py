# Game template
import pygame
import sys
from config import *
from abc import ABC, abstractmethod

class Game(ABC):
    def __init__(self, fullscreen, title, icon_path):
        
        pygame.init()
            
        if fullscreen:
            f = pygame.FULLSCREEN
            
        else:
            f = 0
         
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
             
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT),f)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.score = 0
    
    @abstractmethod
    def handle_input(self):

        # Spracovanie používateľského vstupu
        # Volá sa každý frame ak hra nie je pozastavená
        # Snake - zmena smeru
        # Clicking game - detekcia kliknutia
        # Racing - akcelerácia/brzdenie

        pass
    
    @abstractmethod
    def update(self):
  
        # Aktualizácia hernej logiky a stavu hry
        # Volá sa každý frame ak hra nie je pozastavená
        # Snake - pohyb hada, kolízie    
        # Platformer - fyzika, kolízie, AI
        # Flappy Bird - padanie, kolízie
        # Tower Defense - pohyb nepriateľov, strieľanie veží
  
        pass
    
    @abstractmethod
    def draw(self):
       
        # Vykreslenie všetkých objektov na obrazovku
        # Volá sa každý frame (aj keď je hra pozastavená)
        # Snake - pozadie, had, jablko, skóre
        # Platformer - pozadie, platformy, hráč, nepriatelia
        # Space Shooter - pozadie, hráč, nepriateľia, projektily
        # Menu - tlačidlá, text
    
        pass
    
    def run(self):
        # Main game loop
        while self.running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        
                    # tu bude pauzovanie hry
                    if event.key == pygame.K_p:
                        self.paused = not self.paused       
            
            if not self.paused:
                self.handle_input()
                self.update()
            
            self.draw()
            
            if self.paused:
                self.pause()
               
            pygame.display.flip() 
            self.clock.tick(FPS)
            
        
        pygame.quit()
        sys.exit()
                   
        return self.score
                   
    def pause(self):
        # Pause overlay
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.set_alpha(128)
        surface.fill("Black")
        self.screen.blit(surface, (0, 0))
        
        font = pygame.font.Font(None, 72)
        text = font.render("PAUSED", True, "Yellow")
        rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(text, rect)
    
# Test
if __name__ == "__main__":
    class TestGame(Game):
        def __init__(self, fullscreen=True, title="Game", icon_path=False):
            super().__init__(fullscreen, title, icon_path)
            
            self.player_surf = pygame.image.load("SW/shared/bird_flap_1.png").convert_alpha()
            self.player_rect = self.player_surf.get_rect(midbottom = (WIDTH/2, HEIGHT/2))
            self.rect = pygame.Rect(50, 50, 200, 100)
            self.stvorec = pygame.draw.rect(self.screen, "Blue", self.rect)
            
        def handle_input(self):
            pass
        
        def update(self):
            self.player_rect.right += 1
        
        def draw(self):
            self.screen.fill("Red")
            self.stvorec = pygame.draw.rect(self.screen, "Blue", self.rect)
            self.screen.blit(self.player_surf, self.player_rect)   
    
    
    game = TestGame(fullscreen=False, title="Hra")
    score = game.run()