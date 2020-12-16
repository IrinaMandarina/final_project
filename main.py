import pygame
from pygame.draw import *
import random
import coins_module
import platforms_module
import module_gun_and_bullets
import portals_module
import heal_module
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
width = 1000  # ширина окна
heigth = 750  # высота окна
g = 1  # ускорение свободного падения



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
        text = f.render(self.name, True, (92, 73, 120))
        self.screen.blit(text, (self.x + 5, self.y + 5))

    def hitting(self, x_m, y_m):
        if self.x <= x_m <= self.x + self.w_x + 10 and self.y <= y_m <= self.y + self.w_y + 10:
            self.click = True
            click.play()


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
        text = f.render(self.name, True, (0, 0, 0))
        self.screen.blit(text, (self.x + 40 - int(self.w_x / 2), self.y + 110))

    def hitting(self, x_m, y_m, ch):
        if self.x <= x_m <= self.x + 80 and self.y <= y_m <= self.y + 100:
            click.play()
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




def move(hero, platforms, k):
    m = False
    for platform in platforms:
        if (
                platform.x - 50 <= hero.x <= platform.x + platform.l - 30 or platform.x - 50 <= hero.x + hero.dx <=
                platform.x + platform.l - 30) and \
                hero.y + hero.dy + 100 >= platform.y - 15 >= hero.y + 100 and hero.dy >= 0:
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




def zastavka(music):
    if not music:
        pygame.mixer.stop()
        pygame.mixer.music.load('zastavka.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
        click.play()
        music = True
    image = pygame.image.load('zastava4.jpg')
    image = pygame.transform.scale(image, (width, heigth))
    screen.blit(image, (0, 0))
    play.draw()
    choose_hero.draw()
    rules.draw()
    return music


def dif_heroes():
    image = pygame.image.load('zastava4.jpg')
    image = pygame.transform.scale(image, (width, heigth))
    image.set_alpha(100)
    screen.blit(image, (0, 0))
    f = pygame.font.Font(None, 36)
    text = f.render('Player A', True, (180, 0, 0))
    screen.blit(text, (200, 30))
    text = f.render('Player B', True, (180, 0, 0))
    screen.blit(text, (700, 50))
    for b in image_buttons_b:
        b.draw()
    for b in image_buttons_a:
        b.draw()
    menu.draw()



def rules_t():
    image = pygame.image.load('zastava4.jpg')
    image = pygame.transform.scale(image, (width, heigth))
    image.set_alpha(100)
    screen.blit(image, (0, 0))
    f = pygame.font.Font(None, 36)
    text = f.render('Правила игры:', True, (180, 0, 0))
    screen.blit(text, (450, 20))
    text = f.render('Цель игры – уничтожить соперника и собрать побольше монет!', True, (0, 0, 0))
    screen.blit(text, (150, 55))
    f = pygame.font.Font(None, 24)
    text = f.render('Для управления игроком А используйте кнопки:', True, (0, 0, 0))
    screen.blit(text, (50, 100))
    text = f.render('Для управления игроком B используйте кнопки:', True, (0, 0, 0))
    screen.blit(text, (550, 100))
    text = f.render('A - движение налево', True, (0, 0, 0))
    screen.blit(text, (50, 115))
    text = f.render('D - движение направо', True, (0, 0, 0))
    screen.blit(text, (50, 130))
    text = f.render('W - прыжок', True, (0, 0, 0))
    screen.blit(text, (50, 145))
    text = f.render('S - выстрел', True, (0, 0, 0))
    screen.blit(text, (50, 160))
    text = f.render('<- - движение налево', True, (0, 0, 0))
    screen.blit(text, (550, 115))
    text = f.render('-> - движение направо', True, (0, 0, 0))
    screen.blit(text, (550, 130))
    text = f.render('PgUp - прыжок', True, (0, 0, 0))
    screen.blit(text, (550, 145))
    text = f.render('PgDn - выстрел', True, (0, 0, 0))
    screen.blit(text, (550, 160))
    f = pygame.font.Font(None, 36)
    text = f.render('При падении с платформы игрок умирает...', True, (0, 0, 0))
    screen.blit(text, (150, 190))
    menu.draw()


FPS = 30
screen = pygame.display.set_mode((width, heigth))

pygame.display.update()
clock = pygame.time.Clock()
finished = False
timer = 0
music = False
k_a = False  # индикатор взаимодействия с платформой
k_b = False
timer_monetok=-1
platforms = []  # список платформ
portals = []  # список порталов
bullets = []  # список пуль
coin = []  # список монеток
image_buttons_a = []
image_buttons_b = []
images = [[], [], []]
coins = []  # список монеток

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
rules = Button(screen, 475, 300, (219, 195, 219), 'Rules')  # кнопка правил
menu.click = True
image_buttons_a.append(Image_button(screen, 30, 80, images[0], 'Worker'))
image_buttons_b.append(Image_button(screen, 530, 80, images[0], 'Worker'))
image_buttons_a.append(Image_button(screen, 130, 80, images[1], 'Elf'))
image_buttons_b.append(Image_button(screen, 630, 80, images[1], 'Elf'))
image_buttons_a.append(Image_button(screen, 230, 80, images[2], 'Fairy'))
image_buttons_b.append(Image_button(screen, 730, 80, images[2], 'Fairy'))

platforms_module.generator_pl(screen,width,platforms)  # генерация платформ(важно чтобы было до инициализации игроков)

x_hero = platforms[0].x + int((platforms[0].l) * 0.5)
y_hero = platforms[0].y - 120
hero_a = Hero(screen, x_hero, y_hero)  # инициализация игрока A (справа)
hero_a.images = images[0]
nomer_platform = len(platforms) - 2
x_hero = platforms[nomer_platform].x + int((platforms[nomer_platform].l) * 0.5)
y_hero = platforms[nomer_platform].y - 120
hero_b = Hero(screen, x_hero, y_hero)  # инициализация игрока В (слева)
hero_b.images = images[0]

im_gun_1 = pygame.transform.scale(pygame.image.load('gun1.png'), (80, 45))
im_gun_2 = pygame.transform.scale(pygame.image.load('gun4.png'), (80, 45))
im_gun_3 = pygame.transform.scale(pygame.image.load('gun3.png'), (80, 45))
portals_module.generator_pr(platforms,portals,screen,width)

game_over = pygame.mixer.Sound('game_over_kr.wav')
click = pygame.mixer.Sound('click.wav')
coin = pygame.mixer.Sound('coin.wav')

gun_a = module_gun_and_bullets.Guns(screen, hero_a, 0, im_gun_2)  # инициализация ружья
gun_b = module_gun_and_bullets.Guns(screen, hero_b, 0, im_gun_1)

medkit=heal_module.Medkit(screen,platforms,width)

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
                    music = False
                    play.click = False
            elif choose_hero.click:
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
            elif rules.click:
                menu.hitting(x_m, y_m)
                if menu.click:
                    rules.click = False
            else:
                rules.hitting(x_m, y_m)
                if rules.click:
                    menu.click = False
                play.hitting(x_m, y_m)
                if play.click:
                    music = False
                    menu.click = False
                choose_hero.hitting(x_m, y_m)
                if choose_hero.click:
                    menu.click = False
        if play.click:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    gun_a.vistrel(bullets)
                if event.key == pygame.K_DOWN:
                    gun_b.vistrel(bullets)
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
            medkit=heal_module.Medkit(screen,platforms,width)
            coins=[]
            platforms = []
            bullets = []
            portals = []
            platforms_module.generator_pl(screen, width, platforms)
            portals_module.generator_pr(platforms,portals,screen,width)
            hero_a.score = 0
            hero_b.score = 0
            hero_a.health = 100
            hero_b.health = 100
            hero_a.x = platforms[0].x + int((platforms[0].l) * 0.5)
            hero_a.y = platforms[0].y - 120
            hero_b.y = platforms[len(platforms) - 1].y - 120
            hero_b.x = platforms[len(platforms) - 1].x + int((platforms[len(platforms) - 1].l) * 0.5)
            restart.click = False
            music = False
        if hero_a.health > 0 and hero_b.health > 0:
            if not music:
                pygame.mixer.stop()
                pygame.mixer.music.load('play.mp3')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.3)
                click.play()
                music = True
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
                if pygame.sprite.collide_rect(i, hero_a) and i.owner == hero_b:
                    bullets.remove(i)
                    hero_a.health -= 1
                if pygame.sprite.collide_rect(i, hero_b) and i.owner == hero_a:
                    bullets.remove(i)
                    hero_b.health -= 1
                k = i.move(platforms, i)  # исчезновение пули при взаимодействии с платформой
                if k:
                    bullets.remove(i)
                # if i.timer<0: доделать?

            hero_a.draw()  # отрисовка героя
            gun_a.draw()  # отрисовка ружья
            medkit.draw()
            hero_b.draw()
            gun_b.draw()
            medkit.waiting(hero_a)
            medkit.waiting(hero_b)
            if medkit.time_to_delete<0:
                medkit=heal_module.Medkit(screen,platforms,width)

            timer_monetok =coins_module.generator_cn(screen,platforms,coins,timer_monetok, coin) - 1
            coins_module.drawing_and_removing_coins(coins,[hero_a,hero_b], coin)  # это больше чем просто отрисовка !!  не надо писать как метод!!
            f = pygame.font.Font(None, 36)
            text = f.render('Hp A   ' + str(hero_a.health), True, (180, 0, 0))
            #  text = f.render('Your game time (sec):' + str(round(timer / FPS, 1)), 1, (180, 0, 0))
            screen.blit(text, (20, 20))
            text = f.render('Hp B   ' + str(hero_b.health), True, (180, 0, 0))
            screen.blit(text, (20, 45))
            text = f.render('Score A   ' + str(hero_a.score), True, (0, 0, 0))
            screen.blit(text, (170, 20))
            text = f.render('Score B   ' + str(hero_b.score), True, (0, 0, 0))
            screen.blit(text, (170, 45))
            portals_module.transpos(hero_a,portals)
            portals_module.transpos(hero_b,portals)
            # проверка на возможность телепортации героя и телепортация в случае, если он зашел в
            # портал
            for i in bullets:
                portals_module.transpos(i,portals)  # проверка на возможность телепортации всех пуль

            timer += 1

            menu.draw()
            restart.draw()
        else:
            if music:
                pygame.mixer.stop()
                pygame.mixer.music.load('konets.mp3')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.4)
                game_over.play()
                music = False
            screen.fill((0, 0, 0))
            f = pygame.font.Font(None, 36)
            text = f.render('Game over!', True, (180, 0, 0))
            screen.blit(text, (400, 100))
            text = f.render('Player A score:' + str(hero_a.score), True, (180, 0, 0))
            screen.blit(text, (250, 130))
            text = f.render('Player B score:' + str(hero_a.score), True, (180, 0, 0))
            screen.blit(text, (550, 130))
            text = f.render('Your game time (sec):' + str(round(timer / FPS, 1)), True, (180, 0, 0))
            screen.blit(text, (350, 160))
            restart.draw()

    else:
        if rules.click:
            menu.click = False
            rules_t()
        if choose_hero.click:
            menu.click = False
            dif_heroes()
        if menu.click:
            play.click = False
            rules.click = False
            music = zastavka(music)

    pygame.display.update()

pygame.quit()

'''if __name__ == '__main__':
    main()'''
