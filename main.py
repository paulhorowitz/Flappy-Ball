import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))

def create_defender():
    random_defender_pos = random.choice(defender_height)
    bottom_defender = defender_surface.get_rect(midtop=(700, random_defender_pos))
    top_defender = defender_surface.get_rect(midbottom=(700, random_defender_pos - 400))
    return bottom_defender, top_defender

def move_defender(defender_list):
    for defender in defender_list:
        defender.centerx -= 5
    visible_defenders = [defender for defender in defender_list if defender.right > -50]
    return visible_defenders

def drawdefender(defender_list):
    for defender in defender_list:
        if defender.bottom >= 1024:
            screen.blit(defender_surface, defender)
        else:
            flip_defender = pygame.transform.flip(defender_surface, False, True)
            screen.blit(flip_defender, defender)

def check_collision(defender_list):
    global can_score
    for defender in defender_list:
        if ball_rect.colliderect(defender):
            death_sound.play()
            return False

    if ball_rect.top <= -100 or ball_rect.bottom >= 900:
        can_score = True
        return False

    return True

def rotate_ball(ball):
    new_ball = pygame.transform.rotozoom(ball, ball_movement * 1.5, 1)
    return new_ball

def ball_animation():
    new_ball = ball_frames[ball_index]
    new_ball_rect = new_ball.get_rect(center = (100, ball_rect.centery))
    return new_ball, new_ball_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f'Score: {(int(score))}', True, [255,255,255])
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {(int(score))}', True, [255,255,255])
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {(int(high_score))}', True, [255,255,255])
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def defender_score_check():
    global score, can_score
    if defender_list:
        for defender in defender_list:
            if 95 < defender.centerx < 105 and can_score:
                score += 1
                can_score = False
            if defender.centerx < 0:
                can_score = True

pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04b_19.ttf',40)

# Game Variables
gravity = 0.25
ball_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

bg_surface = pygame.image.load('assets/background-day.png').convert()
floor_surface = pygame.image.load('assets/base.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)
floor_surface = pygame.transform.scale2x(floor_surface)
floor_surface2 = floor_surface
floor_x_pos = 0

ball_downflap = pygame.transform.scale2x(pygame.image.load('assets/basketball_trans_downflap.png').convert_alpha())
ball_midflap = pygame.transform.scale2x(pygame.image.load('assets/basketball_trans_midflap.png').convert_alpha())
ball_upflap = pygame.transform.scale2x(pygame.image.load('assets/basketball_trans_upflap.png').convert_alpha())
ball_frames = [ball_downflap, ball_midflap, ball_upflap]
ball_index = 0
ball_surface = ball_frames[ball_index]
ball_rect = ball_surface.get_rect(center=(100, 512))

BALLFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BALLFLAP, 200)

#ball_surface = pygame.image.load('assets/basketball_trans.png').convert_alpha()
#ball_surface = pygame.transform.scale2x(ball_surface)
#ball_rect = ball_surface.get_rect(center=(100, 512))
#ball_mask = pygame.mask.from_surface(ball_surface)

defender_surface = pygame.image.load('assets/flappy-ball-defender2.png')
defender_surface = pygame.transform.scale2x(defender_surface)
defender_mask = pygame.transform.scale2x(defender_surface)
defender_list = []
SPAWNDEFENDER = pygame.USEREVENT
pygame.time.set_timer(SPAWNDEFENDER, 1200)
defender_height = [400, 600, 800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/messageball.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(288, 512))

flap_sound = pygame.mixer.Sound('assets/audio/wing.wav')
death_sound = pygame.mixer.Sound('assets/audio/rejected.wav')
score_sound = pygame.mixer.Sound('assets/audio/point.wav')
score_sound_countdown = 100

while True:

    screen.blit(bg_surface, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True:
                ball_movement = 0
                ball_movement -= 12
                flap_sound.play()
            if event.type == pygame.KEYDOWN and game_active == False:
                game_active = True
                defender_list.clear()
                ball_rect.center = (100, 512)
                ball_movement = 0
                score = 0

        if event.type == SPAWNDEFENDER:
            defender_list.extend(create_defender())

        if event.type == BALLFLAP:
            if ball_index < 2:
                ball_index += 1
            else:
                ball_index = 0

            ball_surface, ball_rect = ball_animation()

    if game_active:

        # Ball
        ball_movement += gravity
        rotated_ball = rotate_ball(ball_surface)
        ball_rect.centery += ball_movement
        screen.blit(rotated_ball, ball_rect)
        game_active = check_collision(defender_list)

        # Defender
        defender_list = move_defender(defender_list)
        drawdefender(defender_list)

        # Score
        defender_score_check()
        score_display('main_game')

    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
