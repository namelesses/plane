# -*- coding: utf-8 -*-
import pygame
from random import randint
from abs_path import resource_path


class SmallEnemy(pygame.sprite.Sprite):

    def __init__(self, bg_size):
        super(SmallEnemy, self).__init__()

        self.image = pygame.image.load(
            resource_path(r"resources\enemy1.png"))  # 加载敌方飞机图片
        self.rect = self.image.get_rect()  # 获得敌方飞机的位置
        self.width, self.height = bg_size[0], bg_size[1]  # 本地化背景图片位置
        self.speed = 2  # 设置敌机的速度
        # 获取飞机图像的掩膜用以更加精确的碰撞检测:
        self.mask = pygame.mask.from_surface(self.image)

        self.destroy_images = []  # 加载飞机损毁图片
        self.destroy_images.extend([pygame.image.load(resource_path(
            r"resources\enemy1_down1.png")),
            pygame.image.load(resource_path(
                r"resources\enemy1_down2.png")),
            pygame.image.load(resource_path(
                r"resources\enemy1_down3.png")),
            pygame.image.load(resource_path(
                r"resources\enemy1_down4.png"))])
        self.reset()

    def move(self):  # 定义敌机的移动函数
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):  # 重置敌机位置
        self.rect.left, self.rect.top = (randint(5, self.width - self.rect.width - 5),  # 定义敌机出现的位置
                                         randint(-5 * self.rect.height, -5)
                                         )  # 保证敌机不会在程序已开始就立即出现
        self.active = True  # 设置飞机当前的存着属性,True表示飞机正常飞行


class MidEnemy(pygame.sprite.Sprite):
    energy = 5  # 总血量

    def __init__(self, bg_size):
        super(MidEnemy, self).__init__()

        self.image = pygame.image.load(
            resource_path(r"resources\enemy2.png"))  # 加载敌方飞机图片
        self.image_hit = pygame.image.load(
            resource_path(r"resources\enemy2_hit.png"))
        self.rect = self.image.get_rect()  # 获得敌方飞机的位置
        self.width, self.height = bg_size[0], bg_size[1]  # 本地化背景图片位置
        self.speed = 1  # 设置敌机的速度
        # 获取飞机图像的掩膜用以更加精确的碰撞检测:
        self.mask = pygame.mask.from_surface(self.image)
        self.destroy_images = []  # 加载飞机损毁图片
        self.destroy_images.extend([pygame.image.load(resource_path(
            r"resources\enemy2_down1.png")),
            pygame.image.load(resource_path(
                r"resources\enemy2_down2.png")),
            pygame.image.load(resource_path(
                r"resources\enemy2_down3.png")),
            pygame.image.load(resource_path(
                r"resources\enemy2_down4.png"))])
        self.reset()

    def move(self):  # 定义敌机的移动函数
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):  # 重置敌机位置
        self.rect.left, self.rect.top = (randint(0, self.width - self.rect.width),  # 定义敌机出现的位置
                                         randint(-10 * self.rect.height,
                                                 -self.rect.height)
                                         )  # # 保证一开始不会有中型敌机出现
        self.active = True  # 设置飞机当前的存着属性,True表示飞机正常飞行
        self.energy = MidEnemy.energy  # 当前血量
        self.hit = False


class BigEnemy(pygame.sprite.Sprite):
    energy = 15  # 总血量

    def __init__(self, bg_size):
        super(BigEnemy, self).__init__()

        # 加载敌方飞机图片，其中大型飞机有帧切换的特效:
        self.image1 = pygame.image.load(
            resource_path(r"resources\enemy3_n1.png"))
        self.image2 = pygame.image.load(
            resource_path(r"resources\enemy3_n2.png"))
        self.image_hit = pygame.image.load(
            resource_path(r"resources\enemy3_hit.png"))
        self.rect = self.image1.get_rect()  # 获得敌方飞机的位置
        self.width, self.height = bg_size[0], bg_size[1]  # 本地化背景图片位置
        self.speed = 2  # 设置敌机的速度
        # 获取飞机图像的掩膜用以更加精确的碰撞检测:
        self.mask = pygame.mask.from_surface(self.image1)
        self.destroy_images = []  # 加载飞机损毁图片
        self.destroy_images.extend([pygame.image.load(resource_path(
            r"resources\enemy3_down1.png")),
            pygame.image.load(resource_path(
                r"resources\enemy3_down2.png")),
            pygame.image.load(resource_path(
                r"resources\enemy3_down3.png")),
            pygame.image.load(resource_path(
                r"resources\enemy3_down4.png")),
            pygame.image.load(resource_path(
                r"resources\enemy3_down5.png")),
            pygame.image.load(resource_path(
                r"resources\enemy3_down6.png"))])
        self.reset()

    def move(self):  # 定义敌机的移动函数
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):  # 重置敌机位置
        self.rect.left, self.rect.top = (randint(0, self.width - self.rect.width),  # 定义敌机出现的位置
                                         randint(-15 * self.rect.height, - \
                                                 5 * self.rect.height)
                                         )  # 保证敌机过一段时间才会出现
        self.active = True  # 设置飞机当前的存着属性,True表示飞机正常飞行
        self.energy = BigEnemy.energy  # 当前血量
        self.hit = False
