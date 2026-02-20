import pygame
import random
import time
from pygame.math import Vector2
from _game_base import Game
from _input_handler import InputHandler
from config import *


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load('Games/assets/images/snake/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Games/assets/images/snake/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Games/assets/images/snake/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Games/assets/images/snake/head_left.png').convert_alpha()
        
        self.tail_up = pygame.image.load('Games/assets/images/snake/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Games/assets/images/snake/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Games/assets/images/snake/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Games/assets/images/snake/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Games/assets/images/snake/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Games/assets/images/snake/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Games/assets/images/snake/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Games/assets/images/snake/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Games/assets/images/snake/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Games/assets/images/snake/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Games/assets/sounds/crunch.wav')

    def draw_snake(self, screen, cell_size):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0): 
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0): 
            self.head = self.head_right
        elif head_relation == Vector2(0, 1): 
            self.head = self.head_up
        elif head_relation == Vector2(0, -1): 
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): 
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): 
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): 
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): 
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class FRUIT:
    def __init__(self, cell_number_x, cell_number_y):
        self.cell_number_x = cell_number_x
        self.cell_number_y = cell_number_y
        self.randomize()

    def draw_fruit(self, screen, apple, cell_size):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, self.cell_number_x - 1)
        self.y = random.randint(0, self.cell_number_y - 1)
        self.pos = Vector2(self.x, self.y)


class SnakeGame(Game):
    def __init__(self, fullscreen=True, difficulty="easy"):
        super().__init__(
            fullscreen,
            icon_path="Games/assets/images/snake/snake_icon.png",
            title="Snake",
            game_name="Snake"
        )
        
        pygame.mixer.pre_init(44100, -16, 2, 512)
        
        self.width = pygame.display.get_window_size()[0]
        self.height = pygame.display.get_window_size()[1]
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        
        self.i = InputHandler()
        
        self.difficulty = difficulty
        if difficulty == "easy":
            self.cell_size = 40
            self.base_update_speed = 150  
        else:
            self.cell_size = 30
            self.base_update_speed = 100
        
        self.update_speed = self.base_update_speed
        
        self.cell_number_x = self.width // self.cell_size
        self.cell_number_y = self.height // self.cell_size
        
        self.game_state = 0
        self.selected_difficulty = 0
        
        self.apple = pygame.image.load('Games/assets/images/snake/apple.png').convert_alpha()
        self.apple = pygame.transform.scale(self.apple, (self.cell_size, self.cell_size))
        
        self.snake = SNAKE()
        self.fruit = FRUIT(self.cell_number_x, self.cell_number_y)
        
        self.last_update = pygame.time.get_ticks()
        self.start_time = 0
        self.elapsed_time = 0
        self.apples_eaten = 0  
        
        self.font_large = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 60)
        self.font_medium = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 40)
        self.font_small = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 30)
        
        self.bg = pygame.Surface((self.width, self.height))
        self.bg.fill((175, 215, 70))
        
        if self.i.GPIO1 and GPIO_ENABLED and self.i.GPIO:
            self.button = "A"
        else:
            self.button = "SPACE"
        
        pygame.mixer.music.load("Games\\assets\\sounds\\music2.wav")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    
    def handle_input(self):
        if self.game_state == 0:
            if self.i.just_pressed("UP"):
                self.selected_difficulty = (self.selected_difficulty - 1) % 2
            
            if self.i.just_pressed("DOWN"):
                self.selected_difficulty = (self.selected_difficulty + 1) % 2
            
            if self.i.just_pressed("A"):
                if self.selected_difficulty == 0:
                    self.difficulty = "easy"
                    self.cell_size = 40
                    self.base_update_speed = 150
                else:
                    self.difficulty = "hard"
                    self.cell_size = 30
                    self.base_update_speed = 100
                
                self.update_speed = self.base_update_speed
                self.cell_number_x = self.width // self.cell_size
                self.cell_number_y = self.height // self.cell_size
                
                self.apple = pygame.transform.scale(
                    pygame.image.load('Games/assets/images/snake/apple.png').convert_alpha(),
                    (self.cell_size, self.cell_size)
                )
                self.snake = SNAKE()
                self.fruit = FRUIT(self.cell_number_x, self.cell_number_y)
                self.highscore = self.save_system.get_highscore(f"Snake_{self.difficulty}")
                self.game_state = 1
        
        elif self.game_state == 1:
            if self.i.just_pressed("B"):
                self.game_state = 0
            
            if self.i.just_pressed("A"):
                self.game_state = 2
                self.start_time = time.time()
                self.last_update = pygame.time.get_ticks()
                self.update_speed = self.base_update_speed
                self.apples_eaten = 0
                self.snake.reset()
                self.fruit.randomize()
        
        elif self.game_state == 2:
            if self.i.just_pressed("UP"):
                if self.snake.direction.y != 1:
                    self.snake.direction = Vector2(0, -1)
            
            if self.i.just_pressed("DOWN"):
                if self.snake.direction.y != -1:
                    self.snake.direction = Vector2(0, 1)
            
            if self.i.just_pressed("LEFT"):
                if self.snake.direction.x != 1:
                    self.snake.direction = Vector2(-1, 0)
            
            if self.i.just_pressed("RIGHT"):
                if self.snake.direction.x != -1:
                    self.snake.direction = Vector2(1, 0)
        
        elif self.game_state == 3:
            if self.i.just_pressed("A"):
                self.game_state = 0
                self.selected_difficulty = 0
    
    def update(self):
        if self.game_state == 2:
            self.elapsed_time = time.time() - self.start_time
            
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update >= self.update_speed:
                self.last_update = current_time
                
                if self.snake.direction != Vector2(0, 0):
                    self.snake.move_snake()
                    self.check_collision()
                    self.check_fail()
    
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.apples_eaten += 1
            
            self.update_speed = max(60, self.base_update_speed - self.apples_eaten * 5)
        
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
    
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < self.cell_number_x or not 0 <= self.snake.body[0].y < self.cell_number_y:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    
    def game_over(self):
        self.game_state = 3
        self.save_system.update_score(f"Snake_{self.difficulty}", self.calculate_score())
    
    def calculate_score(self):
        difficulty_mult = 2 if self.difficulty == "hard" else 1
        return self.apples_eaten * 10 * difficulty_mult
    
    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(self.cell_number_y):
            if row % 2 == 0:
                for col in range(self.cell_number_x):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * self.cell_size, row * self.cell_size, 
                                                 self.cell_size, self.cell_size)
                        pygame.draw.rect(self.screen, grass_color, grass_rect)
            else:
                for col in range(self.cell_number_x):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * self.cell_size, row * self.cell_size, 
                                                 self.cell_size, self.cell_size)
                        pygame.draw.rect(self.screen, grass_color, grass_rect)
    
    def draw_score(self):
        score_text = str(self.apples_eaten)
        score_surface = self.font_small.render(score_text, True, (56, 74, 12))
        score_x = int(self.width - 80)
        score_y = int(self.height - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = self.apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, 
                             apple_rect.width + score_rect.width + 6, apple_rect.height)
        
        pygame.draw.rect(self.screen, (167, 209, 61), bg_rect)
        self.screen.blit(score_surface, score_rect)
        self.screen.blit(self.apple, apple_rect)
        pygame.draw.rect(self.screen, (56, 74, 12), bg_rect, 2)
    
    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        
        if self.game_state == 0:
            self.draw_difficulty_select()
        
        elif self.game_state == 1:
            self.draw_menu()
        
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
        title_rect = title.get_rect(center=(self.center_x, self.center_y - 150))
        self.screen.blit(title, title_rect)
        
        easy_color = "yellow" if self.selected_difficulty == 0 else "white"
        easy_text = self.font_medium.render("EASY (40px cells, Slow)", True, easy_color)
        easy_rect = easy_text.get_rect(center=(self.center_x, self.center_y - 20))
        self.screen.blit(easy_text, easy_rect)
        
        hard_color = "yellow" if self.selected_difficulty == 1 else "white"
        hard_text = self.font_medium.render("HARD (30px cells, Fast)", True, hard_color)
        hard_rect = hard_text.get_rect(center=(self.center_x, self.center_y + 40))
        self.screen.blit(hard_text, hard_rect)
        
        arrow = self.font_large.render(">", True, "yellow")
        arrow_y = self.center_y - 20 if self.selected_difficulty == 0 else self.center_y + 40
        arrow_rect = arrow.get_rect(center=(self.center_x - 250, arrow_y))
        self.screen.blit(arrow, arrow_rect)
        
        instruction = self.font_small.render(f"Press '{self.button}' to select", True, "gray")
        instruction_rect = instruction.get_rect(center=(self.center_x, self.center_y + 120))
        self.screen.blit(instruction, instruction_rect)
    
    def draw_menu(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill("black")
        self.screen.blit(overlay, (0, 0))
        
        title = self.font_large.render("SNAKE", True, "#16db65")
        title_rect = title.get_rect(center=(self.center_x, self.center_y - 100))
        self.screen.blit(title, title_rect)
        
        diff_text = f"Difficulty: {self.difficulty.upper()} ({self.cell_number_x}x{self.cell_number_y})"
        diff_surf = self.font_medium.render(diff_text, True, "yellow")
        diff_rect = diff_surf.get_rect(center=(self.center_x, self.center_y - 20))
        self.screen.blit(diff_surf, diff_rect)
        
        highscore_text = self.font_medium.render(f"Best Score: {self.highscore}", True, "#FFD700")
        highscore_rect = highscore_text.get_rect(center=(self.center_x, self.center_y + 40))
        self.screen.blit(highscore_text, highscore_rect)
        
        start_text = f"Press '{self.button}' to start"
        start_surf = self.font_medium.render(start_text, True, "white")
        start_rect = start_surf.get_rect(center=(self.center_x, self.center_y + 120))
        self.screen.blit(start_surf, start_rect)
    
    def draw_game(self):
        self.draw_grass()
        self.fruit.draw_fruit(self.screen, self.apple, self.cell_size)
        self.snake.draw_snake(self.screen, self.cell_size)
        self.draw_score()
        
        time_str = f"Time: {int(self.elapsed_time)}s"
        time_surf = self.font_small.render(time_str, True, (56, 74, 12))
        self.screen.blit(time_surf, (20, 20))
        
        highscore_surf = self.font_small.render(f"Best: {self.highscore}", True, (56, 74, 12))
        self.screen.blit(highscore_surf, (20, 50))
        
        score_surf = self.font_small.render(f"Score: {self.calculate_score()}", True, (56, 74, 12))
        self.screen.blit(score_surf, (20, 80))
    
    def draw_game_over(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill("black")
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render("GAME OVER", True, "red")
        game_over_rect = game_over_text.get_rect(center=(self.center_x, self.center_y - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        final_score = self.calculate_score()
        score_surf = self.font_medium.render(f"Score: {final_score}", True, "white")
        score_rect = score_surf.get_rect(center=(self.center_x, self.center_y - 20))
        self.screen.blit(score_surf, score_rect)
        
        apples_surf = self.font_medium.render(f"Apples: {self.apples_eaten}", True, "white")
        apples_rect = apples_surf.get_rect(center=(self.center_x, self.center_y + 30))
        self.screen.blit(apples_surf, apples_rect)
        
        time_surf = self.font_medium.render(f"Time: {int(self.elapsed_time)}s", True, "white")
        time_rect = time_surf.get_rect(center=(self.center_x, self.center_y + 80))
        self.screen.blit(time_surf, time_rect)
        
        restart_surf = self.font_medium.render(f"Press '{self.button}' to return to menu", True, "#16db65")
        restart_rect = restart_surf.get_rect(center=(self.center_x, self.center_y + 150))
        self.screen.blit(restart_surf, restart_rect)
        
        if final_score > self.highscore:
            record_surf = self.font_medium.render("NEW RECORD!", True, "yellow")
            record_rect = record_surf.get_rect(center=(self.center_x, self.center_y - 150))
            self.screen.blit(record_surf, record_rect)

if __name__ == "__main__":
    snake_game = SnakeGame(fullscreen=True, difficulty="easy")
    snake_game.run()