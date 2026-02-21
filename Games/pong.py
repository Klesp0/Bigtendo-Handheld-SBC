import pygame
import random
from _game_base import Game
from _input_handler import InputHandler
from config import *


class Paddle:
    def __init__(self, x, y, image_path, player_num):
        self.player_num = player_num
        self.speed = 450
        
        self.surf = pygame.image.load(image_path).convert_alpha()
        self.surf = pygame.transform.scale(
            self.surf,
            (self.surf.get_width() * 8, self.surf.get_height() * 8)
        )
        
        if player_num == 1:
            self.rect = self.surf.get_rect(midright=(x, y))
        else:
            self.rect = self.surf.get_rect(midleft=(x, y))
    
    def move_up(self, dt):
        if self.rect.top > 0:
            self.rect.y -= self.speed * dt
    
    def move_down(self, dt, screen_height):
        if self.rect.bottom < screen_height:
            self.rect.y += self.speed * dt
    
    def draw(self, screen):
        screen.blit(self.surf, self.rect)
    
    def reset_position(self, y):
        if self.player_num == 1:
            self.rect.midright = (100, y)
        else:
            self.rect.midleft = (self.rect.centerx, y)


class Ball:
    def __init__(self, image_path):
        self.surf = pygame.image.load(image_path).convert_alpha()
        self.surf = pygame.transform.scale(
            self.surf,
            (self.surf.get_width() * 2, self.surf.get_height() * 2)
        )
        self.rect = self.surf.get_rect(center=(512, 300))
        
        self.speed = 300
        self.speed_mult = 1.0
        self.dx = 0
        self.dy = 0
    
    def reset(self):
        self.rect.center = (512, 300)
        self.speed_mult = 1.0
        self.dx = random.choice([-1, 1])
        self.dy = random.randint(-1, 1)
    
    def update(self, dt, screen_width, screen_height):
        self.rect.x += self.dx * self.speed * self.speed_mult * dt
        self.rect.y += self.dy * self.speed * self.speed_mult * dt
        
        if self.rect.top <= 0:
            self.rect.top = 0
            self.dy *= -1
        elif self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.dy *= -1
    
    def bounce_paddle(self):
        self.dx *= -1
        self.dy = random.randint(-2, 2)
        self.speed_mult += 0.10
    
    def draw(self, screen):
        screen.blit(self.surf, self.rect)


class Pong(Game):
    def __init__(self, fullscreen=True):
        super().__init__(
            fullscreen,
            icon_path="Games/assets/images/pong/pong_icon.png",
            title="Pong",
            game_name="Pong"
        )
        
        self.width = pygame.display.get_window_size()[0]
        self.height = pygame.display.get_window_size()[1]
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        
        # 0=mode select, 1=difficulty select (AI), 2=game menu, 3=playing, 4=game over
        self.game_state = 0
        
        self.selected_mode = 0
        self.selected_difficulty = 0
        self.game_mode = "multiplayer"
        self.ai_difficulty = "easy"
        
        self.score_p1 = 0
        self.score_p2 = 0
        self.winning_score = 10
        
        self.player1 = Paddle(100, self.center_y, "Games/assets/images/pong/pongPlayer.png", 1)
        self.player2 = Paddle(self.width - 100, self.center_y, "Games/assets/images/pong/pongPlayer2.png", 2)
        self.ball = Ball("Games/assets/images/pong/pongBall.png")
        
        self.line = pygame.image.load("Games/assets/images/pong/pongLine.png").convert_alpha()
        self.line = pygame.transform.scale(
            self.line,
            (self.line.get_width() * 6, self.line.get_height() * 20)
        )
        self.line_rect = self.line.get_rect(center=(self.center_x, self.center_y))
        
        self.scoreboard = pygame.image.load("Games/assets/images/pong/scoreBoard.png").convert_alpha()
        self.scoreboard = pygame.transform.scale(
            self.scoreboard,
            (self.scoreboard.get_width() * 4, self.scoreboard.get_height() * 4)
        )
        self.scoreboard_rect = self.scoreboard.get_rect(center=(self.center_x, 45))
        
        self.font_large = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 60)
        self.font_medium = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 50)
        self.font_small = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 40)
        
        self.bg = pygame.Surface((self.width, self.height))
        self.bg.fill("#000000")
        
        if GPIO_ENABLED:
            self.button = "A"
        else:
            self.button = "SPACE"
        
        pygame.mixer.music.load("Games/assets/sounds/music2.wav")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    
    def reset_scores(self):
        self.score_p1 = 0
        self.score_p2 = 0
    
    def handle_input(self):
        if self.game_state == 0:
            if self.i.just_pressed("UP"):
                self.selected_mode = (self.selected_mode - 1) % 2
            
            if self.i.just_pressed("DOWN"):
                self.selected_mode = (self.selected_mode + 1) % 2
            
            if self.i.just_pressed("A"):
                if self.selected_mode == 0:
                    self.game_mode = "singleplayer"
                    self.game_state = 1
                else:
                    self.game_mode = "multiplayer"
                    self.game_state = 2
        
        elif self.game_state == 1:
            if self.i.just_pressed("B"):
                self.game_state = 0
                
            if self.i.just_pressed("UP"):
                self.selected_difficulty = (self.selected_difficulty - 1) % 4
            
            if self.i.just_pressed("DOWN"):
                self.selected_difficulty = (self.selected_difficulty + 1) % 4
            
            if self.i.just_pressed("A"):
                difficulties = ["easy", "medium", "hard", "impossible"]
                self.ai_difficulty = difficulties[self.selected_difficulty]
                self.highscore = self.save_system.get_highscore(f"Pong_{self.ai_difficulty}")
                self.game_state = 2
        
        elif self.game_state == 2:
            if self.i.just_pressed("B"):
                self.game_state = 0
                
            if self.i.just_pressed("A"):
                self.game_state = 3
                self.ball.reset()
        
        elif self.game_state == 3:
            dt = self.clock.get_time() / 1000.0
             
            _, left_y = self.i.left_joystick()  
            
            if abs(left_y) > 0.1:
                self.player1.rect.y += left_y * self.player1.speed * dt
                self.player1.rect.y = max(0, min(self.player1.rect.y, self.height - self.player1.rect.height))
            
            if self.i.is_pressed("UP"):
                self.player1.move_up(dt)
            if self.i.is_pressed("DOWN"):
                self.player1.move_down(dt, self.height)
            
            if self.game_mode == "multiplayer":
                _, right_y = self.i.right_joystick()
                
                if abs(right_y) > 0.1:
                    self.player2.rect.y += right_y * self.player2.speed * dt
                    self.player2.rect.y = max(0, min(self.player2.rect.y, self.height - self.player2.rect.height))
                
                if self.i.is_pressed("Y"):
                    self.player2.move_up(dt)
                if self.i.is_pressed("B"):
                    self.player2.move_down(dt, self.height)
        
        elif self.game_state == 4:
            if self.i.just_pressed("A"):
                self.reset_scores()
                if self.game_mode == "singleplayer":
                    self.game_state = 1
                else:
                    self.game_state = 2
    
    def update(self):
        if self.game_state == 3:
            dt = self.clock.get_time() / 1000.0
            dt = max(0.001, min(0.1, dt))
            
            if self.game_mode == "singleplayer":
                self.update_ai(dt)
            
            self.ball.update(dt, self.width, self.height)
            
            if self.ball.rect.colliderect(self.player1.rect) and self.ball.dx < 0:
                self.ball.bounce_paddle()
            
            if self.ball.rect.colliderect(self.player2.rect) and self.ball.dx > 0:
                self.ball.bounce_paddle()
            
            if self.ball.rect.right < 0:
                self.score_p2 += 1
                self.ball.reset()
            
            elif self.ball.rect.left > self.width:
                self.score_p1 += 1
                self.ball.reset()
            
            if self.score_p1 >= self.winning_score or self.score_p2 >= self.winning_score:
                self.game_state = 4
                
                if self.game_mode == "singleplayer":
                    self.save_system.update_score(f"Pong_{self.ai_difficulty}", self.score_p1)
                    if self.score_p1 > self.highscore:
                        self.highscore = self.score_p1
    
    def update_ai(self, dt):
        ai_speeds = {
            "easy": 250,
            "medium": 350,
            "hard": 450,
            "impossible": 600
        }
        
        ai_speed = ai_speeds.get(self.ai_difficulty, 350)
        
        ball_center_y = self.ball.rect.centery
        paddle_center_y = self.player2.rect.centery
        
        tolerance = 20
        
        if ball_center_y < paddle_center_y - tolerance:
            if self.player2.rect.top > 0:
                self.player2.rect.y -= ai_speed * dt
        elif ball_center_y > paddle_center_y + tolerance:
            if self.player2.rect.bottom < self.height:
                self.player2.rect.y += ai_speed * dt
    
    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        
        if self.game_state == 0:
            self.draw_mode_select()
        
        elif self.game_state == 1:
            self.draw_difficulty_select()
        
        elif self.game_state == 2:
            self.draw_game_menu()
        
        elif self.game_state == 3:
            self.draw_game()
        
        elif self.game_state == 4:
            self.draw_game_over()
    
    def draw_mode_select(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill("black")
        self.screen.blit(overlay, (0, 0))
        
        title = self.font_large.render("PONG", True, "white")
        title_rect = title.get_rect(center=(self.center_x, self.center_y - 150))
        self.screen.blit(title, title_rect)
        
        singleplayer_color = "yellow" if self.selected_mode == 0 else "white"
        singleplayer_text = self.font_medium.render("SINGLEPLAYER", True, singleplayer_color)
        singleplayer_rect = singleplayer_text.get_rect(center=(self.center_x, self.center_y - 30))
        self.screen.blit(singleplayer_text, singleplayer_rect)
        
        multiplayer_color = "yellow" if self.selected_mode == 1 else "white"
        multiplayer_text = self.font_medium.render("2 PLAYERS", True, multiplayer_color)
        multiplayer_rect = multiplayer_text.get_rect(center=(self.center_x, self.center_y + 30))
        self.screen.blit(multiplayer_text, multiplayer_rect)
        
        arrow = self.font_large.render(">", True, "yellow")
        arrow_y = self.center_y - 30 if self.selected_mode == 0 else self.center_y + 30
        arrow_rect = arrow.get_rect(center=(self.center_x - 250, arrow_y))
        self.screen.blit(arrow, arrow_rect)
        
        start_text = f"Press '{self.button}' to select"
        start_surf = self.font_small.render(start_text, True, "gray")
        start_rect = start_surf.get_rect(center=(self.center_x, self.center_y + 120))
        self.screen.blit(start_surf, start_rect)
    
    def draw_difficulty_select(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill("black")
        self.screen.blit(overlay, (0, 0))
        
        title = self.font_large.render("SELECT AI DIFFICULTY", True, "#16db65")
        title_rect = title.get_rect(center=(self.center_x, self.center_y - 180))
        self.screen.blit(title, title_rect)
        
        difficulties = [
            ("EASY", 0),
            ("MEDIUM", 1),
            ("HARD", 2),
            ("IMPOSSIBLE", 3)
        ]
        
        for diff_name, diff_index in difficulties:
            color = "yellow" if self.selected_difficulty == diff_index else "white"
            y_pos = self.center_y - 60 + (diff_index * 50)
            
            diff_text = self.font_medium.render(diff_name, True, color)
            diff_rect = diff_text.get_rect(center=(self.center_x, y_pos))
            self.screen.blit(diff_text, diff_rect)
        
        arrow = self.font_large.render(">", True, "yellow")
        arrow_y = self.center_y - 60 + (self.selected_difficulty * 50)
        arrow_rect = arrow.get_rect(center=(self.center_x - 200, arrow_y))
        self.screen.blit(arrow, arrow_rect)
        
        instruction = self.font_small.render(f"Press '{self.button}' to select", True, "gray")
        instruction_rect = instruction.get_rect(center=(self.center_x, self.center_y + 150))
        self.screen.blit(instruction, instruction_rect)
    
    def draw_game_menu(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill("black")
        self.screen.blit(overlay, (0, 0))
        
        title = self.font_large.render("PONG", True, "white")
        title_rect = title.get_rect(center=(self.center_x, self.center_y - 100))
        self.screen.blit(title, title_rect)
        
        if self.game_mode == "singleplayer":
            mode_text = f"Mode: SINGLEPLAYER (AI: {self.ai_difficulty.upper()})"
            mode_surf = self.font_medium.render(mode_text, True, "yellow")
            mode_rect = mode_surf.get_rect(center=(self.center_x, self.center_y - 20))
            self.screen.blit(mode_surf, mode_rect)
            
            highscore_text = self.font_medium.render(f"Best Score: {self.highscore}", True, "#FFD700")
            highscore_rect = highscore_text.get_rect(center=(self.center_x, self.center_y + 40))
            self.screen.blit(highscore_text, highscore_rect)
            
            start_y = self.center_y + 120
        else:
            mode_text = "Mode: 2 PLAYERS"
            mode_surf = self.font_medium.render(mode_text, True, "yellow")
            mode_rect = mode_surf.get_rect(center=(self.center_x, self.center_y))
            self.screen.blit(mode_surf, mode_rect)
            
            start_y = self.center_y + 100
        
        start_text = f"Press '{self.button}' to start"
        start_surf = self.font_medium.render(start_text, True, "white")
        start_rect = start_surf.get_rect(center=(self.center_x, start_y))
        self.screen.blit(start_surf, start_rect)
    
    def draw_game(self):
        self.screen.blit(self.line, self.line_rect)
        self.screen.blit(self.scoreboard, self.scoreboard_rect)
        
        score_text = self.font_medium.render(f"{self.score_p1}    {self.score_p2}", True, "#000000")
        score_rect = score_text.get_rect(center=(self.center_x, 50))
        self.screen.blit(score_text, score_rect)
        
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        self.ball.draw(self.screen)
    
    def draw_game_over(self):
        self.screen.blit(self.line, self.line_rect)
        self.screen.blit(self.scoreboard, self.scoreboard_rect)
        
        score_text = self.font_medium.render(f"{self.score_p1}    {self.score_p2}", True, "#000000")
        score_rect = score_text.get_rect(center=(self.center_x, 50))
        self.screen.blit(score_text, score_rect)
        
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        self.ball.draw(self.screen)
        
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill("black")
        self.screen.blit(overlay, (0, 0))
        
        if self.score_p1 >= self.winning_score:
            winner_text = self.font_large.render("PLAYER 1 WON!", True, "#FFD700")
        else:
            winner_text = self.font_large.render("PLAYER 2 WON!", True, "#FFD700")
        
        winner_rect = winner_text.get_rect(center=(self.center_x, self.center_y - 50))
        self.screen.blit(winner_text, winner_rect)
        
        score_surf = self.font_medium.render(f"Final Score: {self.score_p1} - {self.score_p2}", True, "white")
        score_surf_rect = score_surf.get_rect(center=(self.center_x, self.center_y + 30))
        self.screen.blit(score_surf, score_surf_rect)
        
        restart_text = f"Press '{self.button}' to restart"
        restart_surf = self.font_medium.render(restart_text, True, "#16db65")
        restart_rect = restart_surf.get_rect(center=(self.center_x, self.center_y + 120))
        self.screen.blit(restart_surf, restart_rect)
        
        if self.game_mode == "singleplayer":
            if self.score_p1 >= self.winning_score and self.score_p1 > self.highscore:
                record_text = "NEW RECORD!"
                record_surf = self.font_medium.render(record_text, True, "red")
                record_rect = record_surf.get_rect(center=(self.center_x, self.center_y - 120))
                self.screen.blit(record_surf, record_rect)


if __name__ == "__main__":
    pong = Pong(fullscreen=True)
    pong.run()