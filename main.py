import pygame
import os
import sys
import random
from pygame.locals import *
from button import Button

pygame.font.init()

pygame.init()

# Создаём окно

size = width, height = 710, 670
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Space Invaders')


def get_font(size):  # Возвращает шрифт в заданном размере
    return pygame.font.Font("Игоря на pygame assets/Mono_cyr.ttf", size)


# Загружаем музыку
pygame.mixer.music.load(os.path.join('Игоря на pygame assets', 'Hecu.mp3'))
pygame.mixer.music.play(-1)
postal = pygame.mixer.Sound(os.path.join('Игоря на pygame assets', 'Postal.mp3'))

# Загружаем изображения
space_ship_shooting = pygame.image.load(os.path.join('Игоря на pygame assets', 'enemyBlack1.png'))
suicide_ship = pygame.image.load(os.path.join('Игоря на pygame assets', 'sprite_ship_3.png'))
# mother_ship = pygame.image.load(os.path.join('Игоря на pygame assets', 'playerShip1_red.png'))

# Корабль игрока
player_space_ship = pygame.image.load(os.path.join('Игоря на pygame assets', 'playerShip1_red.png'))
damage = pygame.image.load(os.path.join('Игоря на pygame assets', 'damage.png'))

# Пули
player_bullet = pygame.image.load(os.path.join('Игоря на pygame assets', 'laserRed01.png'))
enemy_bullet = pygame.image.load(os.path.join('Игоря на pygame assets', 'laserBlue01.png'))

# Аптечка
medkit = pygame.image.load(os.path.join('Игоря на pygame assets', 'pill_blue.png'))

# Задний фон
bg = pygame.image.load(os.path.join('Игоря на pygame assets', 'black.png'))

# Цвета
red = (255, 0, 0)
white = (255, 255, 255)


def play():
    class Player(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.laser_image = player_bullet
            self.x = x
            self.y = y

            self.lives = 3
            self.score = 0

            #  Корабль изображение
            image = player_space_ship
            image_scale = 50 / image.get_rect().width
            new_width = image.get_rect().width * image_scale
            new_height = image.get_rect().height * image_scale
            scaled_size = (new_width, new_height)
            self.image = pygame.transform.scale(image, scaled_size)

            self.rect = self.image.get_rect()

            # Для отображения урона
            self.invincibility_frames = 0
            damage_image = damage
            image_scale = 90 / damage_image.get_rect().width
            new_width = damage_image.get_rect().width * image_scale
            new_height = damage_image.get_rect().height * image_scale
            scaled_size = (new_width, new_height)
            self.damage_image = pygame.transform.scale(damage_image, scaled_size)

        def update(self):
            self.rect.x = self.x
            self.rect.y = self.y

            if self.invincibility_frames > 0:
                self.invincibility_frames -= 1

        def draw_damage(self):

            if self.invincibility_frames > 0:
                damage_x = self.x - self.image.get_width() / 3
                damage_y = self.y - self.image.get_height() / 2
                screen.blit(self.damage_image, (damage_x, damage_y))

    class Enemy(pygame.sprite.Sprite):

        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.x = x
            self.y = y

            # Корабль
            self.image = suicide_ship

            # Ставим кол-во ударов для убийства корабля
            # И очки за его убийство
            self.hits = 1
            self.points = 1

            # Rect коробля
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]

        def update(self):

            # Двигаем корабль вниз
            self.rect.y += 3

            # Проверяем коллизию с игроком
            if pygame.sprite.spritecollide(self, player_group, False):
                self.kill()

                # Cнижаем здоровье игрока, при получении урона от корабля
                if player.invincibility_frames == 0:
                    player.lives -= 1

                    # Отоброжаем картинку повреждения
                    player.invincibility_frames = 60

            # Проверяем коллизию со снарядом
            if pygame.sprite.spritecollide(self, bullet_group, True):
                self.hits -= 1

                # Увеличеваем счёт
                if self.hits == 0:
                    player.score += self.points

            # Убираем корабль, когда он улитает за экран или уничтожается игроком
            if self.rect.top > height or self.hits == 0:
                self.kill()

    class Bullets(pygame.sprite.Sprite):

        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.rect = Rect(x, y, 4, 8)  # Cоздаём ректэнглы, которые будут иметь роль снарядов

        def draw(self):
            for w in range(self.rect.width):
                for h in range(self.rect.height):
                    screen.set_at((self.rect.x + w, self.rect.y - h), red)  # Делаем заливку снаряда по x и y

        def update(self):

            # Пули стреляют в экран
            self.rect.y -= 5

            # Отображаем пули ил убираем их когда они пропадают с экрана
            if self.rect.bottom > 0:
                self.draw()
            else:
                self.kill()

    class EnemyShooting(pygame.sprite.Sprite):

        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.x = x
            self.y = y

            # Корабль
            self.image = space_ship_shooting

            # Ставим кол-во ударов для убийства корабля
            # И очки за его убийство
            self.hits = 3
            self.points = 3

            # Rect коробля
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]

        def update(self):

            # Двигаем корабль вниз
            self.rect.y += 2

            # Переворачиваем корабль

            # Проверяем коллизию с игроком
            if pygame.sprite.spritecollide(self, player_group, False):
                self.kill()

                # Cнижаем здоровье игрока, при получении урона от корабля
                if player.invincibility_frames == 0:
                    player.lives -= 1

                    # Отоброжаем картинку повреждения на 60 кадров
                    player.invincibility_frames = 60

            # Проверяем коллизию со снарядом
            if pygame.sprite.spritecollide(self, bullet_group, True):
                self.hits -= 1

                # Увеличеваем счёт игрока
                if self.hits == 0:
                    player.score += self.points

            # Убираем корабль, когда он улитает за экран или уничтожается игроком
            if self.rect.top > height or self.hits == 0:
                enemy_bullet_group.remove()
                self.kill()

    class EnemyBullets(pygame.sprite.Sprite):

        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.rect = Rect(x, y, 4, 8)  # Cоздаём ректэнглы, которые будут иметь роль снарядов

        def draw(self):
            for w in range(self.rect.width):
                for h in range(self.rect.height):
                    screen.set_at((self.rect.x + w, self.rect.y - h), white)  # Делаем заливку снаряда по x и y

        def update(self):

            # Пули стреляют в экран
            self.rect.y += 5

            # Отображаем пули ил убираем их когда они пропадают с экрана
            if self.rect.bottom > 0:
                self.draw()
            else:
                self.kill()

            if pygame.sprite.spritecollide(self, player_group, False):
                self.kill()

                if player.invincibility_frames == 0:
                    player.lives -= 1

                    player.invincibility_frames = 60

    class Medkit(pygame.sprite.Sprite):

        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.x = x
            self.y = y

            # Корабль
            self.image = medkit

            # Rect коробля
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]

        def update(self):

            # Двигаем корабль вниз
            self.rect.y += 1

            # Переворачиваем корабль

            # Проверяем коллизию с игроком
            if pygame.sprite.spritecollide(self, player_group, False):
                self.kill()

                # Увеличиваем здоровье игрока

                player.lives += 1

            # Убираем корабль, когда он улитает за экран или уничтожается игроком
            if self.rect.top > height:
                self.kill()

    # Группы спрайтов
    player_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    enemy_bullet_group = pygame.sprite.Group()
    enemy_shooting_group = pygame.sprite.Group()
    medkit_group = pygame.sprite.Group()

    # Создаём игрока
    player_x = 250
    player_y = 450
    player = Player(player_x, player_y)
    player_group.add(player)

    # Кулдаун снарядов
    bullet_cooldown = 390
    bullet_cooldown_shooting_ship = 200
    last_bullet_enemy = pygame.time.get_ticks() - bullet_cooldown_shooting_ship
    last_bullet = pygame.time.get_ticks() - bullet_cooldown

    # Создаём корабль-камикадзе
    def create_suicide_ship():
        # Ставим рандомные x координаты
        s_ship_x = random.randint(50, width - 50)

        # Ставим корабль в вверх экрана
        s_ship_y = 0

        s_ship = Enemy(s_ship_x, s_ship_y)
        enemy_group.add(s_ship)

    # Создаём аптечки
    def create_medkit():
        # Ставим рандомные x координаты
        med_x = random.randint(50, width - 50)

        # Ставим аптечку в вверх экрана
        med_y = 0

        medkt = Medkit(med_x, med_y)
        enemy_group.add(medkt)

    # Создаём стреляющий корабль

    def create_shooting_ship():

        # Ставим рандомные x координаты
        s_ship_x = random.randint(50, width - 50)

        # Ставим корабль в вверх экрана
        s_ship_y = 0

        shootin_ship = EnemyShooting(s_ship_x, s_ship_y)
        enemy_group.add(shootin_ship)

    # Создаём первый корабль-камикадзе
    create_suicide_ship()

    # Создаём, первый стреляющий корабль
    s_ship_x = random.randint(50, width - 50)
    s_ship_y = 0
    shootin_ship = EnemyShooting(s_ship_x, s_ship_y)
    enemy_group.add(shootin_ship)

    # Игровой цикл
    clock = pygame.time.Clock()
    fps = 120
    running = True
    loop_ctr = 0
    loop_ctr_2 = 0
    loop_ctr_3 = 0
    test = 0

    main_font = pygame.font.SysFont('timesnewroman', 35)
    main_font_for_gameover = pygame.font.SysFont('timesnewroman', 25)
    another_font = pygame.font.SysFont('timesnewroman', 65)
    while running:
        loop_ctr += 1
        loop_ctr_2 += 1
        loop_ctr_3 += 1

        test += 1

        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Двигаем корабль, используя wasd
        if keys[K_a] and player.rect.left > 0:
            player.x -= 2
        elif keys[K_d] and player.rect.right < width:
            player.x += 2
        elif keys[K_w] and player.rect.top > 0:
            player.y -= 2
        elif keys[K_s] and player.rect.bottom < height:
            player.y += 2

        # Cтреляем снарядами с помрщью пробела
        if keys[K_SPACE]:

            # ждём какое-то время перед тем как стрелять другим снарядом
            current_time = pygame.time.get_ticks()
            if current_time - last_bullet > bullet_cooldown:
                bullet = Bullets(player.rect.centerx, player.rect.y)
                bullet_group.add(bullet)

                last_bullet = current_time

        if test == 50:  # !!!!!!!
            test = 0
            current_timee = pygame.time.get_ticks()
            if current_timee - last_bullet_enemy > bullet_cooldown_shooting_ship:
                bullet_enemy = EnemyBullets(shootin_ship.rect.centerx, shootin_ship.rect.y + 25)
                enemy_bullet_group.add(bullet_enemy)

                last_bullet_enemy = current_timee

            if shootin_ship.hits == 0:
                enemy_bullet_group.empty()

        # Рисуем задний фон
        lives_label = main_font.render(f'Здоровье: {player.lives}', True, (255, 255, 255))
        level_label = main_font.render(f'Счёт: {player.score}', True, (255, 255, 255))

        for bg_x in range(0, width, bg.get_width()):
            for bg_y in range(0, height, bg.get_height()):
                screen.blit(bg, (bg_x, bg_y))

                screen.blit(lives_label, (10, 10))
                screen.blit(level_label, (width - lives_label.get_width() - 10, 10))

        # Двигаем и рисуем корабль игрока
        player_group.update()
        player_group.draw(screen)

        # Рисуем урон если по игроку ударили
        player.draw_damage()

        # двигаем и рисуем снаряд
        bullet_group.update()
        enemy_bullet_group.update()

        # Создаём доп. корабли каждую 45-ю итерацию игрового цикла
        if loop_ctr == 45:
            create_suicide_ship()
            # Обновляем счётчик
            loop_ctr = 0

        if loop_ctr_2 == 300:
            s_ship_x = random.randint(50, width - 50)
            s_ship_y = 0

            shootin_ship = EnemyShooting(s_ship_x, s_ship_y)
            enemy_shooting_group.add(shootin_ship)
            loop_ctr_2 = 0

        if loop_ctr_3 == 1200:
            create_medkit()
            # Обновляем счётчик
            loop_ctr_3 = 0

        # Рисуем и двигаем корабли
        enemy_group.update()
        enemy_group.draw(screen)

        enemy_shooting_group.update()
        enemy_shooting_group.draw(screen)

        medkit_group.update()
        medkit_group.draw(screen)

        pygame.display.update()

        # Проверяем если игра окончена
        jameover = player.lives == 0
        while jameover:

            screen.fill((0, 0, 0))
            pygame.mixer.music.stop()

            clock.tick(fps)

            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()

            jameover_str = main_font_for_gameover.render(f'Игра окончена. Хотите сыграть снова? (д или н)', True,
                                                         (255, 255, 255))

            score = another_font.render(f'Ваш счёт: {player.score}!', True,
                                        (255, 255, 255))
            screen.blit(jameover_str, (100, 255))
            screen.blit(score, (150, 400))

            keys = pygame.key.get_pressed()
            if keys[K_l]:
                pygame.mixer.music.load(os.path.join('Игоря на pygame assets', 'Ratz.mp3'))
                pygame.mixer.music.play(-1)

                # Очищаем группы спрайтов
                player_group.empty()
                enemy_group.empty()
                bullet_group.empty()

                # Добавляем корабль
                create_suicide_ship()

                # Перезапускаем игрока
                player = Player(player_x, player_y)
                player_group.add(player)

                jameover = False
            elif keys[K_y]:
                running = False
                break
            pygame.display.update()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("black")

        OPTIONS_TEXT = get_font(45).render("Пока пусто...", True, "white")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(300, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(300, 460),
                              text_input="Назад", font=get_font(75), base_color="white", covering_color="red")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    postal.play()
                    main_menu()

        pygame.display.update()


def help():
    while True:
        HELP_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("black")

        HELP_TEXT = get_font(35).render("W, A, S, D - перемещение", True, "white")
        HELP_RECT = HELP_TEXT.get_rect(center=(330, 260))
        HELP_TEXT2 = get_font(35).render("SPACE - стрельба", True, "white")
        HELP_RECT2 = HELP_TEXT2.get_rect(center=(240, 320))
        screen.blit(HELP_TEXT, HELP_RECT)
        screen.blit(HELP_TEXT2, HELP_RECT2)

        HELP_BACK = Button(image=None, pos=(110, 630),
                           text_input="Назад", font=get_font(60), base_color="white", covering_color="red")

        HELP_BACK.changeColor(HELP_MOUSE_POS)
        HELP_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if HELP_BACK.checkForInput(HELP_MOUSE_POS):
                    postal.play()
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        for bg_x in range(0, width, bg.get_width()):
            for bg_y in range(0, height, bg.get_height()):
                screen.blit(bg, (bg_x, bg_y))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TITLE = get_font(60).render("SPACE INVADERS", True, "#b68f40")
        MENU_RECT = MENU_TITLE.get_rect(center=(350, 100))

        PLAY_BUTTON = Button(image=None, pos=(310, 250),
                             text_input="ИГРАТЬ", font=get_font(50), base_color="#d7fcd4", covering_color="red")
        OPTIONS_BUTTON = Button(image=None, pos=(310, 320),
                                text_input="НАСТРОЙКИ", font=get_font(50), base_color="#d7fcd4", covering_color="red")
        QUIT_BUTTON = Button(image=None, pos=(305, 445),
                             text_input="ВЫХОД", font=get_font(50), base_color="#d7fcd4", covering_color="red")
        HELP_BUTTON = Button(image=None, pos=(310, 385),
                             text_input="ПОМОЩЬ", font=get_font(50), base_color="#d7fcd4", covering_color="red")

        screen.blit(MENU_TITLE, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, HELP_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    postal.play()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(os.path.join('Игоря на pygame assets', 'Ratz.mp3'))
                    pygame.mixer.music.play(-1)
                    play()
                    sys.exit()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    postal.play()
                    options()
                if HELP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    postal.play()
                    help()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    postal.play()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
pygame.quit()