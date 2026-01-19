# """
# Main Menu - Standalone Launcher
# Single controller navigation
#  """
# Pong can still have AI opponent - single player vs computer
# No multiplayer games - all single player
# Controller mapping - Only Controller 1 GPIO pins (17-26)
# Menu navigation - UP/DOWN/A/B only
# RetroPie integration - Works with single controller
# urobit potom, standalone menu
# import pygame
# import sys
# import os

# # Add parent to path
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# from shared.config import *
# from shared.gpio_handler import input_handler
# from shared.save_system import save_system

# # Import all games
# from games.Pygame.snake.snake import SnakeGame
# from games.Pygame.pong.pong import PongGame
# from games.Pygame.memory.memory import MemoryGame
# from games.Pygame.breakout.breakout import BreakoutGame
# from games.Pygame.space_invaders.invaders import SpaceInvadersGame
# from games.Pygame.tetris.tetris import TetrisGame

# pygame.init()
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
# clock = pygame.time.Clock()

# # Game list
# games = [
#     {"name": "Snake", "class": SnakeGame, "engine": "Pygame"},
#     {"name": "Tetris", "class": TetrisGame, "engine": "Pygame"},
#     {"name": "Pong", "class": PongGame, "engine": "Pygame"},
#     {"name": "Breakout", "class": BreakoutGame, "engine": "Pygame"},
#     {"name": "Space Invaders", "class": SpaceInvadersGame, "engine": "Pygame"},
#     {"name": "Memory", "class": MemoryGame, "engine": "Pygame"},
#     {"name": "Settings", "class": None, "engine": None},
#     {"name": "Exit", "class": None, "engine": None}
# ]

# selected = 0
# show_scores = False

# # Fonts
# font_title = pygame.font.Font(None, 96)
# font_game = pygame.font.Font(None, 60)
# font_small = pygame.font.Font(None, 36)
# font_tiny = pygame.font.Font(None, 24)

# def draw_menu():
#     screen.fill(BLACK)
    
#     # Title
#     title = font_title.render("RETRO CUBE", True, NINTENDO_RED)
#     title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 60))
#     screen.blit(title, title_rect)
    
#     # Subtitle
#     subtitle = font_small.render("Gaming Console", True, WHITE)
#     subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 120))
#     screen.blit(subtitle, subtitle_rect)
    
#     # Games list
#     start_y = 180
#     spacing = 50
    
#     for i, game in enumerate(games):
#         y = start_y + i * spacing
        
#         # Selection highlight
#         if i == selected:
#             pygame.draw.rect(screen, BLUE, (50, y - 5, 700, 45), 3)
#             color = YELLOW
#         else:
#             color = WHITE
        
#         # Game name
#         text = font_game.render(game["name"], True, color)
#         screen.blit(text, (70, y))
        
#         # High score (if available)
#         if game["class"]:
#             high_score = save_system.get_highscore(game["name"])
#             if high_score > 0:
#                 score_text = font_small.render(f"Best: {high_score}", True, GRAY)
#                 screen.blit(score_text, (500, y + 5))
        
#         # Engine badge
#         if game["engine"]:
#             engine_text = font_tiny.render(game["engine"], True, DARK_GREEN)
#             screen.blit(engine_text, (650, y + 10))
    
#     # Instructions
#     inst = font_small.render("UP/DOWN: Navigate  |  A: Select  |  B: Exit", True, GREEN)
#     inst_rect = inst.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
#     screen.blit(inst, inst_rect)
    
#     pygame.display.flip()

# def handle_input():
#     global selected, show_scores
    
#     keys = pygame.key.get_pressed()
    
#     # Navigate up
#     if keys[pygame.K_UP] or input_handler.is_pressed('UP'):
#         selected = (selected - 1) % len(games)
#         pygame.time.wait(200)
    
#     # Navigate down
#     if keys[pygame.K_DOWN] or input_handler.is_pressed('DOWN'):
#         selected = (selected + 1) % len(games)
#         pygame.time.wait(200)
    
#     # Select
#     if keys[pygame.K_RETURN] or keys[pygame.K_SPACE] or input_handler.is_pressed('A'):
#         return execute_selection()
    
#     # Exit
#     if keys[pygame.K_ESCAPE] or keys[pygame.K_b] or input_handler.is_pressed('B'):
#         return False
    
#     return True

# def execute_selection():
#     global selected
    
#     game = games[selected]
    
#     if game["name"] == "Exit":
#         return False
    
#     elif game["name"] == "Settings":
#         show_settings()
#         return True
    
#     elif game["class"]:
#         # Launch game
#         try:
#             game_instance = game["class"](screen, fullscreen=False)
#             final_score = game_instance.run()
            
#             # Update high score
#             if final_score > 0:
#                 is_record = save_system.update_score(game["name"], final_score)
#                 if is_record:
#                     show_new_record(game["name"], final_score)
        
#         except Exception as e:
#             print(f"Error launching {game['name']}: {e}")
#             show_error(game["name"], str(e))
        
#         return True
    
#     return True

# def show_settings():
#     """Settings screen"""
#     running = True
#     setting_selected = 0
#     settings = [
#         "Sound: ON",
#         "Display: 800x480",
#         "Controller Test",
#         "About",
#         "Back"
#     ]
    
#     while running:
#         screen.fill(BLACK)
        
#         # Title
#         title = font_title.render("SETTINGS", True, NINTENDO_RED)
#         title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
#         screen.blit(title, title_rect)
        
#         # Settings list
#         start_y = 180
#         for i, setting in enumerate(settings):
#             y = start_y + i * 60
            
#             if i == setting_selected:
#                 pygame.draw.rect(screen, BLUE, (100, y - 5, 600, 50), 3)
#                 color = YELLOW
#             else:
#                 color = WHITE
            
#             text = font_game.render(setting, True, color)
#             screen.blit(text, (120, y))
        
#         # Instructions
#         inst = font_small.render("UP/DOWN: Navigate  |  A: Select  |  B: Back", True, GREEN)
#         inst_rect = inst.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
#         screen.blit(inst, inst_rect)
        
#         pygame.display.flip()
        
#         # Input
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_UP:
#                     setting_selected = (setting_selected - 1) % len(settings)
#                 elif event.key == pygame.K_DOWN:
#                     setting_selected = (setting_selected + 1) % len(settings)
#                 elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
#                     if settings[setting_selected] == "Back":
#                         running = False
#                     elif settings[setting_selected] == "Controller Test":
#                         show_controller_test()
#                     elif settings[setting_selected] == "About":
#                         show_about()
#                 elif event.key == pygame.K_ESCAPE or event.key == pygame.K_b:
#                     running = False
        
#         clock.tick(FPS)

# def show_controller_test():
#     """Test controller buttons"""
#     running = True
    
#     while running:
#         screen.fill(BLACK)
        
#         title = font_title.render("CONTROLLER TEST", True, NINTENDO_RED)
#         title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
#         screen.blit(title, title_rect)
        
#         # Instructions
#         inst = font_small.render("Press buttons to test", True, WHITE)
#         inst_rect = inst.get_rect(center=(SCREEN_WIDTH // 2, 120))
#         screen.blit(inst, inst_rect)
        
#         # Button status
#         buttons = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'A', 'B', 'START', 'SELECT']
#         y = 180
        
#         for button in buttons:
#             is_pressed = input_handler.is_pressed(button)
#             color = GREEN if is_pressed else GRAY
#             text = font_game.render(f"{button}: {'PRESSED' if is_pressed else 'Released'}", True, color)
#             screen.blit(text, (150, y))
#             y += 50
        
#         # Back instruction
#         back = font_small.render("Press B to go back", True, GREEN)
#         back_rect = back.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
#         screen.blit(back, back_rect)
        
#         pygame.display.flip()
        
#         # Check for exit
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_b] or keys[pygame.K_ESCAPE] or input_handler.is_pressed('B'):
#             running = False
        
#         clock.tick(FPS)

# def show_about():
#     """About screen"""
#     running = True
    
#     while running:
#         screen.fill(BLACK)
        
#         title = font_title.render("ABOUT", True, NINTENDO_RED)
#         title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 60))
#         screen.blit(title, title_rect)
        
#         # Info
#         info_lines = [
#             "Retro Cube Console",
#             "Hellathon 2025",
#             "",
#             "Hardware:",
#             "- Raspberry Pi 5",
#             "- 7\" Display",
#             "- Custom Controller",
#             "",
#             "Software:",
#             "- Pygame Games",
#             "- Custom Launcher",
#             "",
#             "Team: [Your Team Name]"
#         ]
        
#         y = 140
#         for line in info_lines:
#             text = font_small.render(line, True, WHITE)
#             text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
#             screen.blit(text, text_rect)
#             y += 35
        
#         # Back
#         back = font_small.render("Press B to go back", True, GREEN)
#         back_rect = back.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
#         screen.blit(back, back_rect)
        
#         pygame.display.flip()
        
#         # Check exit
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_b] or keys[pygame.K_ESCAPE] or input_handler.is_pressed('B'):
#             running = False
        
#         clock.tick(FPS)

# def show_new_record(game_name, score):
#     """Show new high score screen"""
#     screen.fill(BLACK)
    
#     title = font_title.render("NEW RECORD!", True, YELLOW)
#     title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
#     screen.blit(title, title_rect)
    
#     game_text = font_game.render(game_name, True, WHITE)
#     game_rect = game_text.get_rect(center=(SCREEN_WIDTH // 2, 240))
#     screen.blit(game_text, game_rect)
    
#     score_text = font_game.render(f"Score: {score}", True, GREEN)
#     score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 310))
#     screen.blit(score_text, score_rect)
    
#     pygame.display.flip()
#     pygame.time.wait(3000)

# def show_error(game_name, error):
#     """Show error screen"""
#     screen.fill(BLACK)
    
#     title = font_title.render("ERROR", True, RED)
#     title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
#     screen.blit(title, title_rect)
    
#     game_text = font_game.render(f"Game: {game_name}", True, WHITE)
#     game_rect = game_text.get_rect(center=(SCREEN_WIDTH // 2, 240))
#     screen.blit(game_text, game_rect)
    
#     error_text = font_small.render(f"Error: {error[:40]}", True, RED)
#     error_rect = error_text.get_rect(center=(SCREEN_WIDTH // 2, 310))
#     screen.blit(error_text, error_rect)
    
#     pygame.display.flip()
#     pygame.time.wait(3000)

# # Main loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
    
#     draw_menu()
#     running = handle_input()
#     clock.tick(FPS)

# pygame.quit()
# input_handler.cleanup()
# sys.exit()