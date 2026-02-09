import pygame
import random
import sys
from _game_base import Game
from _input_handler import InputHandler
from config import *


class Player:
    def __init__(self, x, y):
        self.speed = 300
        self.shoot_cooldown = 0
        self.shoot_delay = 0.5
        
        # TODO: Načítaj obrázok
        # self.surf = pygame.image.load("Games/assets/images/space_invaders/player_ship.png")
        # self.surf = pygame.transform.scale(self.surf, (60, 40))
        
        self.surf = pygame.Surface((60, 40))
        self.surf.fill("cyan")
        
        self.rect = self.surf.get_rect(midbottom=(x, y))
    
    def move(self, dx, dt, screen_width):
        self.rect.x += dx * self.speed * dt
        
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
    
    def can_shoot(self, dt):
        self.shoot_cooldown -= dt
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = self.shoot_delay
            return True
        return False
    
    def draw(self, screen):
        screen.blit(self.surf, self.rect)


class Bullet:
    def __init__(self, x, y, speed, is_player):
        self.speed = speed
        self.is_player = is_player
        
        # TODO: Načítaj obrázok
        # self.surf = pygame.image.load(f"Games/assets/images/space_invaders/bullet_{'player' if is_player else 'alien'}.png")
        
        self.surf = pygame.Surface((8, 20))
        self.surf.fill("yellow" if is_player else "red")
        
        self.rect = self.surf.get_rect(center=(x, y))
    
    def update(self, dt):
        self.rect.y += self.speed * dt
    
    def is_off_screen(self, screen_height):
        return self.rect.bottom < 0 or self.rect.top > screen_height
    
    def draw(self, screen):
        screen.blit(self.surf, self.rect)


class Alien:
    def __init__(self, x, y, alien_type):
        self.alien_type = alien_type
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.5
        
        # TODO: Načítaj animované obrázky
        # self.frames = [
        #     pygame.image.load(f"Games/assets/images/space_invaders/alien_{alien_type}_1.png"),
        #     pygame.image.load(f"Games/assets/images/space_invaders/alien_{alien_type}_2.png")
        # ]
        
        colors = {1: "red", 2: "green", 3: "purple"}
        self.surf = pygame.Surface((40, 40))
        self.surf.fill(colors.get(alien_type, "white"))
        
        self.rect = self.surf.get_rect(topleft=(x, y))
        
        # Bodové hodnoty
        self.points = {1: 30, 2: 20, 3: 10}[alien_type]
    
    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 2
    
    def draw(self, screen):
        screen.blit(self.surf, self.rect)


class AlienGrid:
    def __init__(self, start_x, start_y):
        self.aliens = []
        self.direction = 1
        self.speed = 50
        self.move_down_amount = 20
        self.shoot_timer = 0
        self.shoot_delay = 1.5
        
        # Vytvor 5 radov, 11 stĺpcov
        for row in range(5):
            alien_type = 1 if row < 1 else (2 if row < 3 else 3)
            for col in range(11):
                x = start_x + col * 50
                y = start_y + row * 45
                alien = Alien(x, y, alien_type)
                self.aliens.append(alien)
    
    def update(self, dt, screen_width):
        if not self.aliens:
            return
        
        # Rýchlosť sa zvyšuje s počtom mŕtvych aliens
        speed_multiplier = 1 + (55 - len(self.aliens)) * 0.05
        
        # Animácia aliens
        for alien in self.aliens:
            alien.update_animation(dt)
        
        # Pohyb celej mriežky
        move_amount = self.direction * self.speed * speed_multiplier * dt
        
        for alien in self.aliens:
            alien.rect.x += move_amount
        
        # Kontrola okrajov
        hit_edge = False
        for alien in self.aliens:
            if alien.rect.left <= 0 or alien.rect.right >= screen_width:
                hit_edge = True
                break
        
        if hit_edge:
            self.direction *= -1
            for alien in self.aliens:
                alien.rect.y += self.move_down_amount
    
    def get_random_shooter(self):
        if not self.aliens:
            return None
        
        # Vyber náhodného aliena z najnižších v každom stĺpci
        columns = {}
        for alien in self.aliens:
            col = alien.rect.centerx // 50
            if col not in columns or alien.rect.y > columns[col].rect.y:
                columns[col] = alien
        
        shooters = list(columns.values())
        return random.choice(shooters) if shooters else None
    
    def lowest_alien_y(self):
        if not self.aliens:
            return 0
        return max(alien.rect.bottom for alien in self.aliens)
    
    def draw(self, screen):
        for alien in self.aliens:
            alien.draw(screen)


class Shield:
    def __init__(self, x, y):
        self.health = 4
        
        # TODO: Načítaj obrázky pre rôzne stavy poškodenia
        # self.images = [
        #     pygame.image.load(f"Games/assets/images/space_invaders/shield_{i}.png")
        #     for i in range(5)
        # ]
        
        self.surf = pygame.Surface((80, 60))
        self.surf.fill("green")
        
        self.rect = self.surf.get_rect(topleft=(x, y))
    
    def take_damage(self):
        self.health -= 1
        return self.health <= 0
    
    def draw(self, screen):
        if self.health > 0:
            # Farba podľa zdravia
            colors = ["darkgreen", "green", "yellow", "orange", "red"]
            self.surf.fill(colors[4 - self.health])
            screen.blit(self.surf, self.rect)


class UFO:
    def __init__(self, screen_width):
        self.speed = 150
        self.active = False
        self.spawn_timer = random.uniform(15, 25)
        
        # TODO: Načítaj obrázok
        # self.surf = pygame.image.load("Games/assets/images/space_invaders/ufo.png")
        
        self.surf = pygame.Surface((60, 30))
        self.surf.fill("magenta")
        
        self.rect = self.surf.get_rect(topleft=(-70, 50))
        self.points = random.choice([50, 100, 150, 200, 300])
    
    def update(self, dt, screen_width):
        if not self.active:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                self.active = True
                self.rect.topleft = (-70, 50)
                self.points = random.choice([50, 100, 150, 200, 300])
        else:
            self.rect.x += self.speed * dt
            if self.rect.left > screen_width:
                self.active = False
                self.spawn_timer = random.uniform(15, 25)
    
    def draw(self, screen):
        if self.active:
            screen.blit(self.surf, self.rect)


class SpaceInvaders(Game):
    def __init__(self, fullscreen=True):
        super().__init__(
            fullscreen,
            icon_path="Games/assets/images/space_invaders/space_invaders_icon.png",
            title="Space Invaders",
            game_name="SpaceInvaders"
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
        self.lives = 3
        self.wave = 1
        
        self.player = Player(self.center_x, self.height - 60)
        self.alien_grid = AlienGrid(100, 80)
        self.bullets = []
        self.shields = []
        self.ufo = UFO(self.width)
        
        self.alien_shoot_timer = 0
        self.alien_shoot_delay = 1.5
        
        self.create_shields()
        
        self.font_large = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 60)
        self.font_medium = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 50)
        self.font_small = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 40)
        
        # TODO: Načítaj pozadie
        # self.bg = pygame.image.load("Games/assets/images/space_invaders/starfield.png")
        # self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        
        self.bg = pygame.Surface((self.width, self.height))
        self.bg.fill("#0a0a1e")
        
        if self.i.GPIO1 and GPIO_ENABLED and self.i.GPIO:
            self.button = "A"
        else:
            self.button = "SPACE"
    
    def create_shields(self):
        self.shields = []
        shield_y = self.height - 150
        spacing = self.width // 5
        
        for i in range(4):
            x = spacing * (i + 1) - 40
            shield = Shield(x, shield_y)
            self.shields.append(shield)
    
    def reset_game(self):
        self.score = 0
        self.wave = 1
        
        # Lives podľa obtiažnosti
        difficulties = {
            "easy": 5,
            "normal": 3,
            "hard": 2,
            "impossible": 1
        }
        self.lives = difficulties.get(self.difficulty, 3)
        
        self.player = Player(self.center_x, self.height - 60)
        self.alien_grid = AlienGrid(100, 80)
        self.bullets = []
        self.ufo = UFO(self.width)
        self.create_shields()
        
        # Nastavenie alien shoot delay podľa obtiažnosti
        delays = {
            "easy": 2.0,
            "normal": 1.5,
            "hard": 1.0,
            "impossible": 0.5
        }
        self.alien_shoot_delay = delays.get(self.difficulty, 1.5)
    
    def next_wave(self):
        self.wave += 1
        self.alien_grid = AlienGrid(100, 80)
        self.bullets = []
        self.player = Player(self.center_x, self.height - 60)
        
        # Štíty sa obnovia každú druhú vlnu
        if self.wave % 2 == 1:
            self.create_shields()
    
    def handle_input(self):
        if self.game_state == 0:
            if self.i.just_pressed("UP"):
                self.selected_difficulty = (self.selected_difficulty - 1) % 4
            
            if self.i.just_pressed("DOWN"):
                self.selected_difficulty = (self.selected_difficulty + 1) % 4
            
            if self.i.just_pressed("A"):
                difficulties = ["easy", "normal", "hard", "impossible"]
                self.difficulty = difficulties[self.selected_difficulty]
                self.highscore = self.save_system.get_highscore(f"SpaceInvaders_{self.difficulty}")
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
            
            if self.i.is_pressed("LEFT"):
                self.player.move(-1, dt, self.width)
            elif self.i.is_pressed("RIGHT"):
                self.player.move(1, dt, self.width)
            
            if self.i.just_pressed("A"):
                if self.player.can_shoot(dt):
                    bullet = Bullet(self.player.rect.centerx, self.player.rect.top, -400, True)
                    self.bullets.append(bullet)
        
        elif self.game_state == 3:
            if self.i.just_pressed("A"):
                self.__init__(fullscreen=self.screen.get_flags() & pygame.FULLSCREEN)
    
    def update(self):
        if self.game_state == 2:
            dt = self.clock.get_time() / 1000.0
            dt = max(0.001, min(0.1, dt))
            
            # Aktualizuj hráča
            self.player.shoot_cooldown = max(0, self.player.shoot_cooldown - dt)
            
            # Aktualizuj alien grid
            self.alien_grid.update(dt, self.width)
            
            # Aktualizuj UFO
            self.ufo.update(dt, self.width)
            
            # Aktualizuj bullets
            bullets_to_remove = []
            for bullet in self.bullets:
                bullet.update(dt)
                
                if bullet.is_off_screen(self.height):
                    bullets_to_remove.append(bullet)
                    continue
                
                # Kolízia s aliens
                if bullet.is_player:
                    for alien in self.alien_grid.aliens[:]:
                        if bullet.rect.colliderect(alien.rect):
                            self.score += alien.points
                            self.alien_grid.aliens.remove(alien)
                            bullets_to_remove.append(bullet)
                            break
                    
                    # Kolízia s UFO
                    if self.ufo.active and bullet.rect.colliderect(self.ufo.rect):
                        self.score += self.ufo.points
                        self.ufo.active = False
                        self.ufo.spawn_timer = random.uniform(15, 25)
                        bullets_to_remove.append(bullet)
                
                # Kolízia so štítmi
                for shield in self.shields[:]:
                    if bullet.rect.colliderect(shield.rect) and shield.health > 0:
                        if shield.take_damage():
                            self.shields.remove(shield)
                        bullets_to_remove.append(bullet)
                        break
                
                # Kolízia s hráčom (alien bullets)
                if not bullet.is_player and bullet.rect.colliderect(self.player.rect):
                    self.lives -= 1
                    bullets_to_remove.append(bullet)
                    
                    if self.lives <= 0:
                        self.game_state = 3
                        self.save_system.update_score(f"SpaceInvaders_{self.difficulty}", self.score)
                        if self.score > self.highscore:
                            self.highscore = self.score
            
            for bullet in bullets_to_remove:
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
            
            # Alien shooting
            self.alien_shoot_timer += dt
            if self.alien_shoot_timer >= self.alien_shoot_delay:
                self.alien_shoot_timer = 0
                shooter = self.alien_grid.get_random_shooter()
                if shooter:
                    bullet = Bullet(shooter.rect.centerx, shooter.rect.bottom, 300, False)
                    self.bullets.append(bullet)
            
            # Kontrola výhry (všetci aliens mŕtvi)
            if not self.alien_grid.aliens:
                self.next_wave()
            
            # Kontrola prehry (aliens dosiahli dno)
            if self.alien_grid.lowest_alien_y() >= self.player.rect.top:
                self.lives = 0
                self.game_state = 3
                self.save_system.update_score(f"SpaceInvaders_{self.difficulty}", self.score)
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
            ("EASY (5 Lives)", 0),
            ("NORMAL (3 Lives)", 1),
            ("HARD (2 Lives)", 2),
            ("IMPOSSIBLE (1 Life)", 3)
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
        
        title = self.font_large.render("SPACE INVADERS", True, "white")
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
    
    def draw_game(self):
        self.player.draw(self.screen)
        self.alien_grid.draw(self.screen)
        self.ufo.draw(self.screen)
        
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        for shield in self.shields:
            shield.draw(self.screen)
        
        # HUD
        score_surf = self.font_medium.render(f"Score: {self.score}", True, "white")
        self.screen.blit(score_surf, (20, 20))
        
        lives_surf = self.font_small.render(f"Lives: {self.lives}", True, "red")
        self.screen.blit(lives_surf, (20, 70))
        
        wave_surf = self.font_small.render(f"Wave: {self.wave}", True, "cyan")
        self.screen.blit(wave_surf, (self.width - 200, 20))
        
        highscore_surf = self.font_small.render(f"Best: {self.highscore}", True, "gold")
        self.screen.blit(highscore_surf, (self.width - 200, 70))
    
    def draw_game_over(self):
        self.player.draw(self.screen)
        self.alien_grid.draw(self.screen)
        
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        for shield in self.shields:
            shield.draw(self.screen)
        
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
        
        wave_text = f"Waves Survived: {self.wave}"
        wave_surf = self.font_medium.render(wave_text, True, "white")
        wave_rect = wave_surf.get_rect(center=(self.center_x, self.center_y + 30))
        self.screen.blit(wave_surf, wave_rect)
        
        restart_text = f"Press '{self.button}' to restart"
        restart_surf = self.font_medium.render(restart_text, True, "#16db65")
        restart_rect = restart_surf.get_rect(center=(self.center_x, self.center_y + 120))
        self.screen.blit(restart_surf, restart_rect)
        
        if self.score > self.highscore:
            record_text = "NEW RECORD!"
            record_surf = self.font_medium.render(record_text, True, "gold")
            record_rect = record_surf.get_rect(center=(self.center_x, self.center_y - 160))
            self.screen.blit(record_surf, record_rect)

if __name__ == "__main__":
    game = SpaceInvaders(fullscreen=False)
    game.run()