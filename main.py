import pygame

# Часы фреймов
clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((700, 400))
pygame.display.set_caption("LOTUS PYGAME")
ikon = pygame. image.load('images/ikon.jpeg')
pygame.display.set_icon(ikon)

bg = pygame.image.load('images/background01.png')
wakl_left = [
    pygame.image.load('images/player_left/Luan01.png'),
    pygame.image.load('images/player_left/Luan02.png'),
    pygame.image.load('images/player_left/Luan03.png'),
    pygame.image.load('images/player_left/Luan04.png'),
]

wakl_right = [
    pygame.image.load('images/player_right/Luan001.png'),
    pygame.image.load('images/player_right/Luan002.png'),
    pygame.image.load('images/player_right/Luan003.png'),
    pygame.image.load('images/player_right/Luan004.png'),

]

player_animation_count = 0
bg_x = 0

player_speed = 5
player_x = 150
player_y = 250

is_jump = False
jump_count = 7 # Сила прыжка. Если установим большее число - будет прыгать выше, если ниже, то ниже

bg_sound = pygame.mixer.Sound('sounds/game_sound.mp3')
bg_sound.play()

# основной цикл
running = True
while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 618, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        screen.blit(wakl_left[player_animation_count], (player_x, player_y))
    else:
        screen.blit(wakl_right[player_animation_count], (player_x, player_y))

    if keys[pygame.K_LEFT] and player_x > 50:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT] and player_x < 200:
        player_x += player_speed

    if not is_jump:
        if keys[pygame.K_SPACE]:
            is_jump = True
    else:
        if jump_count >= -7:
            if jump_count > 0:
                player_y -= (jump_count ** 2) / 2
            else:
                player_y += (jump_count ** 2) / 2
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 7

    if player_animation_count == 3:
        player_animation_count = 0
    else:
        player_animation_count += 1

    bg_x -= 2
    if bg_x == -618:
        bg_x = 0

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    clock.tick(10) # скорость шага героя