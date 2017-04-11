# -*- coding: utf-8 -*-
import pygame
from abs_path import resource_path


class Bullet1(pygame.sprite.Sprite):

    def __init__(self):
        super(Bullet1, self).__init__()

        self.image = pygame.image.load(resource_path(r'resources\bullet1.png'))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.active = False

    def move(self):
        if self.rect.top < 0:
            self.active = False
        else:
            self.rect.top -= self.speed

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.speed = 12
        self.active = True


class Bullet2(pygame.sprite.Sprite):

    def __init__(self):
        super(Bullet2, self).__init__()
        self.image = pygame.image.load(resource_path(r'resources\bullet2.png'))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.active = False

    def move(self):
        if self.rect.top < 0:
            self.active = False
        else:
            self.rect.top -= self.speed

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.speed = 14
        self.active = True
