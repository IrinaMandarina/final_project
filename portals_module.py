import pygame
from pygame.draw import *
import random
import coins_module
import platforms_module
import module_gun_and_bullets
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
        self.link = link  # определяет "частоту портала" порталы с одинаковой частотой телепортируют друг к другу
        # частоты. 0 1 2 соответсвенно синий красный желтый порталы
        self.rect = self.images[self.link][0].get_rect()
        self.rect.center = (self.x + 40, self.y + 50)  # просто rect

    def draw(self):  # отрисовка портала
        if self.orientation:
            self.images[self.link][self.timer_image_portal].set_colorkey((255, 255, 255))
            self.screen.blit(self.images[self.link][self.timer_image_portal], (self.x, self.y))
        else:
            image = pygame.transform.flip(self.images[self.link][self.timer_image_portal], True, False)
            image.set_colorkey((255, 255, 255))
            self.screen.blit(image, (self.x, self.y))
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
def transpos(object,portals):  # телепортация через портал объекта
    for start_portal in portals:
        if start_portal.rect.colliderect(object.rect):  # проверка на пересечение границ спрайтов(пересечение грацниц)
            for end_portal in portals:
                if (start_portal != end_portal) and (
                        start_portal.link == end_portal.link):  # проверяет то, что разные порталы, но одинаковая
                    # связь(цвет)
                    object.y = object.y - start_portal.rect.bottom + end_portal.rect.bottom
                    if end_portal.orientation==True:
                        temp_k=-1
                    else:
                        temp_k=1
                    if end_portal.orientation:
                        object.x = end_portal.x - object.rect[
                            2] -20  # вычитаем 10, чтобы было время на реагирование после телерортации
                        print('-')
                    else:
                        object.x = end_portal.x + object.rect[2] +80  # -||-
                        print('+')
                    if type(object)==module_gun_and_bullets.Bullets:
                        object.vx=int((object.vx**2)**0.5)*temp_k
def generator_pr(platforms,portals,screen):
    for i in range(0,random.randint(0,2)):
        p=random.randint(0,len(platforms)-1)
        while platforms[p].have_a_portal==True:
            p=random.randint(0,len(platforms)-1)
        portals.append(Portals(screen,platforms[p].x+platforms[p].l/2,platforms[p].y-120,True,i))
        platforms[p].have_a_portal=True
        p = random.randint(0, len(platforms) - 1)

        while platforms[p].have_a_portal == True:
            p = random.randint(0, len(platforms) - 1)
        portals.append(Portals(screen, platforms[p].x + platforms[p].l/2, platforms[p].y-120, False, i))
        platforms[p].have_a_portal = True
