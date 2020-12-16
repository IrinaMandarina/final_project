import pygame
from pygame.draw import *
import random
class Platform(pygame.sprite.Sprite):

    def __init__(self, screen, x, y, l):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.l = l
        self.screen = screen
        self.rect = pygame.Rect(self.x, self.y - 15, self.l, 30)
        self.have_a_coin = False

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
def generator_pl(screen,width,platforms):
    level = (670, 520, 370, 220)  # уровни на которых нужно сделать платформы
    jump_distance = 150  # длинна прыжка
    min_length = 200  # минимальная длина платформы
    max_length = 400  # максимальная длина платформы
    for i in level:
        x_nachala = 0
        while x_nachala < width + 5:  # проверка на не выход за экран
            length = random.randint(min_length, max_length)
            if width < x_nachala + length:
                length = width - x_nachala
            platforms.append(Platform(screen, x_nachala, i, length))
            x_nachala += (length + jump_distance)