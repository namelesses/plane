# -*- coding: utf-8 -*-
import pygame
from random import randint
from abs_path import resource_path
# ====================定义超级炸弹补给包====================


class BombSupply(pygame.sprite.Sprite):

    def __init__(self, bg_size):
        super(BombSupply, self).__init__()

        self.image = pygame.image.load(resource_path(r'resources\ufo2.png'))
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 5
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.bottom = randint(
            0, self.width - self.rect.width), -100

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = randint(
            0, self.width - self.rect.width), -100

# ====================定义超级子弹补给包====================


class BulletSupply(pygame.sprite.Sprite):

    def __init__(self, bg_size):
        super(BulletSupply, self).__init__()

        self.image = pygame.image.load(resource_path(r'resources\ufo1.png'))
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.bottom = randint(
            0, self.width - self.rect.width), -100
        self.speed = 5
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = randint(
            0, self.width - self.rect.width), -100
