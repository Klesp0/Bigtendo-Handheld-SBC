import pygame
import random
import sys
from _game_base import Game
from _input_handler import InputHandler
from config import *


class Snake:
    def __init__(self, x, y, cell_size):
        self.cell_size = cell_size
        self.body = [(x, y), (x - cell_size, y), (x - 2 * cell_size, y)]
        self.direction = (1, 0)  # vpravo
        self.next_direction = (1, 0)
        self.grow = False
        
        # TODO: Načítaj obrázky
        # self.head_img = pygame.image.load("Games/assets/images/snake/snake_head.png")
        # self.body_img = pygame.image.load("Games/assets/images/snake/snake_body.png")
        # self.tail_img = pygame.image.load("Games/assets/images/snake/snake_tail.png")
        
    def move(self):
        self.direction = self.next_direction
        
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0] * self.cell_size,
                    head_y + self.direction[1] * self.cell_size)
        
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.next_direction = new_direction
    
    def grow_snake(self):
        self.grow = True
    
    def check_collision(self, width, height, walls_enabled):
        head_x, head_y = self.body[0]
        
        # Kolízia s vlastným telom
        if (head_x, head_y) in self.body[1:]:
            return True
        
        # Kolízia so stenami (iba ak sú zapnuté)
        if walls_enabled:
            if (head_x < 0 or head_x >= width or 
                head_y < 0 or head_y >= height):
                return True
        else:
            # Teleportácia cez steny
            if head_x < 0:
                self.body[0] = (width - self.cell_size, head_y)
            elif head_x >= width:
                self.body[0] = (0, head_y)
            elif head_y < 0:
                self.body[0] = (head_x, height - self.cell_size)
            elif head_y >= height:
                self.body[0] = (head_x, 0)
        
        return False
    
    def draw(self, screen):
        for i, segment in enumerate(self.body):
            if i == 0:
                # Hlava
                color = "darkgreen"
            elif i == len(self.body) - 1:
                # Chvost
                color = "green"
            else:
                # Telo
                color = "lime"
            
            rect = pygame.Rect(segment[0], segment[1], self.cell_size, self.cell_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, "darkgreen", rect, 2)


class Food:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.position = (0, 0)
        
        # TODO: Načítaj obrázok
        # self.img = pygame.image.load("Games/assets/images/snake/apple.png")
    
    def spawn(self, snake_body, width, height):
        while True:
            x = random.randint(0, (width - self.cell_size) // self.cell_size) * self.cell_size
            y = random.randint(0, (height - self.cell_size) // self.cell_size) * self.cell_size
            
            if (x, y) not in snake_body:
                self.position = (x, y)
                break
    
    def draw(self, screen):
        rect = pygame.Rect(self.position[0], self.position[1], 
                          self.cell_size, self.cell_size)
        pygame.draw.rect(screen, "red", rect)
        pygame.draw.rect(screen, "darkred", rect, 2)


class SnakeGame(Game):
    def __init__(self, fullscreen=True):
        super().__init__(
            fullscreen,
            icon_path="Games/assets/images/snake/snake_icon.png",  # TODO: Doplň cestu
            title="Snake",
            game_name="Snake"
        )
        
        self.width = pygame.display.get_window_size()[0]
        self.height = pygame.display.get_window_size()[1]
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        
        self.i = InputHandler()
        
        # 0=difficulty select, 1=game menu, 2=playing, 3=game over
        self.game_state = 0
        
        self.selected_difficulty = 0
        self.difficulty = "medium"
        
        self.cell_size = 20
        self.walls_enabled = True
        self.game_speed = 10
        
        self.snake = Snake(self.width // 2, self.height // 2, self.cell_size)
        self.food = Food(self.cell_size)
        self.food.spawn(self.snake.body, self.width, self.height)
        
        self.move_counter = 0
        self.move_delay = 10
        
        self.font_large = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 60)
        self.font_medium = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 50)
        self.font_small = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 40)
        
        # TODO: Načítaj pozadie
        # self.bg = pygame.image.load("Games/assets/images/snake/background.png")
        # self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.bg = pygame.Surface((self.width, self.height))
        self.bg.fill("#2d5016")
        
        if self.i.GPIO1 and GPIO_ENABLED and self.i.GPIO:
            self.button = "A"
        else:
            self.button = "SPACE"
    
    def reset_game(self):
        self.score = 0
        self.snake = Snake(self.width // 2, self.height // 2, self.cell_size)
        self.food = Food(self.cell_size)
        self.food.spawn(self.snake.body, self.width, self.height)
        self.move_counter = 0
    
    def handle_input(self):
        if self.game_state == 0:
            if self.i.just_pressed("UP"):
                self.selected_difficulty = (self.selected_difficulty - 1) % 4
            
            if self.i.just_pressed("DOWN"):
                self.selected_difficulty = (self.selected_difficulty + 1) % 4
            
            if self.i.just_pressed("A"):
                difficulties = {
                    0: ("easy", False, 7),      # walls OFF, pomalé
                    1: ("medium", False, 10),   # walls OFF, stredné
                    2: ("hard", True, 10),      # walls ON, stredné
                    3: ("extreme", True, 15)    # walls ON, rýchle
                }
                
                diff_data = difficulties[self.selected_difficulty]
                self.difficulty = diff_data[0]
                self.walls_enabled = diff_data[1]
                self.move_delay = diff_data[2]
                
                self.highscore = self.save_system.get_highscore(f"Snake_{self.difficulty}")
                self.game_state = 1
        
        elif self.game_state == 1:
            # BACK - návrat na difficulty select
            if self.i.just_pressed("B"):
                self.game_state = 0
            
            if self.i.just_pressed("A"):
                self.reset_game()
                self.game_state = 2
        
        elif self.game_state == 2:
            if self.i.just_pressed("UP"):
                self.snake.change_direction((0, -1))
            elif self.i.just_pressed("DOWN"):
                self.snake.change_direction((0, 1))
            elif self.i.just_pressed("LEFT"):
                self.snake.change_direction((-1, 0))
            elif self.i.just_pressed("RIGHT"):
                self.snake.change_direction((1, 0))
        
        elif self.game_state == 3:
            if self.i.just_pressed("A"):
                self.__init__(fullscreen=self.screen.get_flags() & pygame.FULLSCREEN)
    
    def update(self):
        if self.game_state == 2:
            self.move_counter += 1
            
            if self.move_counter >= self.move_delay:
                self.move_counter = 0
                self.snake.move()
                
                if self.snake.check_collision(self.width, self.height, self.walls_enabled):
                    self.game_state = 3
                    self.save_system.update_score(f"Snake_{self.difficulty}", self.score)
                    if self.score > self.highscore:
                        self.highscore = self.score
                
                if self.snake.body[0] == self.food.position:
                    self.snake.grow_snake()
                    self.food.spawn(self.snake.body, self.width, self.height)
                    self.score += 10
    
    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        
        if self.game_state == 0:
            self.draw_difficulty_select()
        
        elif self.game_state == 1:
            self.draw_game_menu()
        
        elif self.game_state == 2:
            self.draw_game()
        
        elif self.game_state == 3:
            self.draw_game_over()
    
    def draw_difficulty_select(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill("black")
        self.screen.blit(overlay, (0, 0))
        
        title = self.font_large.render("SELECT DIFFICULTY", True, "#16db65")
        title_rect = title.get_rect(center=(self.center_x, self.center_y - 200))
        self.screen.blit(title, title_rect)
        
        difficulties = [
            ("EASY (No Walls, Slow)", 0),
            ("MEDIUM (No Walls, Normal)", 1),
            ("HARD (Walls, Normal)", 2),
            ("EXTREME (Walls, Fast)", 3)
        ]
        
        for diff_name, diff_index in difficulties:
            color = "yellow" if self.selected_difficulty == diff_index else "white"
            y_pos = self.center_y - 80 + (diff_index * 50)
            
            diff_text = self.font_medium.render(diff_name, True, color)
            diff_rect = diff_text.get_rect(center=(self.center_x, y_pos))
            self.screen.blit(diff_text, diff_rect)
        
        arrow = self.font_large.render(">", True, "yellow")
        arrow_y = self.center_y - 80 + (self.selected_difficulty * 50)
        arrow_rect = arrow.get_rect(center=(self.center_x - 350, arrow_y))
        self.screen.blit(arrow, arrow_rect)
        
        instruction = self.font_small.render(f"Press '{self.button}' to select", True, "gray")
        instruction_rect = instruction.get_rect(center=(self.center_x, self.center_y + 150))
        self.screen.blit(instruction, instruction_rect)
    
    def draw_game_menu(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill("black")
        self.screen.blit(overlay, (0, 0))
        
        title = self.font_large.render("SNAKE", True, "white")
        title_rect = title.get_rect(center=(self.center_x, self.center_y - 120))
        self.screen.blit(title, title_rect)
        
        walls_text = "Walls: ON" if self.walls_enabled else "Walls: OFF"
        speed_text = "Speed: FAST" if self.move_delay <= 7 else ("Speed: NORMAL" if self.move_delay == 10 else "Speed: SLOW")
        
        diff_text = f"Difficulty: {self.difficulty.upper()}"
        diff_surf = self.font_medium.render(diff_text, True, "yellow")
        diff_rect = diff_surf.get_rect(center=(self.center_x, self.center_y - 40))
        self.screen.blit(diff_surf, diff_rect)
        
        walls_surf = self.font_small.render(walls_text, True, "white")
        walls_rect = walls_surf.get_rect(center=(self.center_x, self.center_y + 10))
        self.screen.blit(walls_surf, walls_rect)
        
        speed_surf = self.font_small.render(speed_text, True, "white")
        speed_rect = speed_surf.get_rect(center=(self.center_x, self.center_y + 50))
        self.screen.blit(speed_surf, speed_rect)
        
        highscore_text = self.font_medium.render(f"Best Score: {self.highscore}", True, "#FFD700")
        highscore_rect = highscore_text.get_rect(center=(self.center_x, self.center_y + 110))
        self.screen.blit(highscore_text, highscore_rect)
        
        start_text = f"Press '{self.button}' to start"
        start_surf = self.font_medium.render(start_text, True, "white")
        start_rect = start_surf.get_rect(center=(self.center_x, self.center_y + 180))
        self.screen.blit(start_surf, start_rect)
        
        # Nápis pre návrat späť
        back_text = "Press 'B' to go back"
        back_surf = self.font_small.render(back_text, True, "gray")
        back_rect = back_surf.get_rect(center=(self.center_x, self.center_y + 240))
        self.screen.blit(back_surf, back_rect)
    
    def draw_game(self):
        self.food.draw(self.screen)
        self.snake.draw(self.screen)
        
        score_surf = self.font_medium.render(f"Score: {self.score}", True, "white")
        self.screen.blit(score_surf, (20, 20))
        
        highscore_surf = self.font_small.render(f"Best: {self.highscore}", True, "gold")
        self.screen.blit(highscore_surf, (20, 70))
    
    def draw_game_over(self):
        self.food.draw(self.screen)
        self.snake.draw(self.screen)
        
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill("black")
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render("GAME OVER", True, "red")
        game_over_rect = game_over_text.get_rect(center=(self.center_x, self.center_y - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        score_text = f"Your Score: {self.score}"
        score_surf = self.font_medium.render(score_text, True, "white")
        score_rect = score_surf.get_rect(center=(self.center_x, self.center_y - 20))
        self.screen.blit(score_surf, score_rect)
        
        length_text = f"Snake Length: {len(self.snake.body)}"
        length_surf = self.font_medium.render(length_text, True, "white")
        length_rect = length_surf.get_rect(center=(self.center_x, self.center_y + 30))
        self.screen.blit(length_surf, length_rect)
        
        restart_text = f"Press '{self.button}' to restart"
        restart_surf = self.font_medium.render(restart_text, True, "#16db65")
        restart_rect = restart_surf.get_rect(center=(self.center_x, self.center_y + 120))
        self.screen.blit(restart_surf, restart_rect)
        
        if self.score > self.highscore:
            record_text = "NEW RECORD!"
            record_surf = self.font_medium.render(record_text, True, "gold")
            record_rect = record_surf.get_rect(center=(self.center_x, self.center_y - 160))
            self.screen.blit(record_surf, record_rect)
    
    def run(self):
        while self.running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.save_system.update_time(f"Snake_{self.difficulty}")
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        self.save_system.update_time(f"Snake_{self.difficulty}")
                        
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


if __name__ == "__main__":
    snake = SnakeGame(fullscreen=False)
    snake.run()