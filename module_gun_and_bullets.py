import pygame
from pygame.draw import *
import math
import random
import coins_module
import platforms_module
class Guns(pygame.sprite.Sprite):
    def __init__(self, screen, owner,
                 gun_type, image):  # тут под owner имееться в виду тот кто держит пушку нужен для координат если
        # если будет несколько игроков надо указать игрока если конечно player.x даст координату игрока
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.owner = owner
        self.gun_type = gun_type
        self.image = image
        self.sound_vistrel = pygame.mixer.Sound('vistrel.wav')

    def draw(self):
        if self.owner.m == -1:
            surf = pygame.transform.flip(self.image, True, False)
            surf.set_colorkey((255, 255, 255))
            self.screen.blit(surf, (self.owner.x - 30, self.owner.y + 20))
        else:
            self.image.set_colorkey((255, 255, 255))
            self.screen.blit(self.image, (self.owner.x + 30, self.owner.y + 20))

    def vistrel(self,bullets):
        self.sound_vistrel.play()
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
        self.screen.blit(image, (self.x, self.y))
        self.rect.center = (self.x, self.y)

