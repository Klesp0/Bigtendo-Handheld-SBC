import pygame
from pygame.image import load
from pygame.time import get_ticks
from random import choice
from _game_base import Game
from _input_handler import InputHandler
from config import *

COLUMNS = 10
ROWS = 20
CELL_SIZE = 28  
GAME_WIDTH, GAME_HEIGHT = COLUMNS * CELL_SIZE, ROWS * CELL_SIZE

SIDEBAR_WIDTH = 200
PREVIEW_HEIGHT_FRACTION = 0.7
SCORE_HEIGHT_FRACTION = 1 - PREVIEW_HEIGHT_FRACTION

PADDING = 20
 
UPDATE_START_SPEED = 200
MOVE_WAIT_TIME = 200
ROTATE_WAIT_TIME = 200
BLOCK_OFFSET = pygame.Vector2(COLUMNS // 2, -1)

YELLOW = '#f1e60d'
RED = '#e51b20'
BLUE = '#204b9b'
GREEN = '#65b32e'
PURPLE = '#7b217f'
CYAN = '#6cc6d9'
ORANGE = '#f07e13'
GRAY = '#1C1C1C'
LINE_COLOR = '#FFFFFF'

TETROMINOS = {
	'T': {'shape': [(0,0), (-1,0), (1,0), (0,-1)], 'color': PURPLE},
	'O': {'shape': [(0,0), (0,-1), (1,0), (1,-1)], 'color': YELLOW},
	'J': {'shape': [(0,0), (0,-1), (0,1), (-1,1)], 'color': BLUE},
	'L': {'shape': [(0,0), (0,-1), (0,1), (1,1)], 'color': ORANGE},
	'I': {'shape': [(0,0), (0,-1), (0,-2), (0,1)], 'color': CYAN},
	'S': {'shape': [(0,0), (-1,0), (0,-1), (1,-1)], 'color': GREEN},
	'Z': {'shape': [(0,0), (1,0), (0,-1), (-1,-1)], 'color': RED}
}

SCORE_DATA = {1: 40, 2: 100, 3: 300, 4: 1200}


class Preview:
	def __init__(self, x, y):
		self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION))
		self.rect = self.surface.get_rect(topleft=(x, y))
		self.shape_surfaces = {shape: load(f"Games/assets/images/tetris/{shape}.png").convert_alpha() for shape in TETROMINOS.keys()}
		self.increment_height = self.surface.get_height() / 3

	def display_pieces(self, shapes):
		for i, shape in enumerate(shapes):
			shape_surface = self.shape_surfaces[shape]
			x = self.surface.get_width() / 2
			y = self.increment_height / 2 + i * self.increment_height
			rect = shape_surface.get_rect(center=(x, y))
			self.surface.blit(shape_surface, rect)

	def draw(self, display_surface, next_shapes):
		self.surface.fill(GRAY)
		self.display_pieces(next_shapes)
		display_surface.blit(self.surface, self.rect)
		pygame.draw.rect(display_surface, LINE_COLOR, self.rect, 2, 2)


class ScoreDisplay:
	def __init__(self, x, y):
		self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_FRACTION - PADDING))
		self.rect = self.surface.get_rect(topleft=(x, y))
		self.font = pygame.font.Font('Games/assets/fonts/Pixeltype.ttf', 30)
		self.increment_height = self.surface.get_height() / 3
		self.score = 0
		self.level = 1
		self.lines = 0

	def display_text(self, pos, text):
		text_surface = self.font.render(f'{text[0]}: {text[1]}', True, 'white')
		text_rect = text_surface.get_rect(center=pos)
		self.surface.blit(text_surface, text_rect)

	def draw(self, display_surface):
		self.surface.fill(GRAY)
		for i, text in enumerate([('Score', self.score), ('Level', self.level), ('Lines', self.lines)]):
			x = self.surface.get_width() / 2
			y = self.increment_height / 2 + i * self.increment_height
			self.display_text((x, y), text)
		display_surface.blit(self.surface, self.rect)
		pygame.draw.rect(display_surface, LINE_COLOR, self.rect, 2, 2)


class Timer:
	def __init__(self, duration, repeated=False, func=None):
		self.repeated = repeated
		self.func = func
		self.duration = duration
		self.start_time = 0
		self.active = False

	def activate(self):
		self.active = True
		self.start_time = get_ticks()

	def deactivate(self):
		self.active = False
		self.start_time = 0

	def update(self):
		current_time = get_ticks()
		if current_time - self.start_time >= self.duration and self.active:
			if self.func and self.start_time != 0:
				self.func()
			self.deactivate()
			if self.repeated:
				self.activate()


class GameBoard:
	def __init__(self, x, y, get_next_shape, update_score):
		self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
		self.rect = self.surface.get_rect(topleft=(x, y))
		self.sprites = pygame.sprite.Group()
		
		self.get_next_shape = get_next_shape
		self.update_score = update_score
		 
		self.line_surface = self.surface.copy()
		self.line_surface.fill((0, 255, 0))
		self.line_surface.set_colorkey((0, 255, 0))
		self.line_surface.set_alpha(120)
		
		self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
		self.tetromino = Tetromino(
			choice(list(TETROMINOS.keys())), 
			self.sprites, 
			self.create_new_tetromino,
			self.field_data)
		
		self.down_speed = UPDATE_START_SPEED
		self.down_speed_faster = self.down_speed * 0.3
		self.down_pressed = False
		self.timers = {
			'vertical move': Timer(self.down_speed, True, self.move_down),
			'horizontal move': Timer(MOVE_WAIT_TIME),
			'rotate': Timer(ROTATE_WAIT_TIME)
		}
		self.timers['vertical move'].activate()
		
		self.current_level = 1
		self.current_score = 0
		self.current_lines = 0
		
		self.game_over = False
		
		self.landing_sound = pygame.mixer.Sound('Games/assets/sounds/landing.wav')
		self.landing_sound.set_volume(0.1)

	def calculate_score(self, num_lines):
		self.current_lines += num_lines
		self.current_score += SCORE_DATA[num_lines] * self.current_level
		if self.current_lines / 10 > self.current_level:
			self.current_level += 1
			self.down_speed *= 0.75
			self.down_speed_faster = self.down_speed * 0.3
			self.timers['vertical move'].duration = self.down_speed
		self.update_score(self.current_lines, self.current_score, self.current_level)

	def check_game_over(self):
		for block in self.tetromino.blocks:
			if block.pos.y < 0:
				self.game_over = True
				return True
		return False

	def create_new_tetromino(self):
		self.landing_sound.play()
		if self.check_game_over():
			return
		self.check_finished_rows()
		self.tetromino = Tetromino(
			self.get_next_shape(), 
			self.sprites, 
			self.create_new_tetromino,
			self.field_data)

	def timer_update(self):
		for timer in self.timers.values():
			timer.update()

	def move_down(self):
		self.tetromino.move_down()

	def draw_grid(self):
		for col in range(1, COLUMNS):
			x = col * CELL_SIZE
			pygame.draw.line(self.line_surface, LINE_COLOR, (x, 0), (x, self.surface.get_height()), 1)
		for row in range(1, ROWS):
			y = row * CELL_SIZE
			pygame.draw.line(self.line_surface, LINE_COLOR, (0, y), (self.surface.get_width(), y))
		self.surface.blit(self.line_surface, (0, 0))

	def get_ghost_positions(self):
		drop = 0
		while True:
			can_move = True
			for block in self.tetromino.blocks:
				ny = int(block.pos.y) + drop + 1
				if ny >= ROWS:
					can_move = False; break
				if ny >= 0 and self.field_data[ny][int(block.pos.x)]:
					can_move = False; break
			if not can_move:
				break
			drop += 1
		return [(int(b.pos.x), int(b.pos.y) + drop) for b in self.tetromino.blocks]

	def hard_drop(self):
		while not self.tetromino.next_move_vertical_collide(self.tetromino.blocks, 1):
			for block in self.tetromino.blocks:
				block.pos.y += 1
		for block in self.tetromino.blocks:
			self.field_data[int(block.pos.y)][int(block.pos.x)] = block
		self.create_new_tetromino()

	def input(self, input_handler):
		if not self.timers['horizontal move'].active:
			if input_handler.is_pressed("LEFT"):
				self.tetromino.move_horizontal(-1)
				self.timers['horizontal move'].activate()
			if input_handler.is_pressed("RIGHT"):
				self.tetromino.move_horizontal(1)	
				self.timers['horizontal move'].activate()

		if not self.timers['rotate'].active:
			if input_handler.is_pressed("UP"):
				self.tetromino.rotate()
				self.timers['rotate'].activate()

		if not self.down_pressed and input_handler.is_pressed("DOWN"):
			self.down_pressed = True
			self.timers['vertical move'].duration = self.down_speed_faster

		if self.down_pressed and not input_handler.is_pressed("DOWN"):
			self.down_pressed = False
			self.timers['vertical move'].duration = self.down_speed

		if input_handler.just_pressed("A"):
			self.hard_drop()

	def check_finished_rows(self):
		delete_rows = []
		for i, row in enumerate(self.field_data):
			if all(row):
				delete_rows.append(i)

		if delete_rows:
			for delete_row in delete_rows:
				for block in self.field_data[delete_row]:
					block.kill()
				for row in self.field_data:
					for block in row:
						if block and block.pos.y < delete_row:
							block.pos.y += 1

			self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
			for block in self.sprites:
				self.field_data[int(block.pos.y)][int(block.pos.x)] = block

			self.calculate_score(len(delete_rows))

	def update_game(self):
		self.timer_update()
		self.sprites.update()

	def draw(self, display_surface):
		self.surface.fill(GRAY)

		for gx, gy in self.get_ghost_positions():
			if 0 <= gy < ROWS:
				ghost_surf = pygame.Surface((CELL_SIZE, CELL_SIZE))
				ghost_surf.fill(self.tetromino.color)
				ghost_surf.set_alpha(60)
				self.surface.blit(ghost_surf, (gx * CELL_SIZE, gy * CELL_SIZE))

		self.sprites.draw(self.surface)
		self.draw_grid()
		display_surface.blit(self.surface, self.rect)
		pygame.draw.rect(display_surface, LINE_COLOR, self.rect, 2, 2)


class Tetromino:
	def __init__(self, shape, group, create_new_tetromino, field_data):
		self.shape = shape
		self.block_positions = TETROMINOS[shape]['shape']
		self.color = TETROMINOS[shape]['color']
		self.create_new_tetromino = create_new_tetromino
		self.field_data = field_data
		self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]

	def next_move_horizontal_collide(self, blocks, amount):
		collision_list = [block.horizontal_collide(int(block.pos.x + amount), self.field_data) for block in self.blocks]
		return True if any(collision_list) else False

	def next_move_vertical_collide(self, blocks, amount):
		collision_list = [block.vertical_collide(int(block.pos.y + amount), self.field_data) for block in self.blocks]
		return True if any(collision_list) else False

	def move_horizontal(self, amount):
		if not self.next_move_horizontal_collide(self.blocks, amount):
			for block in self.blocks:
				block.pos.x += amount

	def move_down(self):
		if not self.next_move_vertical_collide(self.blocks, 1):
			for block in self.blocks:
				block.pos.y += 1
		else:
			for block in self.blocks:
				self.field_data[int(block.pos.y)][int(block.pos.x)] = block
			self.create_new_tetromino()

	def rotate(self):
		if self.shape != 'O':
			pivot_pos = self.blocks[0].pos
			new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]
			for pos in new_block_positions:
				if pos.x < 0 or pos.x >= COLUMNS:
					return
				if self.field_data[int(pos.y)][int(pos.x)]:
					return
				if pos.y > ROWS:
					return
			for i, block in enumerate(self.blocks):
				block.pos = new_block_positions[i]


class Block(pygame.sprite.Sprite):
	def __init__(self, group, pos, color):
		super().__init__(group)
		self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
		self.image.fill(color)
		self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
		self.rect = self.image.get_rect(topleft=self.pos * CELL_SIZE)

	def rotate(self, pivot_pos):
		return pivot_pos + (self.pos - pivot_pos).rotate(90)

	def horizontal_collide(self, x, field_data):
		if not 0 <= x < COLUMNS:
			return True
		if field_data[int(self.pos.y)][x]:
			return True

	def vertical_collide(self, y, field_data):
		if y >= ROWS:
			return True
		if y >= 0 and field_data[y][int(self.pos.x)]:
			return True

	def update(self):
		self.rect.topleft = self.pos * CELL_SIZE


class Tetris(Game):
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
		self.game_state = 0
		
		total_width = GAME_WIDTH + SIDEBAR_WIDTH + PADDING * 3
		total_height = GAME_HEIGHT + PADDING * 2
		
		start_x = (self.width - total_width) // 2
		start_y = (self.height - total_height) // 2
		
		self.game_x = start_x + PADDING
		self.game_y = start_y + PADDING
		
		self.preview_x = start_x + PADDING * 2 + GAME_WIDTH
		self.preview_y = start_y + PADDING
		
		self.score_x = start_x + PADDING * 2 + GAME_WIDTH
		self.score_y = start_y + PADDING + int(GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION) + PADDING
		
		self.next_shapes = [choice(list(TETROMINOS.keys())) for shape in range(3)]
		
		self.game_board = None
		self.score_display = ScoreDisplay(self.score_x, self.score_y)
		self.preview = Preview(self.preview_x, self.preview_y)
		
		self.font_large = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 60)
		self.font_medium = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 40)
		self.font_small = pygame.font.Font("Games/assets/fonts/Pixeltype.ttf", 30)
		
		self.bg = pygame.Surface((self.width, self.height))
		self.bg.fill(GRAY)
		
		self.music = pygame.mixer.Sound("Games/assets/sounds/music1.wav")
		self.music.set_volume(0.3)
		
		if self.i.GPIO1 and GPIO_ENABLED and self.i.GPIO:
			self.button = "A"
		else:
			self.button = "SPACE"
	
	def update_score_display(self, lines, score, level):
		self.score_display.lines = lines
		self.score_display.score = score
		self.score_display.level = level

	def get_next_shape(self):
		next_shape = self.next_shapes.pop(0)
		self.next_shapes.append(choice(list(TETROMINOS.keys())))
		return next_shape
	
	def start_game(self):
		self.game_board = GameBoard(self.game_x, self.game_y, self.get_next_shape, self.update_score_display)
		self.score_display.score = 0
		self.score_display.level = 1
		self.score_display.lines = 0
		self.next_shapes = [choice(list(TETROMINOS.keys())) for shape in range(3)]
		self.music.play(-1)
	
	def handle_input(self):
		if self.game_state == 0:  
			if self.i.just_pressed("A"):
				self.start_game()
				self.game_state = 1
		
		elif self.game_state == 1:  
			self.game_board.input(self.i)
		
		elif self.game_state == 2: 
			if self.i.just_pressed("A"):
				self.__init__(fullscreen=self.screen.get_flags() & pygame.FULLSCREEN)
	
	def update(self):
		if self.game_state == 1:  
			self.game_board.update_game()
			if self.game_board.game_over:
				self.game_state = 2
				self.music.stop()
				self.save_system.update_score(self.game_name, self.score_display.score)
	
	def draw(self):
		self.screen.blit(self.bg, (0, 0))
		if self.game_state == 0:
			self.draw_menu()
		elif self.game_state == 1:
			self.draw_game()
		elif self.game_state == 2:
			self.draw_game_over()
	
	def draw_menu(self):
		overlay = pygame.Surface((self.width, self.height))
		overlay.set_alpha(200)
		overlay.fill("black")
		self.screen.blit(overlay, (0, 0))
		
		title = self.font_large.render("TETRIS", True, CYAN)
		title_rect = title.get_rect(center=(self.center_x, self.center_y - 100))
		self.screen.blit(title, title_rect)
		
		highscore_text = self.font_medium.render(f"Best Score: {self.highscore}", True, "#FFD700")
		highscore_rect = highscore_text.get_rect(center=(self.center_x, self.center_y))
		self.screen.blit(highscore_text, highscore_rect)
		
		start_surf = self.font_medium.render(f"Press '{self.button}' to start", True, "white")
		start_rect = start_surf.get_rect(center=(self.center_x, self.center_y + 60))
		self.screen.blit(start_surf, start_rect)

		hint = self.font_small.render(f"'{self.button}' = hard drop during game", True, "gray")
		hint_rect = hint.get_rect(center=(self.center_x, self.center_y + 110))
		self.screen.blit(hint, hint_rect)
	
	def draw_game(self):
		self.game_board.draw(self.screen)
		self.score_display.draw(self.screen)
		self.preview.draw(self.screen, self.next_shapes)
	
	def draw_game_over(self):
		self.game_board.draw(self.screen)
		self.score_display.draw(self.screen)
		self.preview.draw(self.screen, self.next_shapes)
		
		overlay = pygame.Surface((self.width, self.height))
		overlay.set_alpha(200)
		overlay.fill("black")
		self.screen.blit(overlay, (0, 0))
		
		game_over_text = self.font_large.render("GAME OVER", True, RED)
		game_over_rect = game_over_text.get_rect(center=(self.center_x, self.center_y - 100))
		self.screen.blit(game_over_text, game_over_rect)
		
		final_score = self.score_display.score
		score_surf = self.font_medium.render(f"Score: {final_score}", True, "white")
		score_rect = score_surf.get_rect(center=(self.center_x, self.center_y - 20))
		self.screen.blit(score_surf, score_rect)
		
		lines_surf = self.font_medium.render(f"Lines: {self.score_display.lines}", True, "white")
		lines_rect = lines_surf.get_rect(center=(self.center_x, self.center_y + 30))
		self.screen.blit(lines_surf, lines_rect)
		
		level_surf = self.font_medium.render(f"Level: {self.score_display.level}", True, "white")
		level_rect = level_surf.get_rect(center=(self.center_x, self.center_y + 80))
		self.screen.blit(level_surf, level_rect)
		
		restart_surf = self.font_medium.render(f"Press '{self.button}' to restart", True, CYAN)
		restart_rect = restart_surf.get_rect(center=(self.center_x, self.center_y + 150))
		self.screen.blit(restart_surf, restart_rect)
		
		if final_score > self.highscore:
			record_surf = self.font_medium.render("NEW RECORD!", True, YELLOW)
			record_rect = record_surf.get_rect(center=(self.center_x, self.center_y - 150))
			self.screen.blit(record_surf, record_rect)

if __name__ == '__main__':
	tetris = Tetris(fullscreen=True)
	tetris.run()