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
        self.image =pygame.transform.scale(pygame.image.load('coin.png'), (30, 30))

    def draw(self):
        self.image.set_colorkey((255, 255, 255))
        self.screen.blit(self.image, (self.x-17, self.y-20))

def generator_cn(screen,platforms,coins,timer_monetok):
    i=platforms[random.randint(1,len(platforms))-1]
    if (timer_monetok<0) and i.have_a_coin == False:
        coins.append(Coin(screen, i.x + random.randint(0,int(i.l/2)), i.y - 27,i))  # ставит монетку на платформу в рандомном месте(из у вычитаеться 27 чтобы была не в платформе)
        i.have_a_coin = True
        timer_monetok=100
    return timer_monetok

def drawing_and_removing_coins(coins,hero_list):
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
