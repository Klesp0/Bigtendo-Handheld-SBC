# Game template
import pygame
import sys
from config import *
from abc import ABC, abstractmethod
from _save_system import SaveSystem

class Game(ABC):
    def __init__(self, fullscreen, title, icon_path, game_name):
        
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
        
        self.save_system = SaveSystem()
        self.game_name = game_name
        self.highscore = self.save_system.get_highscore(self.game_name)
    
    @abstractmethod
    def handle_input(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def draw(self):
        pass
    
    def run(self):
        while self.running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.save_system.update_time(self.game_name)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        self.save_system.update_time(self.game_name)
                        
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
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.set_alpha(128)
        surface.fill("Black")
        self.screen.blit(surface, (0, 0))
        
        font = pygame.font.Font(None, 72)
        text = font.render("PAUSED", True, "Yellow")
        rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(text, rect)
    
if __name__ == "__main__":
    class TestGame(Game):
        def __init__(self, fullscreen=True, title="Game", icon_path=False):
            super().__init__(fullscreen, title, icon_path)
            
            self.player_surf = pygame.image.load("Games/shared/bird_flap_1.png").convert_alpha()
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