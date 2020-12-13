import pygame
from pygame.draw import *
import math
import random

pygame.init()
width = 1000  # ширина окна
heigth = 750  # высота окна
g = 1  # ускорение свободного падения


class Portals(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, orientation, link):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.x = x
        self.y = y
        self.timer_image_portal = 0
        self.timer_image_portal_temp = random.randint(0, 11)
        self.images = [[
            pygame.transform.scale(pygame.image.load('blueportal1.png'), (79, 100)),
            pygame.transform.scale(pygame.image.load('blueportal2.png'), (79, 100)),
            pygame.transform.scale(pygame.image.load('blueportal3.png'), (79, 100)),
            pygame.transform.scale(pygame.image.load('blueportal4.png'), (79, 100))],
            [
                pygame.transform.scale(pygame.image.load('redportal1.png'), (79, 100)),
                pygame.transform.scale(pygame.image.load('redportal2.png'), (79, 100)),
                pygame.transform.scale(pygame.image.load('redportal3.png'), (79, 100)),
                pygame.transform.scale(pygame.image.load('redportal4.png'), (79, 100))],
            [
                pygame.transform.scale(pygame.image.load('yellowprotal1.png'), (79, 100)),
                pygame.transform.scale(pygame.image.load('yellowportal2.png'), (79, 100)),
                pygame.transform.scale(pygame.image.load('yellowportal3.png'), (79, 100)),
                pygame.transform.scale(pygame.image.load('yellowportal4.png'), (79, 100))
            ]]
        self.orientation = orientation  # определяет оринтацию портала вправо или влево True-влево,False-вправо
        self.link = link  # определяет "частоту портала" порталы с одинаковой частотой телепортируют друг к другу частоты. 0 1 2 соответсвенно синий красный желтый порталы
        self.rect = self.images[self.link][0].get_rect()
        self.rect.center = (self.x + 40, self.y + 50)  # просто rect

    def draw(self):  # отрисовка портала
        if self.orientation:
            self.images[self.link][self.timer_image_portal].set_colorkey((255, 255, 255))
            screen.blit(self.images[self.link][self.timer_image_portal], (self.x, self.y))
        else:
            image = pygame.transform.flip(self.images[self.link][self.timer_image_portal], True, False)
            image.set_colorkey((255, 255, 255))
            screen.blit(image, (self.x, self.y))
        self.timer_image_portal_temp += 1
        if self.timer_image_portal_temp > 3:
            self.timer_image_portal = 1

        if self.timer_image_portal_temp > 6:
            self.timer_image_portal = 2

        if self.timer_image_portal_temp > 9:
            self.timer_image_portal = 3

        if self.timer_image_portal_temp > 12:
            self.timer_image_portal = 0
            self.timer_image_portal_temp = 0


class Guns(pygame.sprite.Sprite):
    def __init__(self, screen, owner,
                 gun_type, image):  # тут под owner имееться в виду тот кто держит пушку нужен для координат если
        # если будет несколько игроков надо указать игрока если конечно player.x даст координату игрока
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.owner = owner
        self.gun_type = gun_type
        self.image = image

    def draw(self):
        if self.owner.m == -1:
            surf = pygame.transform.flip(self.image, True, False)
            surf.set_colorkey((255, 255, 255))
            screen.blit(surf, (self.owner.x - 30, self.owner.y + 20))
        else:
            self.image.set_colorkey((255, 255, 255))
            screen.blit(self.image, (self.owner.x + 30, self.owner.y + 20))

    def vistrel(self):
        bullets.append(
            Bullets(self.screen, self.owner.x + self.owner.m * 60, self.owner.y + 30, 20 * self.owner.m, 0,
                    self.owner, self.gun_type, 0))


class Bullets(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, vx, vy, owner, bullet_type, bullet_time_life):
        # x,y,vx,vy-стандарнто,owner-тот кто выстрелил чтобы в конце пуля не убила стрелявшего
        # bullet_type-тип пули(вдруг будут еще) bullet_time_life-просто таймер(мб время жизни пули должно пригодиться)
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.images = [pygame.transform.scale(pygame.image.load('bullet1.png'), (20, 20))]
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.owner = owner
        self.bullet_type = bullet_type
        self.bullet_time_life = bullet_time_life
        self.rect = self.images[self.bullet_type].get_rect()

    def move(self, platforms, bullet):
        k = False  # исчезновение пули при взаимодействии с платформой
        for platform in platforms:
            if pygame.sprite.collide_rect(platform, bullet):
                k = True
        self.x += self.vx
        self.y += self.vy
        self.bullet_time_life -= 1
        return k

    def draw(self):  # тут ничего интересного просто отрисовка пули (поворот изображения и тп)
        angle = math.atan2(-self.vy, self.vx)
        image = pygame.transform.rotate(self.images[self.bullet_type], angle)
        image = self.images[self.bullet_type]
        image.set_colorkey((0, 0, 0))
        image = pygame.transform.rotate(image, (angle / 3.14) * 180)
        screen.blit(image, (self.x, self.y))
        self.rect.center = (self.x, self.y)


class Coin(pygame.sprite.Sprite):

    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.x = x
        self.y = y

    def draw(self):
        circle(self.screen, (250, 210, 1), self.x, self.y, 12)
        circle(self.screen, (255, 215, 0), self.x, self.y, 10)


class Hero(pygame.sprite.Sprite):

    def __init__(self, screen, x, y, dx=0, dy=0):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.dx = dx
        self.y = y
        self.dy = dy
        self.screen = screen
        self.m = 1
        self.n = 0
        self.rect = pygame.Rect(self.x, self.y, 80, 100)
        self.time = 0
        self.images = []
        self.health = 100
        self.score = 0

    def draw(self):
        if self.dx != 0 and timer % 5 == 0:
            self.n = (self.n + 1) % len(self.images)
        if self.m == -1:
            image = pygame.transform.flip(self.images[self.n], True, False)
            image.set_colorkey((255, 255, 255))
            screen.blit(image, (self.x, self.y))
        else:
            self.images[self.n].set_colorkey((255, 255, 255))
            screen.blit(self.images[self.n], (self.x, self.y))
        self.rect = pygame.Rect(self.x, self.y, 80, 100)
        self.time += 1


class Button:
    def __init__(self, screen, x, y, color, name):
        self.screen = screen
        self.x = x
        self.y = y
        self.name = name
        f = pygame.font.Font(None, 36)
        self.w_x, self.w_y = f.size(self.name)
        self.color = color
        self.click = False

    def draw(self):
        rect(self.screen, self.color, (self.x, self.y, self.w_x + 10, self.w_y + 10))
        f = pygame.font.Font(None, 36)
        text = f.render(self.name, 1, (92, 73, 120))
        self.screen.blit(text, (self.x + 5, self.y + 5))

    def hitting(self, x_m, y_m):
        if self.x <= x_m <= self.x + self.w_x + 10 and self.y <= y_m <= self.y + self.w_y + 10:
            self.click = True


class Image_button:
    def __init__(self, screen, x, y, image, name):
        self.screen = screen
        self.x = x
        self.y = y
        self.name = name
        f = pygame.font.Font(None, 36)
        self.w_x, self.w_y = f.size(self.name)
        self.image = image
        self.click = False

    def draw(self):
        self.image[0].set_colorkey((255, 255, 255))
        if self.click:
            rect(self.screen, (200, 162, 200), (self.x - 3, self.y - 3, 86, 106))
        screen.blit(self.image[0], (self.x, self.y))
        f = pygame.font.Font(None, 36)
        text = f.render(self.name, 1, (0, 0, 0))
        self.screen.blit(text, (self.x + 40 - int(self.w_x / 2), self.y + 110))

    def hitting(self, x_m, y_m, ch):
        if self.x <= x_m <= self.x + 80 and self.y <= y_m <= self.y + 100:
            if not self.click:
                self.click = True
            else:
                self.click = False
        else:
            if ch:
                self.click = False

    def check(self, x_m, y_m):
        if self.x <= x_m <= self.x + 80 and self.y <= y_m <= self.y + 100:
            return True
        else:
            return False


class Platform(pygame.sprite.Sprite):

    def __init__(self, screen, x, y, l):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.l = l
        self.screen = screen
        self.rect = pygame.Rect(self.x, self.y - 15, self.l, 30)

    def draw(self):
        rect(self.screen, (194, 120, 16), (self.x, self.y - 15, self.l, 30), border_bottom_left_radius=14,
             border_bottom_right_radius=14)
        points = [(self.x, self.y - 15), (self.x, self.y)]
        k = 1
        for i in range(10, self.l, 10):
            points.append((self.x + i, self.y - k * 5))
            k *= (-1)
        points.append((self.x + self.l, self.y))
        points.append((self.x + self.l, self.y - 15))
        polygon(self.screen, (80, 180, 89), points)


def move(hero, platforms, k):
    m = False
    for platform in platforms:
        if (
                platform.x - 50 <= hero.x <= platform.x + platform.l - 30 or platform.x - 50 <= hero.x + hero.dx <= platform.x + platform.l - 30) and hero.y + hero.dy + 100 >= platform.y - 15 >= hero.y + 100 and hero.dy >= 0:
            m = True
            hero.y = platform.y - 115
    if hero.y + hero.dy + 100 >= heigth >= hero.y + 100 and not m:
        hero.y = heigth - 100
        hero.health = 0
        m = True
    if m:
        k = True
    else:
        k = False
    if k:
        if hero.dy < 0:
            hero.y += hero.dy
            hero.dy += g
        else:
            hero.dy = 0
    if not k and hero.y <= heigth - 100:
        hero.y += hero.dy
        hero.dy += g
    if hero.x < 0 or hero.x + 80 > width:
        if hero.x < 0:
            hero.x = 0
            hero.dx = 0
        if hero.x + 80 > width:
            hero.x = width - 80
            hero.dx = 0
    else:
        hero.x += hero.dx
    return k


def generator_pl():
    level = (670, 520, 370, 220)  # уровни на которых нужно сделать платформы
    jump_distance = 150  # длинна прыжка
    min_length = 200  # минимальная длина платформы
    max_length = 400  # максимальная длина платформы
    for i in level:
        x_nachala = 0
        while x_nachala < width + 5:  # проверка на не выход за экран
            length = random.randint(min_length, max_length)
            platforms.append(Platform(screen, x_nachala, i, length))
            x_nachala += (length + jump_distance)


def zastavka():
    image = pygame.image.load('zastava4.jpg')
    image = pygame.transform.scale(image, (width, heigth))
    screen.blit(image, (0, 0))
    play.draw()
    choose_hero.draw()


def dif_heroes():
    image = pygame.image.load('zastava4.jpg')
    image = pygame.transform.scale(image, (width, heigth))
    image.set_alpha(100)
    screen.blit(image, (0, 0))
    f = pygame.font.Font(None, 36)
    text = f.render('Player A', 1, (180, 0, 0))
    screen.blit(text, (200, 30))
    text = f.render('Player B', 1, (180, 0, 0))
    screen.blit(text, (700, 50))
    for b in image_buttons_b:
        b.draw()
    for b in image_buttons_a:
        b.draw()
    menu.draw()


def transpos(object):  # телепортация через портал объекта
    for start_portal in portals:
        if start_portal.rect.colliderect(object.rect):  # проверка на пересечение границ спрайтов(пересечение грацниц)
            for end_portal in portals:
                if (start_portal != end_portal) and (
                        start_portal.link == end_portal.link):  # проверяет то, что разные порталы, но одинаковая
                    # связь(цвет)
                    object.y = object.y - object.rect.bottom + end_portal.rect.bottom
                    if end_portal.orientation:
                        object.x = end_portal.x - object.rect[
                            2] - 10  # вычитаем 10, чтобы было время на реагирование после телерортации
                    else:
                        object.x = end_portal.x + object.rect[2] + 10  # -||-
                    if (start_portal.orientation != end_portal.orientation) and (type(object) == Bullets):
                        object.vx = int((-1) * object.vx)


FPS = 30
screen = pygame.display.set_mode((width, heigth))

pygame.display.update()
clock = pygame.time.Clock()
finished = False
timer = 0
k_a = False  # индикатор взаимодействия с платформой
k_b = False
platforms = []  # список платформ
portals = []  # список порталов
bullets = []  # список пуль
image_buttons_a = []
image_buttons_b = []
images = [[], [], []]

images[0].append(pygame.transform.scale(pygame.image.load('1hero.png'), (80, 100)))
images[0].append(pygame.transform.scale(pygame.image.load('2hero.png'), (80, 100)))
images[0].append(pygame.transform.scale(pygame.image.load('3hero.png'), (80, 100)))
images[0].append(pygame.transform.scale(pygame.image.load('4hero.png'), (80, 100)))

images[1].append(pygame.transform.scale(pygame.image.load('1hero1.png'), (80, 100)))
images[1].append(pygame.transform.scale(pygame.image.load('2hero1.png'), (80, 100)))
images[1].append(pygame.transform.scale(pygame.image.load('3hero1.png'), (80, 100)))
images[1].append(pygame.transform.scale(pygame.image.load('4hero1.png'), (80, 100)))

images[2].append(pygame.transform.scale(pygame.image.load('1hero2.png'), (80, 100)))
images[2].append(pygame.transform.scale(pygame.image.load('2hero2.png'), (80, 100)))
images[2].append(pygame.transform.scale(pygame.image.load('3hero2.png'), (80, 100)))
images[2].append(pygame.transform.scale(pygame.image.load('4hero2.png'), (80, 100)))

play = Button(screen, 480, 250, (219, 195, 219), 'Play!')  # кнопка начала игры
choose_hero = Button(screen, 410, 200, (219, 195, 219), 'Choose your hero!')  # кнопка для выбора героя
menu = Button(screen, 920, 10, (219, 195, 219), 'Menu')  # кнопка выхода в меню
restart = Button(screen, 800, 10, (219, 195, 219), 'Restart')  # кнопка выхода в меню
menu.click = True
image_buttons_a.append(Image_button(screen, 30, 80, images[0], 'Worker'))
image_buttons_b.append(Image_button(screen, 530, 80, images[0], 'Worker'))
image_buttons_a.append(Image_button(screen, 130, 80, images[1], 'Elf'))
image_buttons_b.append(Image_button(screen, 630, 80, images[1], 'Elf'))
image_buttons_a.append(Image_button(screen, 230, 80, images[2], 'Fairy'))
image_buttons_b.append(Image_button(screen, 730, 80, images[2], 'Fairy'))

hero_a = Hero(screen, 0, 35)  # инициализация игрока A (справа)
hero_a.images = images[0]
hero_b = Hero(screen, 950, 35)  # инициализация игрока В (слева)
hero_b.images = images[0]

im_gun_1 = pygame.transform.scale(pygame.image.load('gun1.png'), (80, 45))
im_gun_2 = pygame.transform.scale(pygame.image.load('gun4.png'), (80, 45))
im_gun_3 = pygame.transform.scale(pygame.image.load('gun3.png'), (80, 45))

gun_a = Guns(screen, hero_a, 0, im_gun_2)  # инициализация ружья
gun_b = Guns(screen, hero_b, 0, im_gun_1)

generator_pl()  # генерация платформ

while not finished:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            (x_m, y_m) = pygame.mouse.get_pos()
            if play.click:
                restart.hitting(x_m, y_m)
                menu.hitting(x_m, y_m)
                if menu.click:
                    play.click = False
            if choose_hero.click:
                a_c = False
                b_c = False
                menu.hitting(x_m, y_m)
                if menu.click:
                    choose_hero.click = False
                for b in image_buttons_a:
                    if b.check(x_m, y_m):
                        a_c = True
                for b in image_buttons_b:
                    if b.check(x_m, y_m):
                        b_c = True
                for b in image_buttons_a:
                    b.hitting(x_m, y_m, a_c)
                    if b.click:
                        hero_a.images = b.image
                for b in image_buttons_b:
                    b.hitting(x_m, y_m, b_c)
                    if b.click:
                        hero_b.images = b.image
            else:
                play.hitting(x_m, y_m)
                if play.click:
                    menu.click = False
                choose_hero.hitting(x_m, y_m)
                if choose_hero.click:
                    menu.click = False
        if play.click:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    gun_a.vistrel()
                if event.key == pygame.K_DOWN:
                    gun_b.vistrel()
                if event.key == pygame.K_LEFT:
                    hero_b.dx = -5
                    hero_b.m = (-1)
                if event.key == pygame.K_RIGHT:
                    hero_b.dx = 5
                    hero_b.m = 1
                if event.key == pygame.K_UP and k_b:
                    hero_b.dy = -17
                if event.key == pygame.K_a:
                    hero_a.dx = -5
                    hero_a.m = (-1)
                if event.key == pygame.K_d:
                    hero_a.dx = 5
                    hero_a.m = 1
                if event.key == pygame.K_w and k_a:
                    hero_a.dy = -17
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    hero_b.dx = 0
                if event.key == pygame.K_RIGHT:
                    hero_b.dx = 0
                if event.key == pygame.K_a:
                    hero_a.dx = 0
                if event.key == pygame.K_d:
                    hero_a.dx = 0

    if play.click:
        if restart.click:
            timer = 0
            hero_a.score = 0
            hero_b.score = 0
            hero_a.health = 100
            hero_b.health = 100
            hero_a.x = 0
            hero_b.y = 35
            hero_b.x = 950
            hero_a.y = 35
            platforms = []
            generator_pl()
            restart.click = False
        if hero_a.health > 0 and hero_b.health > 0:
            screen.fill((255, 255, 255))
            image = pygame.image.load('forest1.jpg')
            image = pygame.transform.scale(image, (width, heigth))
            image.set_alpha(200)
            screen.blit(image, (0, 0))

            k_a = move(hero_a, platforms, k_a)  # движение героя A
            k_b = move(hero_b, platforms, k_b)  # движение героя B

            for i in portals:  # отрисовка порталов
                i.draw()

            for i in platforms:  # отрисовка платформ
                i.draw()

            for i in bullets:  # движение и отрисовка пуль
                i.draw()
                k = i.move(platforms, i)  # исчезновение пули при взаимодействии с платформой
                if k:
                    bullets.remove(i)
                # if i.timer<0: доделать?

            hero_a.draw()  # отрисовка героя
            hero_b.draw()

            gun_a.draw()  # отрисовка ружья
            gun_b.draw()

            f = pygame.font.Font(None, 36)
            text = f.render('Your game time (sec):' + str(round(timer / FPS, 1)), 1, (180, 0, 0))
            screen.blit(text, (400, 30))

            transpos(hero_a)  # проверка на возможность телепортации героя и телепортация в случае если он зашел в
            # портал
            for i in bullets:
                transpos(i)  # проверка на возможность телепортации всех пуль

            timer += 1

            menu.draw()
            restart.draw()
        else:
            screen.fill((0, 0, 0))
            f = pygame.font.Font(None, 36)
            text = f.render('Game over!', 1, (180, 0, 0))
            screen.blit(text, (400, 100))
            text = f.render('Player A score:' + str(hero_a.score), 1, (180, 0, 0))
            screen.blit(text, (250, 130))
            text = f.render('Player B score:' + str(hero_a.score), 1, (180, 0, 0))
            screen.blit(text, (550, 130))
            text = f.render('Your game time (sec):' + str(round(timer / FPS, 1)), 1, (180, 0, 0))
            screen.blit(text, (350, 160))
            restart.draw()

    else:
        if choose_hero.click:
            menu.click = False
            dif_heroes()
        if menu.click:
            play.click = False
            zastavka()

    pygame.display.update()

pygame.quit()

'''if __name__ == '__main__':
    main()'''
