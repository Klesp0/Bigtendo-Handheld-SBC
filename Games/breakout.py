import pygame
import random
from lib._game_base import Game
from lib.config import *


class Padle:
    def __init__(self, x, y, width, height, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.original_width = width
        self.expand_timer = None
        self.expand_duration = 5000 
        self.speed = 10
        self.screen = screen
    
    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0
    
    def move_right(self):
        self.x += self.speed
        if self.x + self.width > pygame.display.get_window_size()[0]:
            self.x = pygame.display.get_window_size()[0] - self.width
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self):
        pygame.draw.rect(self.screen, "Blue", self.get_rect())
    
    def collide_with_power_up(self, power_up, remove_lt, balls):
        if self.get_rect().colliderect(power_up.rect):
            remove_lt.append(power_up)
            if power_up.type == "expand_paddle":
                self.width = self.original_width * 2
                self.expand_timer = pygame.time.get_ticks()
            else:
                power_up.activate(power_up, balls, self.width)
        

class Ball:
    def __init__(self, x, y, dx=None, dy=None):
        self.x = x
        self.y = y
        
        if dx is None:
            self.dx = random.choice([-5, -4, -3, 3, 4, 5])
        else:
            self.dx = dx
        if dy is None:
            self.dy = -5
        else:
            self.dy = dy
            
        self.surf = pygame.image.load("Games/assets/images/breakout/ball_breakout.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (self.surf.get_width() * 3, self.surf.get_height() * 3))
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        self.radius = self.rect.width // 2
    
    def update(self, width, height):

        self.x += self.dx
        self.y += self.dy
        
        self.rect.center = (self.x, self.y)
        
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.dx = abs(self.dx)
        elif self.x + self.radius >= width:
            self.x = width - self.radius
            self.dx = -abs(self.dx)
        
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.dy = abs(self.dy)
    
    def is_out_of_bounds(self, height):
        return self.y - self.radius > height
    
    def collide_with_paddle(self, paddle_rect):

        if self.rect.colliderect(paddle_rect):

            if self.dy > 0:
                self.dy = -abs(self.dy)
                hit_pos = (self.x - paddle_rect.x) / paddle_rect.width
                self.dx += (hit_pos - 0.5) * 6
                self.dx = max(-8, min(8, self.dx))

                return True
        return False
    
    def collide_with_brick(self, brick_rect):

        if self.rect.colliderect(brick_rect):
            overlap_left = self.rect.right - brick_rect.left
            overlap_right = brick_rect.right - self.rect.left
            overlap_top = self.rect.bottom - brick_rect.top
            overlap_bottom = brick_rect.bottom - self.rect.top
            
            min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
            
            if min_overlap == overlap_top or min_overlap == overlap_bottom:
                self.dy = -self.dy
            else:
                self.dx = -self.dx
            
            return True
        return False

class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        i = random.randint(1, 100)
        if i in range(1, 71):
            self.color = "blue"
            self.b_score = 1
        elif i in range(71, 86):
            self.color = "green"
            self.b_score = 3
        elif i in range(86, 96):
            self.color = "orange"
            self.b_score = 5
        else:
            self.color = "red"
            self.b_score = 10
            
        self.surf = pygame.image.load(f"Games/assets/images/breakout/brick_{self.color}.png").convert_alpha()
        self.width = self.surf.get_width()
        self.height = self.surf.get_height()
        self.surf = pygame.transform.scale(self.surf, (self.width * 2, self.height * 2))
        self.rect = self.surf.get_rect(topleft=(self.x, self.y))


class PowerUp:
    def __init__(self, x, y, power_up_types):
        self.x = x
        self.y = y
        self.type = random.choice(power_up_types)

        if self.type == "multiball":
            self.surf = pygame.image.load("Games/assets/images/breakout/powerup_multiball.png").convert_alpha()
        elif self.type == "expand_paddle":
            self.surf = pygame.image.load("Games/assets/images/breakout/powerup_expand.png").convert_alpha()
        
        self.rect = self.surf.get_rect(center = (self.x, self.y))
    
    def update(self, dy):
        self.y += dy
        self.rect.centery = self.y

    def activate(self, power_up, balls, width):
        if power_up.type == "multiball":
            x = power_up.rect.centerx
            y = power_up.rect.centery
            balls.append(Ball(x, y, 0))
            balls.append(Ball(x, y, 5))
            balls.append(Ball(x, y, -5))
            return width


class Breakout(Game):
    def __init__(self, fullscreen=True):
        super().__init__(fullscreen, icon_path="Games/assets/images/breakout/breakout_icon.png", title="Breakout", game_name="Breakout")
        
        self.width = pygame.display.get_window_size()[0]
        self.height = pygame.display.get_window_size()[1]
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        self.game_state = 0
        
        self.sound_fail = pygame.mixer.Sound("Games/assets/sounds/fail.wav")
        self.sound_impact = pygame.mixer.Sound("Games/assets/sounds/impact.wav")
        self.sound_powerup = pygame.mixer.Sound("Games/assets/sounds/powerup.wav")
        pygame.mixer.music.load("Games/assets/sounds/music2.wav")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        
        self.paddle_width = 125 
        self.player = Padle(self.center_x - self.paddle_width / 2, self.height - 50, self.paddle_width, 10, self.screen)
        
        self.balls = [Ball(self.center_x, self.height - 150)]

        brick_surf = pygame.image.load(f"Games/assets/images/breakout/brick_blue.png").convert_alpha()
        self.brick_width = brick_surf.get_width()
        self.brick_height = brick_surf.get_height()
         
        self.bricks = []
        for i in range((self.height // self.brick_height - 15) // 2):
            for j in range(self.width // self.brick_width // 2):
                self.brick = Brick(j * self.brick_width * 2 + 5, i * (self.brick_height) * 2 + 10)
                self.bricks.append(self.brick)
        
        self.power_ups = []
        self.power_ups_types = ["multiball", "expand_paddle"]
        
        self.bg = pygame.image.load("Games/assets/images/breakout/breakout_bg.png").convert()
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        
        if GPIO_ENABLED:
            self.button = "A"
        else:
            self.button = "SPACE"
        
        self.font1 = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 50)
        self.font_surface = self.font1.render(f"Press '{self.button}' to start", False, "#16db65").convert_alpha()
        self.font_rect = self.font_surface.get_rect(center=(self.center_x, self.center_y))
        
        self.game_over_surface = self.font1.render("GAME OVER", False, "#ff0000").convert_alpha()
        self.game_over_rect = self.game_over_surface.get_rect(center=(self.center_x, self.center_y))
    
    def handle_input(self):
        if self.game_state == 0:
            if self.i.just_pressed("A"):
                self.game_state = 1
        
        elif self.game_state == 1:
            if self.i.is_pressed("RIGHT"):
                self.player.move_right()
            
            if self.i.is_pressed("LEFT"):
                self.player.move_left()
                
            joystick_x, _ = self.i.left_joystick()
            if abs(joystick_x) > 0.15: 
                self.player.x += joystick_x * self.player.speed
                self.player.x = max(0, min(self.player.x, self.width - self.player.width))
        
        elif self.game_state == 2:
            if self.i.just_pressed("A"):
                self.__init__(fullscreen=self.screen.get_flags() & pygame.FULLSCREEN)
        
    def update(self):
        if self.game_state == 1:

            if self.player.expand_timer is not None:
                if pygame.time.get_ticks() - self.player.expand_timer > self.player.expand_duration:
                    self.player.width = self.player.original_width
                    self.player.expand_timer = None

            balls_to_remove = []
            for ball in self.balls:
                ball.update(self.width, self.height)
                
                if ball.is_out_of_bounds(self.height):
                    balls_to_remove.append(ball)
                    continue
                
                if ball.collide_with_paddle(self.player.get_rect()):
                    self.sound_impact.play()

                bricks_to_remove = []
                for brick in self.bricks:
                    if len(bricks_to_remove) > 0:
                        continue
                    if ball.collide_with_brick(brick.rect):
                        bricks_to_remove.append(brick)
                        self.score += brick.b_score
                        self.sound_impact.play()

                if len(bricks_to_remove) > 0:
                    i = random.randint(1, 100)
                    chance = brick.b_score*6
                    if i <= chance:
                        center = bricks_to_remove[0].rect.center
                        self.power_ups.append(PowerUp(center[0],center[1],self.power_ups_types))

                    self.bricks.remove(bricks_to_remove[0])
            
            for power_up in self.power_ups:
                power_up.update(1)
            
            power_ups_remove = []
            for power_up in self.power_ups:
                if self.player.get_rect().colliderect(power_up.rect):
                    self.sound_powerup.play()
                self.player.collide_with_power_up(power_up, power_ups_remove, self.balls)
            
            for power_up in power_ups_remove:
                self.power_ups.remove(power_up)

            for ball in balls_to_remove:
                self.balls.remove(ball)
            
            if len(self.balls) == 0:
                self.sound_fail.play()
                self.game_state = 2
                self.save_system.update_score("Breakout", self.score)
    
    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        
        self.player.draw()
        
        for ball in self.balls:
            self.screen.blit(ball.surf, ball.rect)
        
        for brick in self.bricks:
            self.screen.blit(brick.surf, brick.rect)
        
        for power_up in self.power_ups:
            self.screen.blit(power_up.surf, power_up.rect)
        
        score_surface = self.font1.render(f"Score: {self.score}", False, "#FFFFFF").convert_alpha()
        self.screen.blit(score_surface, (10, 10))
        
        if self.game_state == 0:
            surface = pygame.Surface((self.width, self.height))
            surface.fill("Black")
            self.screen.blit(surface, (0, 0))
            highscore_text = self.font1.render(f"Best Score: {self.highscore}", False, "#FFD700").convert_alpha()
            highscore_rect = highscore_text.get_rect(center=(self.center_x, self.center_y - 60))
            self.screen.blit(highscore_text, highscore_rect)
            self.screen.blit(self.font_surface, self.font_rect)
        
        elif self.game_state == 2:
            surface = pygame.Surface((self.width, self.height))
            surface.set_alpha(128)
            surface.fill("Black")
            self.screen.blit(surface, (0, 0))
            self.screen.blit(self.game_over_surface, self.game_over_rect)
            
            restart_surface = self.font1.render(f"Press '{self.button}' to restart", False, "#16db65").convert_alpha()
            restart_rect = restart_surface.get_rect(center=(self.center_x, self.center_y + 60))
            self.screen.blit(restart_surface, restart_rect)
    
if __name__ == "__main__":
    breakout = Breakout(fullscreen=True)
    breakout.run()