# -*- coding: utf-8 -*-
import pygame
import sys
from abs_path import resource_path


class Myplane(pygame.sprite.Sprite):

    def __init__(self, bg_size):
        super(Myplane, self).__init__()
        # pygame.sprite.Sprite.__init__(self)
        # 加载我方飞机图片，其中飞机有尾气喷射的特效
        self.image1 = pygame.image.load(resource_path(r"resources\hero1.png"))
        self.image2 = pygame.image.load(resource_path(r"resources\hero2.png"))
        self.rect = self.image1.get_rect()  # 得到当前我方飞机的位置
        self.width, self.height = bg_size[0], bg_size[1]  # 本地化背景图片的尺寸
        self.rect.left, self.rect.top = (
            self.width - self.rect.width) // 2, (self.height - self.rect.height - 60)  # 定义飞机初始化位置，底部预留60像素

        self.speed = 10  # 设置飞机移动速度
        self.active = True  # 设置飞机当前的存着属性,True表示飞机正常飞行
        self.invincible = False  # 飞机初始化时有三秒的无敌时间

        # 获取飞机图像的掩膜用以更加精确的碰撞检测:
        self.mask = pygame.mask.from_surface(self.image1)
        self.destroy_images = []  # 加载飞机损毁图片
        self.destroy_images.extend([pygame.image.load(resource_path(r"resources\hero_blowup_n1.png")),
                                    pygame.image.load(resource_path(
                                        r"resources\hero_blowup_n2.png")),
                                    pygame.image.load(resource_path(
                                        r"resources\hero_blowup_n3.png")),
                                    pygame.image.load(resource_path(r"resources\hero_blowup_n4.png"))])

    def move_up(self):  # 飞机向上移动的操作函数，其余移动函数方法类似
        if self.rect.top > 0:  # 如果飞机尚未移动出背景区域
            self.rect.top -= self.speed
        else:  # 若即将移动出背景区域，则及时纠正为背景边缘位置
            self.rect.top = 0

    def move_down(self):
        if self.rect.bottom < self.height - 60:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height - 60

    def move_left(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def move_right(self):
        if self.rect.right < self.width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.width

    def reset(self):
        self.rect.left, self.rect.top = (
            self.width - self.rect.width) // 2, (self.height - self.rect.height - 60)  # 定义飞机初始化位置，底部预留60像素
        self.active = True  # 设置飞机当前的存着属性,True表示飞机正常飞行
        self.invincible = True  # 飞机初始化时有三秒的无敌时间
