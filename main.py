import pygame, sys

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))

pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()

bg_surface = pygame.image.load('assets/background-day.png').convert()
floor_surface = pygame.image.load('assets/base.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)
floor_surface = pygame.transform.scale2x(floor_surface)
floor_surface2 = floor_surface
floor_x_pos = 0

ball_surface = pygame.image.load('assets/basketball_trans.png')
ball_surface = pygame.transform.scale2x(ball_surface)
ball_rect = ball_surface.get_rect(center=(100, 512))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(bg_surface, (0, 0))
    screen.blit(ball_surface, ball_rect)
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
