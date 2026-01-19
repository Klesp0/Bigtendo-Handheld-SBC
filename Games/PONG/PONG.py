import pygame
from random import randint

pygame.init()

screen = pygame.display.set_mode((1024, 600))

#score
sc1 = 0
sc2 = 0

#ball move vars
bmove_x = 0
bmove_y = 0
ball_speed = 300
ball_speed_mult = 1.0

# * * * * * PAIN * * * * *

#text
font1 = pygame.font.Font("SW/PONG/Pixeltype.ttf",50)
font_surface = font1.render(f"{sc1}    {sc2}", False, "#000000").convert_alpha()
font_rect = font_surface.get_rect(center=(512,50))

pongtext_surface = font1.render("Pong", False, "white").convert_alpha()
pongtext_rect = pongtext_surface.get_rect(center = (512, 250))

pongtext2_surface = font1.render("Press SPACE to start", False, "white").convert_alpha()
pongtext2_rect = pongtext2_surface.get_rect(center = (512, 350))

wintext1_surf = font1.render("Player 1 won.",False, "white").convert_alpha()
wintext1_rect = wintext1_surf.get_rect(center = (512, 250))

wintext2_surf = font1.render("Player 2 won.",False, "white").convert_alpha()
wintext2_rect = wintext2_surf.get_rect(center = (512, 250))

#p1
player = pygame.image.load("SW/PONG/pongPlayer.png").convert_alpha()
player = pygame.transform.scale(
    player,
    (player.get_width() * 8, player.get_height() * 8))
player_rect = player.get_rect(midright=(100,300))

#p2
player2 = pygame.image.load("SW/PONG/pongPlayer2.png").convert_alpha()
player2 = pygame.transform.scale(
    player2,
    (player2.get_width() * 8, player2.get_height() * 8))
player2_rect = player2.get_rect(midleft=(1024-100,300))

#ball
ball = pygame.image.load("SW/PONG/pongBall.png").convert_alpha()
ball = pygame.transform.scale(
    ball,
    (ball.get_width() * 2, ball.get_height() * 2))
ball_rect = ball.get_rect(center=(512,300))

#mid line
line = pygame.image.load("SW/PONG/pongLine.png").convert_alpha()
line = pygame.transform.scale(
    line,
    (line.get_width() * 6, line.get_height() * 20))
line_rect = line.get_rect(center=(512,300))

#score board
board = pygame.image.load("SW/PONG/scoreBoard.png").convert_alpha()
board = pygame.transform.scale(
    board,
    (board.get_width() * 4, board.get_height() * 4))
board_rect = board.get_rect(center=(512,45))


running = True
clock = pygame.time.Clock()
movement_speed = 450  # pixels per second
game_state = 0

#title screen
def game_state0():
    if keys[pygame.K_SPACE]:
        global game_state, bmove_x, bmove_y, ball_speed_mult
        game_state += 1

        # randomize starting direction
        ball_speed_mult = 1.0
        bmove_x = randint(0,1)*2 - 1     # -1 or +1
        bmove_y = randint(-1,1)

    screen.blit(pongtext_surface,pongtext_rect)
    screen.blit(pongtext2_surface,pongtext2_rect)

#main game
def game_state1():
    global game_state, sc1, sc2, bmove_x, bmove_y, ball_speed_mult

    # Player 1
    if keys[pygame.K_w]:
        if player_rect.top>=0:
            player_rect.y -= movement_speed * delta_time
    if keys[pygame.K_s]:
        if player_rect.bottom<=600:
            player_rect.y += movement_speed * delta_time

    # Player 2
    if keys[pygame.K_UP]:
        if player2_rect.top>=0:
            player2_rect.y -= movement_speed * delta_time
    if keys[pygame.K_DOWN]:
        if player2_rect.bottom<=600:
            player2_rect.y += movement_speed * delta_time

    # ---- BALL MOVEMENT ----
    ball_rect.x += bmove_x * ball_speed * ball_speed_mult * delta_time
    ball_rect.y += bmove_y * ball_speed * ball_speed_mult * delta_time

    # Wall bounce
    if ball_rect.top <= 0:
        ball_rect.top = 0
        bmove_y *= -1
    elif ball_rect.bottom >= 600:
        ball_rect.bottom = 600
        bmove_y *= -1

    # Paddle bounce (player 1)
    if ball_rect.colliderect(player_rect) and bmove_x < 0:
        bmove_x *= -1
        bmove_y = randint(-2, 2)
        ball_speed_mult += 0.10  # increase speed

    # Paddle bounce (player 2)
    if ball_rect.colliderect(player2_rect) and bmove_x > 0:
        bmove_x *= -1
        bmove_y = randint(-2, 2)
        ball_speed_mult += 0.10

    # ---- SCORING ----
    if ball_rect.right < 0:
        sc2 += 1
        ball_rect.center = (512,300)
        ball_speed_mult = 1.0
        bmove_x = randint(0,1)*2 - 1
        bmove_y = randint(-1,1)

    elif ball_rect.left > 1024:
        sc1 += 1
        ball_rect.center = (512,300)
        ball_speed_mult = 1.0
        bmove_x = randint(0,1)*2 - 1
        bmove_y = randint(-1,1)

    if sc1 == 10 or sc2 == 10:
        game_state += 1

    # DRAW
    screen.fill((0,0,0))
    screen.blit(line,line_rect)
    screen.blit(board,board_rect)
    screen.blit(font1.render(f"{sc1}    {sc2}", False, "#000000").convert_alpha(), font_rect) 
    screen.blit(player, player_rect)
    screen.blit(ball, ball_rect)
    screen.blit(player2, player2_rect)

#game over screen
def game_state2():
    if keys[pygame.K_SPACE]:
        global game_state, sc1, sc2
        ball_rect.center = (512,300)
        sc1 = 0
        sc2 = 0
        game_state -= 1

    if sc1 == 10:
        screen.blit(wintext1_surf,wintext1_rect)
    else: 
        screen.blit(wintext1_surf,wintext1_rect)

    screen.blit(pongtext2_surface,pongtext2_rect)

while running:
    # ---- Time management ----
    delta_time = clock.tick(60) / 1000  # seconds
    delta_time = max(0.001, min(0.1, delta_time))

    # ---- Event handling ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    keys = pygame.key.get_pressed()

    screen.fill("#000000")

    # ---- Update ----
    if game_state == 0:
        game_state0()
    if game_state == 1:
        game_state1()
    if game_state == 2:
        game_state2()

    pygame.display.flip()

pygame.quit()