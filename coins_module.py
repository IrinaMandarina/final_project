import pygame
from pygame.draw import *
import random

class Coin(pygame.sprite.Sprite):

    def __init__(self, screen, x, y, platform_host):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.x = x
        self.y = y
        self.time_to_delete = random.randint(300, 450)
        self.platform_host = platform_host
        self.rect = pygame.Rect((x, y, 6, 6))

    def draw(self):
        circle(self.screen, (250, 210, 1), (self.x, self.y), 12)
        circle(self.screen, (255, 215, 0), (self.x, self.y), 10)

def generator_cn(screen,platforms,coins):
    for i in platforms:
        if random.randint(1, 10000) > 9990 and i.have_a_coin == False:
            coins.append(Coin(screen, i.x + random.randint(12, i.l) - 12, i.y - 27,
                              i))  # ставит монетку на платформу в рандомном месте(из у вычитаеться 27 чтобы была не в платформе)
            i.have_a_coin = True

def drawing_and_removing_coins(screen,platforms,coins,hero_list):
    generator_cn(screen,platforms,coins)
    for i in coins:
        i.draw()
        i.time_to_delete -= 1
    for p in range(len(coins)):
        for i in coins:
            if i.time_to_delete < 0:
                i.platform_host.have_a_coin = False
                coins.remove(i)
                break
    for p in range(len(coins)):
        for temp_hero in hero_list:
            for i in coins:
                if i.rect.colliderect(temp_hero.rect):
                    temp_hero.score += 1
                    i.platform_host.have_a_coin = False
                    coins.remove(i)
                    break
