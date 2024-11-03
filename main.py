import pygame
from pygame import Rect
from pygame.rect import RectType

# Часы фреймов
clock = pygame.time.Clock()

# Задний фон
pygame.init()
screen = pygame.display.set_mode((700, 400))
pygame.display.set_caption("LOTUS PYGAME")
ikon = pygame. image.load('images/ikon.jpeg')
pygame.display.set_icon(ikon)

# Player
# Конвертация изображений
bg = pygame.image.load('images/background01.png').convert()
walk_left = [
    pygame.image.load('images/player_left/Luan01.png').convert_alpha(),
    pygame.image.load('images/player_left/Luan02.png').convert_alpha(),
    pygame.image.load('images/player_left/Luan03.png').convert_alpha(),
    pygame.image.load('images/player_left/Luan04.png').convert_alpha(),
]
walk_right = [
    pygame.image.load('images/player_right/Luan001.png').convert_alpha(),
    pygame.image.load('images/player_right/Luan002.png').convert_alpha(),
    pygame.image.load('images/player_right/Luan003.png').convert_alpha(),
    pygame.image.load('images/player_right/Luan004.png').convert_alpha(),

]

ghost = pygame.image.load('images/ghost.png').convert_alpha()
ghost_list_in_game = []

player_animation_count = 0
bg_x = 0

# Координаты игрока
player_speed = 5
player_x = 150
player_y = 229

is_jump = False
jump_count = 8

bg_sound = pygame.mixer.Sound('sounds/game_sound.mp3')
# bg_sound.play()

# Таймер для появления монстра
ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

# Отображение надписи
label = pygame.font.Font('font/Monocraft.otf', 45)
lose_label = label.render("Вы проиграли!", False, (28, 28, 27))
# Рестарт игры
restart_label = label.render("Играть заново!", False, (66, 103, 138))
restart_label_rect = restart_label.get_rect(topleft=(190, 199)) # Для отслеживания прикосновений, нажатий и т.д.

# Добавление снаряда в игру
paintballs_left = 5
paintball = pygame.image.load('images/paintball.png').convert_alpha()
paintballs = []


# Остановка игры
gameplay = True


# основной цикл
running = True
while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 618, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

    # Вывод всех монстров на экран
        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 10

                #удаление монстра
                if el.x < -10:
                    ghost_list_in_game.pop(i) # для удаления монстра через индекс, который будет приписан в 69 строчке кода через новую переменную и через функцию enumerate, чтобы правильно шло печисление(который перебирает список ghost_list_in_game)

                if player_rect.colliderect(el):
                    gameplay = False #Как только игрок прикоснеться призрока, то экран поменяет цвет

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_animation_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_animation_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 200:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_animation_count == 3:
            player_animation_count = 0
        else:
            player_animation_count += 1

        bg_x -= 2
        if bg_x == -618:
            bg_x = 0

        # Отслеживание нажатия
        # if keys[pygame.K_a]: # при нажатии клавищи "а" мф просто добавим новый элемент внутр списка paintballs
        #     paintballs.append(paintball.get_rect(topleft=(player_x + 50, player_y + 15)))


        # Отображение патронов и их передвижение
        if paintballs: # Проверяем есть ли этот список. Есть ли в нем какие-то элементы
            for (i, el) in enumerate(paintballs): # Перебираем все элементы
                screen.blit(paintball, (el.x, el.y)) # Под каждый элемент рисуем по сути картинку со снарядом. Указываем что снаряды будут находится в тех координатах, которые указывали для предыдущего сноряда из 128 строки
                el.x += 4 # Сам снаряд будем передвигать по координату "х" к врагам

                # Удаление снаряда
                if el.x > 720:
                    paintballs.pop(i)

                # Уничтожение врагов
                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el): # el это по сути снаряд и когда он столкнется с монстром
                            ghost_list_in_game.pop(index) # То в таком случае мы удаляем монстра из всей игры, из списка
                            paintballs.pop(i) # И сам по себе снаряд мы также удаляем

    else:
        screen.fill((18, 47, 170))
        screen.blit(lose_label, (190, 99))
        screen.blit(restart_label, restart_label_rect)

        # Обработчик событий, который будет срабатывать при нажатии кнопки
        mous = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mous) and pygame.mouse.get_pressed()[0]: # Проверяет совпадает ли квадрат  restart_label_rect с мышкой и через pygame.mouse.get_pressed() после нажатия кнопки мышью игра заново запускается
            gameplay = True
            player_x = 150
            ghost_list_in_game.clear()
            paintballs.clear() # Удаление снаряда (связь 1)
            paintballs_left = 5 # Перезапукается сноряд, когда та заканчивается в условии с 173 по 175 строки


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(618, 229)))
        # Отслеживание нажатия (исправленная версия)
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_a and paintballs_left > 0:
            paintballs.append(paintball.get_rect(topleft=(player_x + 50, player_y + 15)))
            paintballs_left -= 1 # Весь этот код будет выполняться если paintballs_left больше 0, если 0 снарядом, то часть кода с "ограничение по снарядам" не будет выполняться

    clock.tick(7) #Cкорость шага героя
