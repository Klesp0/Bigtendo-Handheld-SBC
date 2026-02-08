import pygame
import random
import sys
from _game_base import Game
from _input_handler import InputHandler
from config import *


# Tetromino tvary a farby
SHAPES = {
    'I': {'shape': [[1, 1, 1, 1]], 'color': 'cyan'},
    'O': {'shape': [[1, 1], [1, 1]], 'color': 'yellow'},
    'T': {'shape': [[0, 1, 0], [1, 1, 1]], 'color': 'purple'},
    'S': {'shape': [[0, 1, 1], [1, 1, 0]], 'color': 'green'},
    'Z': {'shape': [[1, 1, 0], [0, 1, 1]], 'color': 'red'},
    'J': {'shape': [[1, 0, 0], [1, 1, 1]], 'color': 'blue'},
    'L': {'shape': [[0, 0, 1], [1, 1, 1]], 'color': 'orange'}
}

# SRS Wall Kick data
WALL_KICKS = {
    0: [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],  # 0->R
    1: [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],      # R->2
    2: [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],     # 2->L
    3: [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]    # L->0
}

# I piece má špeciálne wall kicks
WALL_KICKS_I = {
    0: [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    1: [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    2: [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    3: [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)]
}


class Tetromino:
    def __init__(self, shape_type, x, y):
        self.type = shape_type
        self.shape = SHAPES[shape_type]['shape']
        self.color = SHAPES[shape_type]['color']
        self.x = x
        self.y = y
        self.rotation = 0
    
    def rotate_matrix(self, clockwise=True):
        """Otočí maticu o 90° v smere/proti smeru hodinových ručičiek"""
        if clockwise:
            return [list(row) for row in zip(*self.shape[::-1])]
        else:
            return [list(row) for row in zip(*self.shape)][::-1]
    
    def get_rotated_shape(self):
        """Vráti otočený tvar"""
        temp_shape = self.shape
        for _ in range(self.rotation % 4):
            temp_shape = [list(row) for row in zip(*temp_shape[::-1])]
        return temp_shape


class TetrisGame(Game):
    def __init__(self, fullscreen=True):
        super().__init__(
            fullscreen,
            icon_path="Games/assets/images/tetris/tetris_icon.png",
            title="Tetris",
            game_name="Tetris"
        )
        
        self.width = pygame.display.get_window_size()[0]
        self.height = pygame.display.get_window_size()[1]
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        
        self.i = InputHandler()
        
        # 0=difficulty select, 1=game menu, 2=playing, 3=game over
        self.game_state = 0
        
        self.selected_difficulty = 0
        self.difficulty = "normal"
        
        # Grid nastavenia
        self.grid_width = 10
        self.grid_height = 20
        self.cell_size = 25
        self.grid = [[None for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        
        # Pozícia gridu na obrazovke
        self.grid_x = (self.width - self.grid_width * self.cell_size) // 2
        self.grid_y = 50
        
        # Herné premenné
        self.current_piece = None
        self.next_piece = None
        self.hold_piece = None
        self.can_hold = True
        
        self.fall_time = 0
        self.fall_speed = 1.0  # Sekundy medzi pádom
        self.level = 1
        self.lines_cleared = 0
        
        # Input handling
        self.move_delay = 0.15
        self.move_timer = 0
        self.rotate_cooldown = 0
        
        self.font_large = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 60)
        self.font_medium = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 50)
        self.font_small = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 35)
        
        self.bg = pygame.Surface((self.width, self.height))
        self.bg.fill("#1a1a2e")
        
        if self.i.GPIO1 and GPIO_ENABLED and self.i.GPIO:
            self.button = "A"
        else:
            self.button = "SPACE"
    
    def spawn_piece(self):
        """Vytvor nový tetromino"""
        if self.next_piece is None:
            self.next_piece = random.choice(list(SHAPES.keys()))
        
        self.current_piece = Tetromino(self.next_piece, self.grid_width // 2 - 1, 0)
        self.next_piece = random.choice(list(SHAPES.keys()))
        self.can_hold = True
        
        # Kontrola game over
        if self.check_collision(self.current_piece, 0, 0):
            return False
        return True
    
    def check_collision(self, piece, offset_x, offset_y):
        """Skontroluj kolíziu s gridom alebo okrajmi"""
        shape = piece.get_rotated_shape()
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece.x + x + offset_x
                    new_y = piece.y + y + offset_y
                    
                    # Kontrola okrajov
                    if new_x < 0 or new_x >= self.grid_width or new_y >= self.grid_height:
                        return True
                    
                    # Kontrola kolízie s gridom
                    if new_y >= 0 and self.grid[new_y][new_x] is not None:
                        return True
        
        return False
    
    def rotate_piece(self):
        """Otočí piece s SRS wall kicks"""
        if self.current_piece is None:
            return
        
        old_rotation = self.current_piece.rotation
        self.current_piece.rotation = (self.current_piece.rotation + 1) % 4
        
        # Vyber správne wall kicks (I piece má iné)
        kicks = WALL_KICKS_I if self.current_piece.type == 'I' else WALL_KICKS
        kick_data = kicks[old_rotation]
        
        # Skúsaj všetky wall kick pozície
        for kick_x, kick_y in kick_data:
            if not self.check_collision(self.current_piece, kick_x, -kick_y):
                self.current_piece.x += kick_x
                self.current_piece.y -= kick_y
                return
        
        # Ak žiadny wall kick nefunguje, vráť starú rotáciu
        self.current_piece.rotation = old_rotation
    
    def lock_piece(self):
        """Zamkni piece do gridu"""
        shape = self.current_piece.get_rotated_shape()
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_y = self.current_piece.y + y
                    grid_x = self.current_piece.x + x
                    if 0 <= grid_y < self.grid_height:
                        self.grid[grid_y][grid_x] = self.current_piece.color
        
        self.clear_lines()
    
    def clear_lines(self):
        """Vymaž plné riadky"""
        lines_to_clear = []
        
        for y in range(self.grid_height):
            if all(cell is not None for cell in self.grid[y]):
                lines_to_clear.append(y)
        
        if lines_to_clear:
            # Vymaž riadky
            for y in lines_to_clear:
                del self.grid[y]
                self.grid.insert(0, [None for _ in range(self.grid_width)])
            
            # Počítaj skóre
            num_lines = len(lines_to_clear)
            self.lines_cleared += num_lines
            
            points = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += points.get(num_lines, 0) * self.level
            
            # Level up každých 10 riadkov
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(0.1, 1.0 - (self.level - 1) * 0.05)
    
    def hard_drop(self):
        """Okamžite spusti piece nadol"""
        if self.current_piece is None:
            return
        
        while not self.check_collision(self.current_piece, 0, 1):
            self.current_piece.y += 1
        
        self.lock_piece()
        if not self.spawn_piece():
            self.game_state = 3
            self.save_system.update_score(f"Tetris_{self.difficulty}", self.score)
            if self.score > self.highscore:
                self.highscore = self.score
    
    def hold_current_piece(self):
        """Daj current piece do hold boxu"""
        if not self.can_hold or self.current_piece is None:
            return
        
        if self.hold_piece is None:
            self.hold_piece = self.current_piece.type
            if not self.spawn_piece():
                self.game_state = 3
        else:
            # Swap
            temp = self.hold_piece
            self.hold_piece = self.current_piece.type
            self.current_piece = Tetromino(temp, self.grid_width // 2 - 1, 0)
        
        self.can_hold = False
    
    def get_ghost_y(self):
        """Vypočítaj y pozíciu ghost piece"""
        if self.current_piece is None:
            return 0
        
        ghost_y = self.current_piece.y
        while not self.check_collision(self.current_piece, 0, ghost_y - self.current_piece.y + 1):
            ghost_y += 1
        
        return ghost_y
    
    def reset_game(self):
        """Reset hry"""
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.grid = [[None for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.current_piece = None
        self.next_piece = None
        self.hold_piece = None
        self.can_hold = True
        self.fall_time = 0
        
        # Nastavenie rýchlosti podľa obtiažnosti
        speeds = {
            "easy": 1.2,
            "normal": 1.0,
            "hard": 0.7,
            "insane": 0.4
        }
        self.fall_speed = speeds.get(self.difficulty, 1.0)
        
        self.spawn_piece()
    
    def handle_input(self):
        if self.game_state == 0:
            if self.i.just_pressed("UP"):
                self.selected_difficulty = (self.selected_difficulty - 1) % 4
            
            if self.i.just_pressed("DOWN"):
                self.selected_difficulty = (self.selected_difficulty + 1) % 4
            
            if self.i.just_pressed("A"):
                difficulties = ["easy", "normal", "hard", "insane"]
                self.difficulty = difficulties[self.selected_difficulty]
                self.highscore = self.save_system.get_highscore(f"Tetris_{self.difficulty}")
                self.game_state = 1
        
        elif self.game_state == 1:
            # BACK - návrat na difficulty select
            if self.i.just_pressed("B"):
                self.game_state = 0
            
            if self.i.just_pressed("A"):
                self.reset_game()
                self.game_state = 2
        
        elif self.game_state == 2:
            dt = self.clock.get_time() / 1000.0
            
            # Rotácia
            if self.i.just_pressed("UP"):
                if self.rotate_cooldown <= 0:
                    self.rotate_piece()
                    self.rotate_cooldown = 0.15
            
            # Hard drop
            if self.i.just_pressed("A"):
                self.hard_drop()
            
            # Hold piece
            if self.i.just_pressed("X"):
                self.hold_current_piece()
            
            # Pohyb vľavo/vpravo
            if self.i.is_pressed("LEFT"):
                if self.move_timer <= 0:
                    if not self.check_collision(self.current_piece, -1, 0):
                        self.current_piece.x -= 1
                    self.move_timer = self.move_delay
            
            if self.i.is_pressed("RIGHT"):
                if self.move_timer <= 0:
                    if not self.check_collision(self.current_piece, 1, 0):
                        self.current_piece.x += 1
                    self.move_timer = self.move_delay
            
            # Soft drop (rýchlejší pád)
            if self.i.is_pressed("DOWN"):
                if not self.check_collision(self.current_piece, 0, 1):
                    self.current_piece.y += 1
                    self.score += 1
        
        elif self.game_state == 3:
            if self.i.just_pressed("A"):
                self.__init__(fullscreen=self.screen.get_flags() & pygame.FULLSCREEN)
    
    def update(self):
        if self.game_state == 2:
            dt = self.clock.get_time() / 1000.0
            dt = max(0.001, min(0.1, dt))
            
            self.move_timer -= dt
            self.rotate_cooldown -= dt
            
            # Automatický pád
            self.fall_time += dt
            if self.fall_time >= self.fall_speed:
                self.fall_time = 0
                
                if self.current_piece is None:
                    if not self.spawn_piece():
                        self.game_state = 3
                        self.save_system.update_score(f"Tetris_{self.difficulty}", self.score)
                        if self.score > self.highscore:
                            self.highscore = self.score
                else:
                    if not self.check_collision(self.current_piece, 0, 1):
                        self.current_piece.y += 1
                    else:
                        self.lock_piece()
                        if not self.spawn_piece():
                            self.game_state = 3
                            self.save_system.update_score(f"Tetris_{self.difficulty}", self.score)
                            if self.score > self.highscore:
                                self.highscore = self.score
    
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
            ("EASY (Slow Fall)", 0),
            ("NORMAL (Classic)", 1),
            ("HARD (Fast Fall)", 2),
            ("INSANE (Very Fast)", 3)
        ]
        
        for diff_name, diff_index in difficulties:
            color = "yellow" if self.selected_difficulty == diff_index else "white"
            y_pos = self.center_y - 80 + (diff_index * 50)
            
            diff_text = self.font_medium.render(diff_name, True, color)
            diff_rect = diff_text.get_rect(center=(self.center_x, y_pos))
            self.screen.blit(diff_text, diff_rect)
        
        arrow = self.font_large.render(">", True, "yellow")
        arrow_y = self.center_y - 80 + (self.selected_difficulty * 50)
        arrow_rect = arrow.get_rect(center=(self.center_x - 280, arrow_y))
        self.screen.blit(arrow, arrow_rect)
        
        instruction = self.font_small.render(f"Press '{self.button}' to select", True, "gray")
        instruction_rect = instruction.get_rect(center=(self.center_x, self.center_y + 150))
        self.screen.blit(instruction, instruction_rect)
    
    def draw_game_menu(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill("black")
        self.screen.blit(overlay, (0, 0))
        
        title = self.font_large.render("TETRIS", True, "white")
        title_rect = title.get_rect(center=(self.center_x, self.center_y - 100))
        self.screen.blit(title, title_rect)
        
        diff_text = f"Difficulty: {self.difficulty.upper()}"
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
        
        # Nápis pre návrat späť
        back_text = "Press 'B' to go back"
        back_surf = self.font_small.render(back_text, True, "gray")
        back_rect = back_surf.get_rect(center=(self.center_x, self.center_y + 180))
        self.screen.blit(back_surf, back_rect)
    
    def draw_block(self, x, y, color, alpha=255):
        """Vykreslí jeden blok"""
        rect = pygame.Rect(
            self.grid_x + x * self.cell_size,
            self.grid_y + y * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        
        surf = pygame.Surface((self.cell_size, self.cell_size))
        surf.set_alpha(alpha)
        surf.fill(color)
        self.screen.blit(surf, rect)
        
        # Obrys
        pygame.draw.rect(self.screen, "black", rect, 1)
    
    def draw_game(self):
        # Grid pozadie
        grid_bg = pygame.Rect(
            self.grid_x - 5,
            self.grid_y - 5,
            self.grid_width * self.cell_size + 10,
            self.grid_height * self.cell_size + 10
        )
        pygame.draw.rect(self.screen, "darkgray", grid_bg, 3)
        
        # Grid
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.grid[y][x] is not None:
                    self.draw_block(x, y, self.grid[y][x])
        
        # Ghost piece
        if self.current_piece:
            ghost_y = self.get_ghost_y()
            shape = self.current_piece.get_rotated_shape()
            for y, row in enumerate(shape):
                for x, cell in enumerate(row):
                    if cell:
                        self.draw_block(
                            self.current_piece.x + x,
                            ghost_y + y,
                            self.current_piece.color,
                            alpha=50
                        )
        
        # Current piece
        if self.current_piece:
            shape = self.current_piece.get_rotated_shape()
            for y, row in enumerate(shape):
                for x, cell in enumerate(row):
                    if cell:
                        self.draw_block(
                            self.current_piece.x + x,
                            self.current_piece.y + y,
                            self.current_piece.color
                        )
        
        # UI - Left panel
        score_surf = self.font_small.render(f"Score: {self.score}", True, "white")
        self.screen.blit(score_surf, (20, 50))
        
        level_surf = self.font_small.render(f"Level: {self.level}", True, "cyan")
        self.screen.blit(level_surf, (20, 90))
        
        lines_surf = self.font_small.render(f"Lines: {self.lines_cleared}", True, "yellow")
        self.screen.blit(lines_surf, (20, 130))
        
        best_surf = self.font_small.render(f"Best: {self.highscore}", True, "gold")
        self.screen.blit(best_surf, (20, 170))
        
        # UI - Right panel (Next & Hold)
        next_text = self.font_small.render("NEXT:", True, "white")
        self.screen.blit(next_text, (self.grid_x + self.grid_width * self.cell_size + 30, 50))
        
        # Vykreslenie next piece (zjednodušené)
        if self.next_piece:
            next_color = SHAPES[self.next_piece]['color']
            next_rect = pygame.Rect(
                self.grid_x + self.grid_width * self.cell_size + 30,
                90,
                80,
                40
            )
            pygame.draw.rect(self.screen, next_color, next_rect)
            pygame.draw.rect(self.screen, "white", next_rect, 2)
        
        hold_text = self.font_small.render("HOLD (X):", True, "white")
        self.screen.blit(hold_text, (self.grid_x + self.grid_width * self.cell_size + 30, 200))
        
        # Vykreslenie hold piece
        if self.hold_piece:
            hold_color = SHAPES[self.hold_piece]['color']
            hold_rect = pygame.Rect(
                self.grid_x + self.grid_width * self.cell_size + 30,
                240,
                80,
                40
            )
            pygame.draw.rect(self.screen, hold_color, hold_rect)
            pygame.draw.rect(self.screen, "white", hold_rect, 2)
    
    def draw_game_over(self):
        self.draw_game()
        
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
        
        lines_text = f"Lines Cleared: {self.lines_cleared}"
        lines_surf = self.font_medium.render(lines_text, True, "white")
        lines_rect = lines_surf.get_rect(center=(self.center_x, self.center_y + 30))
        self.screen.blit(lines_surf, lines_rect)
        
        level_text = f"Level Reached: {self.level}"
        level_surf = self.font_medium.render(level_text, True, "white")
        level_rect = level_surf.get_rect(center=(self.center_x, self.center_y + 80))
        self.screen.blit(level_surf, level_rect)
        
        restart_text = f"Press '{self.button}' to restart"
        restart_surf = self.font_medium.render(restart_text, True, "#16db65")
        restart_rect = restart_surf.get_rect(center=(self.center_x, self.center_y + 150))
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
                    self.save_system.update_time(f"Tetris")
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        self.save_system.update_time(f"Tetris")
                        
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
    game = TetrisGame(fullscreen=False)
    game.run()