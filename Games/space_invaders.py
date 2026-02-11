import pygame, sys
from random import choice, randint
from _game_base import Game
from _input_handler import InputHandler
from _save_system import SaveSystem
from config import *


class Alien(pygame.sprite.Sprite):
	def __init__(self,color,x,y):
		super().__init__()
		file_path = 'Games/assets/images/space_invaders/' + color + '.png'
		self.image = pygame.image.load(file_path).convert_alpha()
		self.rect = self.image.get_rect(topleft = (x,y))

		if color == 'red': self.value = 100
		elif color == 'green': self.value = 200
		else: self.value = 300

	def update(self,direction):
		self.rect.x += direction


class Extra(pygame.sprite.Sprite):
	def __init__(self,side,screen_width):
		super().__init__()
		self.image = pygame.image.load('Games/assets/images/space_invaders/extra.png').convert_alpha()
		
		if side == 'right':
			x = screen_width + 50
			self.speed = - 3
		else:
			x = -50
			self.speed = 3

		self.rect = self.image.get_rect(topleft = (x,80))

	def update(self):
		self.rect.x += self.speed


class Laser(pygame.sprite.Sprite):
	def __init__(self,pos,speed,screen_height):
		super().__init__()
		self.image = pygame.Surface((4,20))
		self.image.fill('white')
		self.rect = self.image.get_rect(center = pos)
		self.speed = speed
		self.height_y_constraint = screen_height

	def destroy(self):
		if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
			self.kill()

	def update(self):
		self.rect.y += self.speed
		self.destroy()


class Block(pygame.sprite.Sprite):
	def __init__(self,size,color,x,y):
		super().__init__()
		self.image = pygame.Surface((size,size))
		self.image.fill(color)
		self.rect = self.image.get_rect(topleft = (x,y))


shape = [
'  xxxxxxx',
' xxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxx     xxx',
'xx       xx']


class Player(pygame.sprite.Sprite):
	def __init__(self, pos, constraint, speed, input_handler):
		super().__init__()
		self.image = pygame.image.load('Games/assets/images/space_invaders/player.png').convert_alpha()
		self.rect = self.image.get_rect(midbottom = pos)
		self.speed = speed
		self.max_x_constraint = constraint
		self.ready = True
		self.laser_time = 0
		self.laser_cooldown = 600
		self.input_handler = input_handler

		self.lasers = pygame.sprite.Group()

		self.laser_sound = pygame.mixer.Sound('Games/assets/sounds/laser.wav')
		self.laser_sound.set_volume(0.5)

	def get_input(self):
		if self.input_handler.is_pressed("RIGHT"):
			self.rect.x += self.speed
		elif self.input_handler.is_pressed("LEFT"):
			self.rect.x -= self.speed

		if self.input_handler.just_pressed("A") and self.ready:
			self.shoot_laser()
			self.ready = False
			self.laser_time = pygame.time.get_ticks()
			self.laser_sound.play()

	def recharge(self):
		if not self.ready:
			current_time = pygame.time.get_ticks()
			if current_time - self.laser_time >= self.laser_cooldown:
				self.ready = True

	def constraint(self):
		if self.rect.left <= 0:
			self.rect.left = 0
		if self.rect.right >= self.max_x_constraint:
			self.rect.right = self.max_x_constraint

	def shoot_laser(self):
		self.lasers.add(Laser(self.rect.center,-8,self.rect.bottom))

	def update(self):
		self.get_input()
		self.constraint()
		self.recharge()
		self.lasers.update()


class SpaceInvaders(Game):
	def __init__(self, fullscreen=False, difficulty="normal"):
		super().__init__(
			fullscreen=fullscreen,
			title="Space Invaders",
			icon_path='Games/assets/images/space_invaders/space_invaders_icon.png',
			game_name="SpaceInvaders"
		)
		
		self.width = WIDTH
		self.height = HEIGHT
		self.center_x = self.width / 2
		self.center_y = self.height / 2
		
		self.i = InputHandler()
		
		# Game states: 0=difficulty, 1=menu, 2=playing, 3=game_over, 4=victory
		self.game_state = 0
		
		# Alien laser timer - musí byť definovaný PRED setup_difficulty()
		self.ALIENLASER = pygame.USEREVENT + 1
		
		# Difficulty
		self.difficulty = difficulty
		self.selected_difficulty = 1  # 0=easy, 1=normal, 2=hard
		self.setup_difficulty()
		
		# Fonty
		self.font_small = pygame.font.Font('Games/assets/fonts/Pixeltype.ttf', 20)
		self.font_medium = pygame.font.Font('Games/assets/fonts/Pixeltype.ttf', 30)
		self.font_large = pygame.font.Font('Games/assets/fonts/Pixeltype.ttf', 60)
		
		# Audio
		self.music = pygame.mixer.Sound('Games/assets/sounds/music.wav')
		self.music.set_volume(0.2)
		self.laser_sound = pygame.mixer.Sound('Games/assets/sounds/laser.wav')
		self.laser_sound.set_volume(0.5)
		self.explosion_sound = pygame.mixer.Sound('Games/assets/sounds/explosion.wav')
		self.explosion_sound.set_volume(0.3)
		
		# CRT effect
		self.crt = CRT(self.width, self.height)
		
		# Background
		self.bg = pygame.Surface((self.width, self.height))
		self.bg.fill((30,30,30))
		
		# Button text
		if self.i.GPIO1 and GPIO_ENABLED and self.i.GPIO:
			self.button = "A"
		else:
			self.button = "SPACE"
		
		# Inicializácia hry
		self.init_game()

	def setup_difficulty(self):
		"""Nastaví parametre podľa obtiažnosti"""
		if self.difficulty == "easy":
			self.alien_speed = 2
			self.starting_lives = 5
			self.alien_shoot_interval = 1200
		elif self.difficulty == "normal":
			self.alien_speed = 3
			self.starting_lives = 3
			self.alien_shoot_interval = 800
		else:  # hard
			self.alien_speed = 5
			self.starting_lives = 2
			self.alien_shoot_interval = 600
		
		# Update timer
		pygame.time.set_timer(self.ALIENLASER, self.alien_shoot_interval)

	def init_game(self):
		"""Inicializuje/resetuje herné objekty"""
		player_sprite = Player((self.center_x, self.height), self.width, 5, self.i)
		self.player = pygame.sprite.GroupSingle(player_sprite)

		self.lives = self.starting_lives
		self.live_surf = pygame.image.load('Games/assets/images/space_invaders/player.png').convert_alpha()
		self.live_x_start_pos = self.width - (self.live_surf.get_size()[0] * 2 + 20)
		
		self.score = 0
		self._score_saved = False

		# Obstacles
		self.shape = shape
		self.block_size = 6
		self.blocks = pygame.sprite.Group()
		self.obstacle_amount = 4
		self.obstacle_x_positions = [num * (self.width / self.obstacle_amount) for num in range(self.obstacle_amount)]
		self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = self.width / 15, y_start = 480)

		# Aliens
		self.aliens = pygame.sprite.Group()
		self.alien_lasers = pygame.sprite.Group()
		self.alien_setup(rows = 6, cols = 8)
		self.alien_direction = self.alien_speed

		# Extra
		self.extra = pygame.sprite.GroupSingle()
		self.extra_spawn_time = randint(40,80)

	def create_obstacle(self, x_start, y_start, offset_x):
		for row_index, row in enumerate(self.shape):
			for col_index, col in enumerate(row):
				if col == 'x':
					x = x_start + col_index * self.block_size + offset_x
					y = y_start + row_index * self.block_size
					block = Block(self.block_size,(241,79,80),x,y)
					self.blocks.add(block)

	def create_multiple_obstacles(self, *offset, x_start, y_start):
		for offset_x in offset:
			self.create_obstacle(x_start, y_start, offset_x)

	def alien_setup(self, rows, cols, x_distance = 60, y_distance = 48, x_offset = 70, y_offset = 100):
		for row_index, row in enumerate(range(rows)):
			for col_index, col in enumerate(range(cols)):
				x = col_index * x_distance + x_offset
				y = row_index * y_distance + y_offset
				
				if row_index == 0: alien_sprite = Alien('yellow',x,y)
				elif 1 <= row_index <= 2: alien_sprite = Alien('green',x,y)
				else: alien_sprite = Alien('red',x,y)
				self.aliens.add(alien_sprite)

	def alien_position_checker(self):
		all_aliens = self.aliens.sprites()
		for alien in all_aliens:
			if alien.rect.right >= self.width:
				self.alien_direction = -self.alien_speed
				self.alien_move_down(4)
			elif alien.rect.left <= 0:
				self.alien_direction = self.alien_speed
				self.alien_move_down(4)

	def alien_move_down(self, distance):
		if self.aliens:
			for alien in self.aliens.sprites():
				alien.rect.y += distance

	def alien_shoot(self):
		if self.aliens.sprites():
			random_alien = choice(self.aliens.sprites())
			laser_sprite = Laser(random_alien.rect.center, 6, self.height)
			self.alien_lasers.add(laser_sprite)
			self.laser_sound.play()

	def extra_alien_timer(self):
		self.extra_spawn_time -= 1
		if self.extra_spawn_time <= 0:
			self.extra.add(Extra(choice(['right','left']), self.width))
			self.extra_spawn_time = randint(400,800)

	def collision_checks(self):
		# Player lasers 
		if self.player.sprite.lasers:
			for laser in self.player.sprite.lasers:
				if pygame.sprite.spritecollide(laser, self.blocks, True):
					laser.kill()

				aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
				if aliens_hit:
					for alien in aliens_hit:
						self.score += alien.value
					laser.kill()
					self.explosion_sound.play()

				if pygame.sprite.spritecollide(laser, self.extra, True):
					self.score += 500
					laser.kill()

		# Alien lasers 
		if self.alien_lasers:
			for laser in self.alien_lasers:
				if pygame.sprite.spritecollide(laser, self.blocks, True):
					laser.kill()

				if pygame.sprite.spritecollide(laser, self.player, False):
					laser.kill()
					self.lives -= 1
					if self.lives <= 0:
						self.game_state = 3
						self.music.stop()

		# Aliens
		if self.aliens:
			for alien in self.aliens:
				pygame.sprite.spritecollide(alien, self.blocks, True)

				if pygame.sprite.spritecollide(alien, self.player, False):
					self.game_state = 3
					self.music.stop()

	def handle_input(self):
		"""Spracovanie vstupov podľa game state"""
		# Event handling pre alien laser
		for event in pygame.event.get():
			if event.type == self.ALIENLASER and self.game_state == 2:
				self.alien_shoot()
		
		if self.game_state == 0:  # Difficulty select
			if self.i.just_pressed("UP"):
				self.selected_difficulty = (self.selected_difficulty - 1) % 3
			
			if self.i.just_pressed("DOWN"):
				self.selected_difficulty = (self.selected_difficulty + 1) % 3
			
			if self.i.just_pressed("A"):
				if self.selected_difficulty == 0:
					self.difficulty = "easy"
				elif self.selected_difficulty == 1:
					self.difficulty = "normal"
				else:
					self.difficulty = "hard"
				
				self.setup_difficulty()
				self.init_game()
				self.highscore = self.save_system.get_highscore(f"SpaceInvaders_{self.difficulty}")
				self.game_state = 1
		
		elif self.game_state == 1:  # Menu
			if self.i.just_pressed("B"):
				self.game_state = 0
			
			if self.i.just_pressed("A"):
				self.game_state = 2
				self.music.play(loops = -1)
		
		elif self.game_state == 2:  # Playing
			pass  # Player input je spracovaný v Player.update()
		
		elif self.game_state == 3 or self.game_state == 4:  # Game Over / Victory
			if self.i.just_pressed("A"):
				self.game_state = 0
				self._score_saved = False

	def update(self):
		"""Aktualizácia hernej logiky"""
		if self.game_state == 2:
			self.player.update()
			self.alien_lasers.update()
			self.extra.update()
			
			self.aliens.update(self.alien_direction)
			self.alien_position_checker()
			self.extra_alien_timer()
			self.collision_checks()
			
			# Victory check
			if not self.aliens.sprites():
				self.game_state = 4
				self.music.stop()
				self.save_system.update_score(f"SpaceInvaders_{self.difficulty}", self.score)

	def draw(self):
		"""Vykreslenie podľa game state"""
		if self.game_state == 0:
			self.draw_difficulty_select()
		
		elif self.game_state == 1:
			self.draw_menu()
		
		elif self.game_state == 2:
			self.draw_game()
		
		elif self.game_state == 3:
			self.draw_game_over()
		
		elif self.game_state == 4:
			self.draw_victory()
	
	def draw_difficulty_select(self):
		"""Výber obtiažnosti"""
		self.screen.blit(self.bg, (0, 0))
		
		overlay = pygame.Surface((self.width, self.height))
		overlay.set_alpha(200)
		overlay.fill("black")
		self.screen.blit(overlay, (0, 0))
		
		title = self.font_large.render("SELECT DIFFICULTY", True, "white")
		title_rect = title.get_rect(center=(self.center_x, 150))
		self.screen.blit(title, title_rect)
		
		# Easy
		easy_color = "yellow" if self.selected_difficulty == 0 else "white"
		easy_text = self.font_medium.render("EASY", True, easy_color)
		easy_rect = easy_text.get_rect(center=(self.center_x, 280))
		self.screen.blit(easy_text, easy_rect)
		
		easy_desc = self.font_small.render("5 Lives | Slow Aliens", True, easy_color)
		easy_desc_rect = easy_desc.get_rect(center=(self.center_x, 310))
		self.screen.blit(easy_desc, easy_desc_rect)
		
		# Normal
		normal_color = "yellow" if self.selected_difficulty == 1 else "white"
		normal_text = self.font_medium.render("NORMAL", True, normal_color)
		normal_rect = normal_text.get_rect(center=(self.center_x, 360))
		self.screen.blit(normal_text, normal_rect)
		
		normal_desc = self.font_small.render("3 Lives | Medium Aliens", True, normal_color)
		normal_desc_rect = normal_desc.get_rect(center=(self.center_x, 390))
		self.screen.blit(normal_desc, normal_desc_rect)
		
		# Hard
		hard_color = "yellow" if self.selected_difficulty == 2 else "white"
		hard_text = self.font_medium.render("HARD", True, hard_color)
		hard_rect = hard_text.get_rect(center=(self.center_x, 440))
		self.screen.blit(hard_text, hard_rect)
		
		hard_desc = self.font_small.render("2 Lives | Fast Aliens", True, hard_color)
		hard_desc_rect = hard_desc.get_rect(center=(self.center_x, 470))
		self.screen.blit(hard_desc, hard_desc_rect)
		
		# Arrow
		arrow = self.font_large.render(">", True, "yellow")
		arrow_y = 280 if self.selected_difficulty == 0 else (360 if self.selected_difficulty == 1 else 440)
		arrow_rect = arrow.get_rect(center=(self.center_x - 150, arrow_y))
		self.screen.blit(arrow, arrow_rect)
		
		instruction = self.font_small.render(f"Press '{self.button}' to select", True, "gray")
		instruction_rect = instruction.get_rect(center=(self.center_x, 540))
		self.screen.blit(instruction, instruction_rect)
		
		self.crt.draw(self.screen)
	
	def draw_menu(self):
		"""Hlavné menu"""
		self.screen.blit(self.bg, (0, 0))
		
		overlay = pygame.Surface((self.width, self.height))
		overlay.set_alpha(200)
		overlay.fill("black")
		self.screen.blit(overlay, (0, 0))

		title = self.font_large.render("SPACE INVADERS", True, "white")
		title_rect = title.get_rect(center=(self.center_x, 150))
		self.screen.blit(title, title_rect)
		
		diff_text = f"Difficulty: {self.difficulty.upper()}"
		diff_surf = self.font_medium.render(diff_text, True, "yellow")
		diff_rect = diff_surf.get_rect(center=(self.center_x, 250))
		self.screen.blit(diff_surf, diff_rect)
		
		highscore_text = self.font_medium.render(f"Best Score: {self.highscore}", True, "#FFD700")
		highscore_rect = highscore_text.get_rect(center=(self.center_x, 310))
		self.screen.blit(highscore_text, highscore_rect)
		
		start_text = f"Press '{self.button}' to start"
		start_surf = self.font_medium.render(start_text, True, "green")
		start_rect = start_surf.get_rect(center=(self.center_x, 400))
		self.screen.blit(start_surf, start_rect)
		
		controls_surf = self.font_small.render("Arrow Keys: Move | A: Shoot", True, "white")
		controls_rect = controls_surf.get_rect(center=(self.center_x, 460))
		self.screen.blit(controls_surf, controls_rect)
		
		back_surf = self.font_small.render("Press 'B' to change difficulty", True, "gray")
		back_rect = back_surf.get_rect(center=(self.center_x, 520))
		self.screen.blit(back_surf, back_rect)
		
		self.crt.draw(self.screen)
	
	def draw_game(self):
		"""Herná obrazovka"""
		self.screen.blit(self.bg, (0, 0))
		
		# Game objects
		self.player.sprite.lasers.draw(self.screen)
		self.player.draw(self.screen)
		self.blocks.draw(self.screen)
		self.aliens.draw(self.screen)
		self.alien_lasers.draw(self.screen)
		self.extra.draw(self.screen)
		
		# HUD
		self.display_lives()
		self.display_score()
		
		self.crt.draw(self.screen)
	
	def display_lives(self):
		for live in range(self.lives - 1):
			x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
			self.screen.blit(self.live_surf,(x,8))

	def display_score(self):
		score_surf = self.font_small.render(f'Score: {self.score}',False,'white')
		score_rect = score_surf.get_rect(topleft = (10,-10))
		self.screen.blit(score_surf, score_rect)
	
	def draw_game_over(self):
		"""Game Over obrazovka"""
		self.screen.blit(self.bg, (0, 0))
		
		# Pozadie hry
		self.player.sprite.lasers.draw(self.screen)
		self.player.draw(self.screen)
		self.blocks.draw(self.screen)
		self.aliens.draw(self.screen)
		self.alien_lasers.draw(self.screen)
		self.extra.draw(self.screen)
		self.display_lives()
		self.display_score()
		
		overlay = pygame.Surface((self.width, self.height))
		overlay.set_alpha(180)
		overlay.fill((0,0,0))
		self.screen.blit(overlay, (0,0))
		
		game_over_surf = self.font_large.render("GAME OVER", False, "red")
		game_over_rect = game_over_surf.get_rect(center = (self.center_x, 200))
		self.screen.blit(game_over_surf, game_over_rect)
		
		final_score_surf = self.font_medium.render(f"Final Score: {self.score}", False, "white")
		final_score_rect = final_score_surf.get_rect(center = (self.center_x, 280))
		self.screen.blit(final_score_surf, final_score_rect)
		
		if self.score > self.highscore:
			new_best_surf = self.font_medium.render("NEW BEST SCORE!", False, "yellow")
			new_best_rect = new_best_surf.get_rect(center = (self.center_x, 340))
			self.screen.blit(new_best_surf, new_best_rect)
		else:
			best_surf = self.font_medium.render(f"Best: {self.highscore}", False, "yellow")
			best_rect = best_surf.get_rect(center = (self.center_x, 340))
			self.screen.blit(best_surf, best_rect)
		
		restart_surf = self.font_small.render(f"Press '{self.button}' to Play Again or ESC to Exit", False, "white")
		restart_rect = restart_surf.get_rect(center = (self.center_x, 450))
		self.screen.blit(restart_surf, restart_rect)
		
		# Uložiť skóre iba raz
		if not self._score_saved:
			self.save_system.update_score(f"SpaceInvaders_{self.difficulty}", self.score)
			self._score_saved = True
		
		self.crt.draw(self.screen)
	
	def draw_victory(self):
		"""Victory obrazovka"""
		self.screen.blit(self.bg, (0, 0))
		
		# Pozadie hry
		self.player.sprite.lasers.draw(self.screen)
		self.player.draw(self.screen)
		self.blocks.draw(self.screen)
		self.aliens.draw(self.screen)
		self.alien_lasers.draw(self.screen)
		self.extra.draw(self.screen)
		self.display_lives()
		self.display_score()
		
		overlay = pygame.Surface((self.width, self.height))
		overlay.set_alpha(180)
		overlay.fill((0,0,0))
		self.screen.blit(overlay, (0,0))
		
		victory_surf = self.font_large.render("VICTORY!", False, "green")
		victory_rect = victory_surf.get_rect(center = (self.center_x, 200))
		self.screen.blit(victory_surf, victory_rect)
		
		final_score_surf = self.font_medium.render(f"Final Score: {self.score}", False, "white")
		final_score_rect = final_score_surf.get_rect(center = (self.center_x, 280))
		self.screen.blit(final_score_surf, final_score_rect)
		
		if self.score > self.highscore:
			new_best_surf = self.font_medium.render("NEW BEST SCORE!", False, "yellow")
			new_best_rect = new_best_surf.get_rect(center = (self.center_x, 340))
			self.screen.blit(new_best_surf, new_best_rect)
		else:
			best_surf = self.font_medium.render(f"Best: {self.highscore}", False, "yellow")
			best_rect = best_surf.get_rect(center = (self.center_x, 340))
			self.screen.blit(best_surf, best_rect)
		
		restart_surf = self.font_small.render(f"Press '{self.button}' to Play Again or ESC to Exit", False, "white")
		restart_rect = restart_surf.get_rect(center = (self.center_x, 450))
		self.screen.blit(restart_surf, restart_rect)
		
		self.crt.draw(self.screen)


class CRT:
	def __init__(self, screen_width, screen_height):
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.tv = pygame.image.load('Games/assets/images/space_invaders/tv.png').convert_alpha()
		self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height))

	def create_crt_lines(self):
		line_height = 3
		line_amount = int(self.screen_height / line_height)
		for line in range(line_amount):
			y_pos = line * line_height
			pygame.draw.line(self.tv, 'black', (0, y_pos), (self.screen_width, y_pos), 1)

	def draw(self, screen):
		self.tv.set_alpha(randint(75,90))
		self.create_crt_lines()
		screen.blit(self.tv, (0, 0))


if __name__ == '__main__':
	game = SpaceInvaders(fullscreen=False, difficulty="normal")
	game.run()