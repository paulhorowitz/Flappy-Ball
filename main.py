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
    return defender_list

def drawdefender(defender_list):
    for defender in defender_list:
        if defender.bottom >= 1024:
            screen.blit(defender_surface, defender)
        else:
            flip_defender = pygame.transform.flip(defender_surface, False, True)
            screen.blit(flip_defender, defender)

def check_collision(defender_list):
    for defender in defender_list:
        if ball_rect.colliderect(defender):
            return False

    if ball_rect.top <= -100 or ball_rect.bottom >= 900:
        return False

    return True

pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()

# Game Variables
gravity = 0.25
ball_movement = 0
game_active = True

bg_surface = pygame.image.load('assets/background-day.png').convert()
floor_surface = pygame.image.load('assets/base.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)
floor_surface = pygame.transform.scale2x(floor_surface)
floor_surface2 = floor_surface
floor_x_pos = 0

ball_surface = pygame.image.load('assets/basketball_trans.png')
#ball_surface = pygame.transform.scale2x(ball_surface)
ball_rect = ball_surface.get_rect(center=(100, 512))

defender_surface = pygame.image.load('assets/flappy-ball-defender2.png')
#defender_surface = pygame.transform.scale2x(defender_surface)
defender_list = []
SPAWNDEFENDER = pygame.USEREVENT
pygame.time.set_timer(SPAWNDEFENDER, 1200)
defender_height = [400, 600, 800]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True:
                ball_movement = 0
                ball_movement -= 12
            if event.type == pygame.KEYDOWN and game_active == False:
                game_active = True
                defender_list.clear()
                ball_rect.center = (100, 512)
                ball_movement = 0


        if event.type == SPAWNDEFENDER:
            defender_list.extend(create_defender())

    if game_active:

        screen.blit(bg_surface, (0, 0))

        # Bird

        ball_movement += gravity
        ball_rect.centery += ball_movement
        screen.blit(ball_surface, ball_rect)
        game_active = check_collision(defender_list)

        # Defender
        defender_list = move_defender(defender_list)
        drawdefender(defender_list)

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
