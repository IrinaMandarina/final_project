import pygame
from pygame.draw import *
import random
import coins_module
import platforms_module
import module_gun_and_bullets
import portals_module


class Medkit(pygame.sprite.Sprite):

    def __init__(self, screen, platforms, width):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        nomer_plt = random.randint(0, len(platforms) - 1)
        self.time_to_delete = random.randint(300, 450)
        while platforms[nomer_plt].x + platforms[nomer_plt].l > width:
            nomer_plt = random.randint(0, len(platforms) - 1)
        self.x = platforms[nomer_plt].x + int(platforms[nomer_plt].l / 2)
        self.y = platforms[nomer_plt].y - 30
        if platforms[nomer_plt].x + platforms[nomer_plt].l > width:
            self.time_to_delete = -1
        self.rect = pygame.Rect((self.x, self.y, 6, 6))
        self.image = pygame.transform.scale(pygame.image.load('heal.png'), (30, 30))

    def draw(self):
        self.image.set_colorkey((255, 255, 255))
        self.screen.blit(self.image, (self.x - 17, self.y - 20))

    def waiting(self, hero):
        if self.rect.colliderect(hero.rect):
            hero.health = 100
            self.time_to_delete = -1
