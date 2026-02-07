import pygame
import random
import time
from _game_base import Game
from _input_handler import InputHandler
from config import *


class Card:
    def __init__(self, x, y, card_type, card_id):
        self.x = x
        self.y = y
        self.card_type = card_type  
        self.card_id = card_id  
        self.is_flipped = False  
        self.is_matched = False  
        self.flip_progress = 0.0  
        
        self.width = 100
        self.height = 100
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Načítanie obrázkov (TODO: doplň cesty k obrázkom)
        # self.front_img = pygame.image.load(f"SW/assets/images/pexeso/{card_type}.png")
        # self.front_img = pygame.transform.scale(self.front_img, (self.width, self.height))
        
        self.front_surf = pygame.Surface((self.width, self.height))
        self.color_map = {
            "apple": "red",
            "banana": "yellow", 
            "cherry": "darkred",
            "grape": "purple",
            "orange": "orange",
            "strawberry": "pink",
            "watermelon": "green",
            "pineapple": "gold",
            "kiwi": "red",
            "mango": "yellow",
            "peach": "darkred",
            "pear": "darkred",
            "plum": "purple",
            "lemon": "orange",
            "blueberry": "pink",
            "raspberry": "green",
            "apricot": "gold",
            "coconut": "red"
        }
        self.front_surf.fill(self.color_map.get(card_type, "gray"))
        
        self.back_surf = pygame.Surface((self.width, self.height))
        self.back_surf.fill("darkblue")
        # TODO: Načítaj textúru zadnej strany
        # self.back_img = pygame.image.load("SW/assets/images/pexeso/card_back.png")
    
    def update(self, dt):
        if self.is_flipped and self.flip_progress < 1.0:
            self.flip_progress += dt * 4 
            if self.flip_progress > 1.0:
                self.flip_progress = 1.0
        
        elif not self.is_flipped and self.flip_progress > 0.0:
            self.flip_progress -= dt * 4
            if self.flip_progress < 0.0:
                self.flip_progress = 0.0
    
    def draw(self, screen, selected=False):
        if self.is_matched:
            return
        
        scale = abs(self.flip_progress - 0.5) * 2  
        current_width = int(self.width * scale)
        
        if self.flip_progress > 0.5:
            surf = self.front_surf
        else:
            surf = self.back_surf
        
        if current_width > 0:
            scaled_surf = pygame.transform.scale(surf, (current_width, self.height))
            x_offset = (self.width - current_width) // 2
            screen.blit(scaled_surf, (self.x + x_offset, self.y))
        
        if selected and not self.is_matched:
            pygame.draw.rect(screen, "yellow", self.rect, 4)
        
        pygame.draw.rect(screen, "white", self.rect, 2)
    
    def flip(self):
        if not self.is_matched:
            self.is_flipped = True
    
    def unflip(self):
        if not self.is_matched:
            self.is_flipped = False


class Pexeso(Game):
    def __init__(self, fullscreen=True, difficulty="easy"):
        super().__init__(
            fullscreen, 
            icon_path="Games/assets/images/pexeso/pexeso_icon.png",  # TODO: Doplň cestu
            title="Memory", 
            game_name="Memory_easy"
        )
        
        self.width = pygame.display.get_window_size()[0]
        self.height = pygame.display.get_window_size()[1]
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        
        self.i = InputHandler()
        
        self.difficulty = difficulty
        if difficulty == "easy":
            self.grid_rows = 4
            self.grid_cols = 4
        else:
            self.grid_rows = 6
            self.grid_cols = 6
        
        self.total_pairs = (self.grid_rows * self.grid_cols) // 2
        
        self.card_types = [
            "apple", "banana", "cherry", "grape",
            "orange", "strawberry", "watermelon", "pineapple"
        ]
        
        if difficulty == "hard":
            self.card_types += [
                "kiwi", "mango", "peach", "pear",
                "plum", "lemon", "blueberry", "raspberry",
                "apricot", "coconut"
            ]
        
        # 0=difficulty select, 1=game menu, 2=playing, 3=win
        self.game_state = 0
        self.moves = 0
        self.matches_found = 0
        self.start_time = 0
        self.elapsed_time = 0
        
        self.selected_difficulty = 0
        
        self.cursor_row = 0
        self.cursor_col = 0
        
        self.flipped_cards = []
        self.checking_match = False
        self.check_timer = 0
        
        self.cards = []
        self.create_cards()
        
        self.font_large = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 60)
        self.font_medium = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 40)
        self.font_small = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 30)
        
        self.bg = pygame.Surface((self.width, self.height))
        self.bg.fill("#1a1a2e")
        
        if self.i.GPIO1 and GPIO_ENABLED and self.i.GPIO:
            self.button = "A"
        else:
            self.button = "SPACE"
    
    def create_cards(self):
        self.cards = []
        
        card_pairs = []
        for i in range(self.total_pairs):
            card_type = self.card_types[i % len(self.card_types)]
            card_pairs.append(card_type)
            card_pairs.append(card_type)
        
        random.shuffle(card_pairs)
        
        card_spacing = 20
        total_grid_width = self.grid_cols * 100 + (self.grid_cols - 1) * card_spacing
        total_grid_height = self.grid_rows * 100 + (self.grid_rows - 1) * card_spacing
        
        start_x = (self.width - total_grid_width) // 2
        start_y = (self.height - total_grid_height) // 2 + 30
        
        card_id = 0
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                x = start_x + col * (100 + card_spacing)
                y = start_y + row * (100 + card_spacing)
                card_type = card_pairs[card_id]
                
                card = Card(x, y, card_type, card_id)
                self.cards.append(card)
                card_id += 1
    
    def get_selected_card(self):
        index = self.cursor_row * self.grid_cols + self.cursor_col
        if 0 <= index < len(self.cards):
            return self.cards[index]
        return None
    
    def skip_matched_cards(self, direction):
        original_row = self.cursor_row
        original_col = self.cursor_col
        max_steps = self.grid_rows * self.grid_cols
        steps = 0
        
        while steps < max_steps:
            card = self.get_selected_card()
            if card and not card.is_matched:
                return
            
            if direction == "UP":
                self.cursor_row = (self.cursor_row - 1) % self.grid_rows
            elif direction == "DOWN":
                self.cursor_row = (self.cursor_row + 1) % self.grid_rows
            elif direction == "LEFT":
                self.cursor_col = (self.cursor_col - 1) % self.grid_cols
            elif direction == "RIGHT":
                self.cursor_col = (self.cursor_col + 1) % self.grid_cols
            
            steps += 1
        
        self.cursor_row = original_row
        self.cursor_col = original_col
    
    def handle_input(self):
        if self.game_state == 0:
            if self.i.just_pressed("UP"):
                self.selected_difficulty = (self.selected_difficulty - 1) % 2
            
            if self.i.just_pressed("DOWN"):
                self.selected_difficulty = (self.selected_difficulty + 1) % 2
            
            if self.i.just_pressed("A"):
                if self.selected_difficulty == 0:
                    self.difficulty = "easy"
                    self.grid_rows = 4
                    self.grid_cols = 4
                else:
                    self.difficulty = "hard"
                    self.grid_rows = 6
                    self.grid_cols = 6
                
                self.total_pairs = (self.grid_rows * self.grid_cols) // 2
                
                if self.difficulty == "hard":
                    self.card_types = [
                        "apple", "banana", "cherry", "grape",
                        "orange", "strawberry", "watermelon", "pineapple",
                        "kiwi", "mango", "peach", "pear",
                        "plum", "lemon", "blueberry", "raspberry",
                        "apricot", "coconut"
                    ]
                else:
                    self.card_types = [
                        "apple", "banana", "cherry", "grape",
                        "orange", "strawberry", "watermelon", "pineapple"
                    ]
                
                self.create_cards()
                self.highscore = self.save_system.get_highscore(f"Memory_{self.difficulty}")
                self.game_state = 1
        
        elif self.game_state == 1:
            if self.i.just_pressed("A"):
                self.game_state = 2
                self.start_time = time.time()
        
        elif self.game_state == 2:
            if not self.checking_match:
                if self.i.just_pressed("UP"):
                    self.cursor_row = (self.cursor_row - 1) % self.grid_rows
                    self.skip_matched_cards("UP")
                
                if self.i.just_pressed("DOWN"):
                    self.cursor_row = (self.cursor_row + 1) % self.grid_rows
                    self.skip_matched_cards("DOWN")
                
                if self.i.just_pressed("LEFT"):
                    self.cursor_col = (self.cursor_col - 1) % self.grid_cols
                    self.skip_matched_cards("LEFT")
                
                if self.i.just_pressed("RIGHT"):
                    self.cursor_col = (self.cursor_col + 1) % self.grid_cols
                    self.skip_matched_cards("RIGHT")
                
                if self.i.just_pressed("A"):
                    self.select_card()
        
        elif self.game_state == 3:
                self.__init__(fullscreen=self.screen.get_flags() & pygame.FULLSCREEN, difficulty=self.difficulty)
    
    def select_card(self):
        card = self.get_selected_card()
        
        if card and not card.is_flipped and not card.is_matched:
            if len(self.flipped_cards) < 2:
                card.flip()
                self.flipped_cards.append(card)
                
                if len(self.flipped_cards) == 2:
                    self.moves += 1
                    self.checking_match = True
                    self.check_timer = time.time()
    
    def update(self):
        if self.game_state == 2:
            self.elapsed_time = time.time() - self.start_time
            
            dt = self.clock.get_time() / 1000.0
            for card in self.cards:
                card.update(dt)
            
            if self.checking_match:
                if time.time() - self.check_timer > 1.0:
                    self.check_match()
                    self.checking_match = False
            
            if self.matches_found == self.total_pairs:
                self.game_state = 3
                self.save_system.update_score(f"Memory_{self.difficulty}", self.calculate_score())
                if self.calculate_score() > self.highscore:
                    self.highscore = self.calculate_score()
    
    def check_match(self):
        if len(self.flipped_cards) == 2:
            card1, card2 = self.flipped_cards
            
            if card1.card_type == card2.card_type:
                card1.is_matched = True
                card2.is_matched = True
                self.matches_found += 1
            else:
                card1.unflip()
                card2.unflip()
            
            self.flipped_cards = []
    
    def calculate_score(self):
        base_score = 10000
        move_penalty = self.moves * 100
        time_penalty = int(self.elapsed_time * 10)
        
        score = max(0, base_score - move_penalty - time_penalty)
        return score
    
    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        
        if self.game_state == 0:
            self.draw_difficulty_select()
        
        elif self.game_state == 1:
            self.draw_menu()
        
        elif self.game_state == 2:
            self.draw_game()
        
        elif self.game_state == 3:
            self.draw_win_screen()
    
    def draw_difficulty_select(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill("black")
        self.screen.blit(overlay, (0, 0))
        
        title = self.font_large.render("SELECT DIFFICULTY", True, "#16db65")
        title_rect = title.get_rect(center=(self.center_x, self.center_y - 150))
        self.screen.blit(title, title_rect)
        
        easy_color = "yellow" if self.selected_difficulty == 0 else "white"
        easy_text = self.font_medium.render("EASY (4x4)", True, easy_color)
        easy_rect = easy_text.get_rect(center=(self.center_x, self.center_y - 20))
        self.screen.blit(easy_text, easy_rect)
        
        hard_color = "yellow" if self.selected_difficulty == 1 else "white"
        hard_text = self.font_medium.render("HARD (6x6)", True, hard_color)
        hard_rect = hard_text.get_rect(center=(self.center_x, self.center_y + 40))
        self.screen.blit(hard_text, hard_rect)
        
        arrow = self.font_large.render(">", True, "yellow")
        arrow_y = self.center_y - 20 if self.selected_difficulty == 0 else self.center_y + 40
        arrow_rect = arrow.get_rect(center=(self.center_x - 200, arrow_y))
        self.screen.blit(arrow, arrow_rect)
        
        instruction = self.font_small.render(f"Press '{self.button}' to select", True, "gray")
        instruction_rect = instruction.get_rect(center=(self.center_x, self.center_y + 120))
        self.screen.blit(instruction, instruction_rect)
    
    def draw_menu(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill("black")
        self.screen.blit(overlay, (0, 0))

        title = self.font_large.render("MEMORY", True, "#16db65")
        title_rect = title.get_rect(center=(self.center_x, self.center_y - 100))
        self.screen.blit(title, title_rect)
        
        diff_text = f"Difficulty: {self.difficulty.upper()} ({self.grid_rows}x{self.grid_cols})"
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
        moves_surf = self.font_small.render(f"Moves: {self.moves}", True, "white")
        self.screen.blit(moves_surf, (20, 20))
        
        time_str = f"Time: {int(self.elapsed_time)}s"
        time_surf = self.font_small.render(time_str, True, "white")
        self.screen.blit(time_surf, (self.width - 200, 20))
        
        pairs_surf = self.font_small.render(f"Pairs: {self.matches_found}/{self.total_pairs}", True, "white")
        pairs_rect = pairs_surf.get_rect(center=(self.center_x, 30))
        self.screen.blit(pairs_surf, pairs_rect)
        
        highscore_surf = self.font_small.render(f"Best: {self.highscore}", True, "gold")
        self.screen.blit(highscore_surf, (20, 60))
        
        selected_card = self.get_selected_card()
        for card in self.cards:
            card.draw(self.screen, selected=(card == selected_card))
    
    def draw_win_screen(self):
        for card in self.cards:
            card.draw(self.screen)
        
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill("black")
        self.screen.blit(overlay, (0, 0))
        
        win_text = self.font_large.render("YOU WIN!", True, "#FFD700")
        win_rect = win_text.get_rect(center=(self.center_x, self.center_y - 100))
        self.screen.blit(win_text, win_rect)
        
        final_score = self.calculate_score()
        score_text = f"Score: {final_score}"
        score_surf = self.font_medium.render(score_text, True, "white")
        score_rect = score_surf.get_rect(center=(self.center_x, self.center_y - 20))
        self.screen.blit(score_surf, score_rect)
        
        moves_text = f"Moves: {self.moves}"
        moves_surf = self.font_medium.render(moves_text, True, "white")
        moves_rect = moves_surf.get_rect(center=(self.center_x, self.center_y + 30))
        self.screen.blit(moves_surf, moves_rect)
        
        time_text = f"Time: {int(self.elapsed_time)}s"
        time_surf = self.font_medium.render(time_text, True, "white")
        time_rect = time_surf.get_rect(center=(self.center_x, self.center_y + 80))
        self.screen.blit(time_surf, time_rect)
        
        restart_text = f"Press '{self.button}' to restart"
        restart_surf = self.font_medium.render(restart_text, True, "#16db65")
        restart_rect = restart_surf.get_rect(center=(self.center_x, self.center_y + 150))
        self.screen.blit(restart_surf, restart_rect)
        
        if final_score > self.highscore:
            record_text = "NEW RECORD!"
            record_surf = self.font_medium.render(record_text, True, "red")
            record_rect = record_surf.get_rect(center=(self.center_x, self.center_y - 150))
            self.screen.blit(record_surf, record_rect)


if __name__ == "__main__":
    pexeso = Pexeso(fullscreen=False, difficulty="easy")
    pexeso.run()
