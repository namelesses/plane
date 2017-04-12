# -*- coding: utf-8 -*-
# ================导入模块================
import pygame
import json
import sys
import traceback
import os
from random import choice
from abs_path import resource_path
from pygame.locals import *
# ================导入模块================

# ================导入自定义模块================
import myplane
import enemy
import bullet
import supply

# ================导入自定义模块================

# ================创建窗口====================
pygame.init()  # pygame初始化
pygame.mixer.init()  # 混音器初始化
bg_size = width, height = 480, 852  # 设计背景尺寸
x = (1920 - width) // 2
y = (1080 - height) // 2
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)  # 设置窗口位置为中间
screen = pygame.display.set_mode(bg_size, DOUBLEBUF, 32)  # 设置背景对话框

pygame.display.set_caption("飞机大战Beta版!")  # 设置窗口标题
# ================创建窗口====================

# ==============载入游戏音乐================
pygame.mixer.music.load(resource_path(r'resources\game_music.wav'))
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound(resource_path(r'resources\bullet.wav'))
bullet_sound.set_volume(0.2)
big_enemy_flying_sound = pygame.mixer.Sound(
    resource_path(r'resources\big_spaceship_flying.wav'))
big_enemy_flying_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound(
    resource_path(r'resources\enemy1_down.wav'))
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound(
    resource_path(r'resources\enemy2_down.wav'))
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound(
    resource_path(r'resources\enemy3_down.wav'))
enemy3_down_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound(resource_path(r'resources\game_over.wav'))
me_down_sound.set_volume(0.2)
button_down_sound = pygame.mixer.Sound(resource_path(r'resources\button.wav'))
button_down_sound.set_volume(0.4)
level_up_sound = pygame.mixer.Sound(
    resource_path(r'resources\achievement.wav'))
level_up_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound(resource_path(r'resources\use_bomb.wav'))
bomb_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound(resource_path(r'resources\get_bomb.wav'))
get_bomb_sound.set_volume(0.4)
get_bullet_sound = pygame.mixer.Sound(
    resource_path(r'resources\get_double_laser.wav'))
get_bullet_sound.set_volume(0.4)


# ==============载入游戏音乐================

# ===========敌方飞机生成控制函数============


def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)


def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)


# ===========敌方飞机生成控制函数============

# ====================提升敌机速度====================


def inc_speed(target, inc):
    for each in target:
        each.speed += inc


# ====================提升敌机速度====================

# ===========最高分保存,读取函数============
score_filename = resource_path(r'resources\score_record.json')


def create_score_file():
    try:
        inFile = open(score_filename, 'r')
    except FileNotFoundError:
        inFile = open(score_filename, 'w')
        json.dump(0, inFile)


def load_best_score():
    inFile = open(score_filename, 'r')
    score = json.load(inFile)
    return score


def save_score(score):
    best_score = load_best_score()
    if score > best_score:
        inFile = open(score_filename, 'w')
        json.dump(score, inFile)


# ===========最高分保存,读取函数============

# =================主程序===================


def main():
    # ==========================初始化============================
    clock = pygame.time.Clock()  # 设置帧率
    switch_image = False  # 控制飞机图片切换的标志位（用以模拟发动机喷火效果)
    pygame.mixer.music.play(-1)  # 循环播放音乐
    me = myplane.Myplane(bg_size)  # 生成我方飞机
    score = 0  # 统计用户得分
    level = 1  # 游戏难度级别
    life_num = 3  # 一共有三条命
    bomb_num = 3  # 初始为三个炸弹
    delay = 60  # 延时参数
    paused = False  # 标志是否暂停游戏
    create_score_file()
    # 定义分数字体:
    score_font = pygame.font.Font(
        resource_path(r'resources\Score_Font.otf'), 27)
    bomb_font = pygame.font.Font(
        resource_path(r'resources\Score_Font.otf'), 32)
    # 定义颜色:
    color_black = (0, 0, 0)
    color_green = (0, 255, 0)
    color_red = (255, 0, 0)
    color_white = (255, 255, 255)

    flag_record = False  # 标志是否已经存入最高分
    invincible_timer = USEREVENT + 2  # 接触我方飞机无敌时间定时器
    # ==================加载图片===================
    # =================背景图像=================
    background = pygame.image.load(resource_path(r"resources\background.png"))
    gameover_image = pygame.image.load(
        resource_path(r'resources\game_over.png'))
    gameover_rect = gameover_image.get_rect()
    # =================背景图像=================

    # ===============暂停图标===============
    pause_nor_image = pygame.image.load(
        resource_path(r'resources\game_pause_nor.png'))
    pause_pressed_image = pygame.image.load(
        resource_path(r'resources\game_pause_pressed.png'))
    resume_nor_image = pygame.image.load(
        resource_path(r'resources\game_resume_nor.png'))
    resume_pressed_image = pygame.image.load(
        resource_path(r'resources\game_resume_pressed.png'))
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = pause_nor_image  # 设置默认显示的暂停按钮
    # ===============暂停图标===============

    # ==============生命值图标==============
    life_image = pygame.image.load(resource_path(
        r'resources\life.png')).convert_alpha()
    life_rect = life_image.get_rect()
    # ==============生命值图标==============

    # ==============全屏炸弹图标==============
    bomb_image = pygame.image.load(
        resource_path(r"resources\bomb.png"))  # 加载全屏炸弹图标
    bomb_rect = bomb_image.get_rect()
    # ==============全屏炸弹图标==============

    # ===============回到游戏图标===============
    regame_image = pygame.image.load(
        resource_path(r'resources\btn_finish.png'))
    regame_rect = regame_image.get_rect()
    regame_rect.left, regame_rect.top = (
        480 - regame_rect.width) // 2, 370 + regame_rect.height
    # ===============回到游戏图标===============
    # ==================加载图片===================
    # ==========================初始化============================

    # ====================实例化补给包====================
    bullet_supply = supply.BulletSupply(bg_size)
    bomb_supply = supply.BombSupply(bg_size)
    supply_timer = USEREVENT  # 补给包发放定时器
    pygame.time.set_timer(supply_timer, 9 * 1000)  # 定义每10秒发放一次补给包
    # ====================实例化补给包====================

    # =============实例化敌方飞机================
    enemies = pygame.sprite.Group()  # 生成敌方飞机组
    small_enemies = pygame.sprite.Group()  # 敌方小型飞机组
    add_small_enemies(small_enemies, enemies, 1)  # 生成若干敌方小型飞机
    mid_enemies = pygame.sprite.Group()  # 敌方中型飞机组
    add_mid_enemies(mid_enemies, enemies, 1)  # 生成若干敌方中型飞机
    big_enemies = pygame.sprite.Group()  # 敌方大型飞机组
    add_big_enemies(big_enemies, enemies, 1)  # 生成若干敌方大型飞机
    # =============实例化敌方飞机================

    # ===============生成普通子弹===============
    bullet1 = []
    bullet1_index = 0
    bullet1_num = 6  # 定义子弹实例化个数
    for i in range(bullet1_num):
        bullet1.append(bullet.Bullet1())
    # ===============生成普通子弹===============

    # ===============生成超级子弹===============
    double_bullet_timer = USEREVENT + 1  # 超级子弹持续时间定时器
    is_double_bullet = False  # 是否使用超级子弹标志位
    bullet2 = []
    bullet2_index = 0
    bullet2_num = 10  # 定义子弹实例化个数
    for i in range(bullet2_num // 2):
        bullet2.append(bullet.Bullet2())
        bullet2.append(bullet.Bullet2())
    # ===============生成超级子弹===============

    # =============飞机损毁图像索引=============
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0
    # =============飞机损毁图像索引=============

    # 主循环:
    running = True
    while running:
        if not (delay % 3):  # 每3帧切换一次图片
            switch_image = not switch_image
        # ====================绘制背景图和得分====================
        screen.blit(background, (0, 0))
        score_text = score_font.render(
            '得分: {}'.format(score), True, color_white)
        screen.blit(score_text, (0, 0))
        # ====================绘制背景图和得分====================

        # ====================定义难度递进操作====================
        if level == 1 and score > 50000:  # 如果达到第二难度等级，则增加3架小型敌机，2架中型敌机，1架大型敌机,并提升小型敌机速度
            level = 2
            level_up_sound.play()
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            inc_speed(small_enemies, 1)
        elif level == 2 and score > 200000:  # 如果达到第三难度等级
            level = 3
            level_up_sound.play()
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
            bomb_num += 1
        elif level == 3 and score > 400000:  # 如果达到第四难度等级
            level = 4
            level_up_sound.play()
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
            inc_speed(big_enemies, 1)
            bomb_num += 2
        elif level == 4 and score > 1000000:  # 如果达到第五难度等级
            level = 5
            level_up_sound.play()
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
            inc_speed(big_enemies, 1)
            bomb_num += 3
        # ====================定义难度递进操作====================

        # ====================检测用户的退出及暂停操作====================
        for event in pygame.event.get():  # 响应用户的偶然操作
            if event.type == QUIT:  # 如果用户按下屏幕上的关闭按钮，触发QUIT事件，程序退出
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):  # 如果鼠标悬停在按钮区域
                    if paused:  # r如果当前的状态是暂停
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
            elif event.type == MOUSEBUTTONDOWN:
                button_down_sound.play()
                # 如果检测到用户在指定按钮区域按下鼠标左键:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:  # r如果当前的状态是暂停
                        paused_image = resume_pressed_image
                        # 关闭补给机制以及所有音效:
                        pygame.time.set_timer(supply_timer, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        paused_image = pause_pressed_image
                        # 开启补给机制以及所有音效:
                        pygame.time.set_timer(supply_timer, 9 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                if event.button == 1 and regame_rect.collidepoint(event.pos):
                    # 如果用户点击回到游戏按钮
                    # ==============重置游戏===============
                    pygame.time.set_timer(supply_timer, 9 * 1000)  # 开启补给包
                    pygame.mixer.music.play(-1)  # 循环背景音乐
                    me.reset()  # 重置我方飞机
                    score = 0  # 分数初始化
                    level = 1  # 难度等级初始化
                    life_num = 3  # 生命值初始化
                    bomb_num = 3  # 超级炸弹初始化
                    for b in bullet1:
                        b.reset(me.rect.midtop)
                    is_double_bullet = False  # 超级子弹关闭
                    # 补给品关闭：
                    bomb_supply.active = False
                    bullet_supply.active = False

                    del enemies  # 删除所有敌机
                    # 重新生成敌机：
                    enemies = pygame.sprite.Group()  # 生成敌方飞机组
                    small_enemies = pygame.sprite.Group()  # 敌方小型飞机组
                    add_small_enemies(small_enemies, enemies, 1)  # 生成若干敌方小型飞机
                    mid_enemies = pygame.sprite.Group()  # 敌方中型飞机组
                    add_mid_enemies(mid_enemies, enemies, 1)  # 生成若干敌方中型飞机
                    big_enemies = pygame.sprite.Group()  # 敌方大型飞机组
                    add_big_enemies(big_enemies, enemies, 1)  # 生成若干敌方大型飞机
                    for e in enemies:  # 激活所有敌机
                        e.reset()
                        # ==============重置游戏===============
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:  # 如果检测到用户按下空格键
                    if bomb_num:  # 如果炸弹数量大于零，则引爆一颗超级炸弹
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:  # 屏幕上的所有敌机均销毁
                                each.active = False
            elif event.type == supply_timer:  # 响应补给发放的事件消息
                if choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            elif event.type == double_bullet_timer:  # 响应超级子弹的事件消息
                is_double_bullet = False
                pygame.time.set_timer(double_bullet_timer, 0)
            elif event.type == invincible_timer:  # 如果无敌时间已过
                me.invincible = False
                pygame.time.set_timer(invincible_timer, 0)
        # ====================检测用户的退出及暂停操作====================

        # ====================绘制暂停图标====================
        screen.blit(paused_image, paused_rect)
        # ====================绘制暂停图标====================

        if life_num and (not paused):  # 如果游戏未被暂停，正常运行
            # ============绘制全屏炸弹数量和剩余生命数量=============
            bomb_text = bomb_font.render(
                "× {:0>2d}".format(bomb_num), True, color_black)
            bomb_text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width,
                                    height - 20 - bomb_text_rect.height))
            for i in range(life_num):
                screen.blit(life_image, (width - 10 - (i + 1) *
                                         life_rect.width, height - life_rect.height))
            # ============绘制全屏炸弹数量和剩余生命数量=============

            # ====================控制飞机====================
            key_pressed = pygame.key.get_pressed()  # 获得用户所有的键盘输入序列
            if key_pressed[K_w] or key_pressed[K_UP]:
                # 如果用户通过键盘发出“向上”的指令,其他类似
                me.move_up()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.move_down()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.move_left()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.move_right()
            # ====================控制飞机====================

            # =================发射子弹===================
            if not (delay % 10):
                bullet_sound.play()
                if not is_double_bullet:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % bullet1_num
                else:  # 如果当前是超级子弹状态
                    bullets = bullet2
                    bullets[bullet2_index].reset(
                        (me.rect.centerx - 35, me.rect.centery))
                    bullets[bullet2_index +
                            1].reset((me.rect.centerx + 28, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % bullet2_num
            # =================发射子弹===================

            # ===========================检测碰撞===========================
            # ===============绘制补给并检测玩家是否获得================
            if bomb_supply.active:  # 如果是超级炸弹补给包
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False
            if bullet_supply.active:  # 如果是超级子弹补给包
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    is_double_bullet = True
                    bullet_supply.active = False
                    # 超级子弹事件持续18秒:
                    pygame.time.set_timer(double_bullet_timer, 18 * 1000)
            # ===============绘制补给并检测玩家是否获得================

            # =================检测是否击中敌机==================
            for b in bullets:
                if b.active:  # 只有激活的子弹才可能击中敌机
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemies_hit = pygame.sprite.spritecollide(
                        b, enemies, False, pygame.sprite.collide_mask)
                    if enemies_hit:  # 如果子弹击中飞机
                        b.active = False  # 子弹损毁
                        for e in enemies_hit:
                            if e in big_enemies or e in mid_enemies:
                                e.energy -= 1
                                e.hit = True  # 表示飞机已经被击中
                                if e.energy == 0:
                                    e.active = False  # 大中型敌机损毁
                            else:
                                e.active = False  # 小型敌机损毁
            # =================检测是否击中敌机===================

            # ===============检测是否与敌机碰撞=======================
            enemies_down = pygame.sprite.spritecollide(
                me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                # 如果碰撞检测返回的列表非空，则说明已发生碰撞,若此时我方飞机处于无敌状态
                me.active = False
                for e in enemies_down:
                    e.active = False
            # ===============检测是否与敌机碰撞=======================
            # ===========================检测碰撞===========================

            # =================我方飞机===================
            if delay == 0:
                delay = 60
            delay -= 1
            if me.active:
                if switch_image:  # 绘制我方飞机的两种不同的形式
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                if switch_image:
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        me_down_sound.play()
                        life_num -= 1
                        me.reset()
                        # 我方飞机重生并开始无敌时间计时:
                        pygame.time.set_timer(invincible_timer, 3 * 1000)
            # =================我方飞机===================

            # =================敌方飞机===================
            for each in big_enemies:  # 绘制大型敌机并自动移动
                if each.active:  # 如果飞机正常存在
                    each.move()
                    if each.rect.bottom == 0:
                        big_enemy_flying_sound.play(-1)

                    if not each.hit:
                        # 如果飞机未被击中
                        if switch_image:
                            # 绘制大型敌机的两种不同的形式
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)
                    else:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False

                    # ====================绘制血槽====================
                    pygame.draw.line(screen, color_black,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5),
                                     2)
                    energy_remain3 = each.energy / enemy.BigEnemy.energy
                    if energy_remain3 > 0.2:  # 如果血量大约百分之二十则为绿色，否则为红色
                        energy_color = color_green
                    else:
                        energy_color = color_red
                    pygame.draw.line(screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain3,
                                      each.rect.top - 5),
                                     2)
                    # ====================绘制血槽====================
                else:
                    # ====================飞机坠毁====================

                    big_enemy_flying_sound.stop()
                    if e3_destroy_index == 0:
                        enemy3_down_sound.play()  # 播放飞机撞毁音效

                    if switch_image:  # 每三帧播放一张损毁图片
                        screen.blit(each.destroy_images[
                            e3_destroy_index], each.rect)
                        e3_destroy_index = (
                            e3_destroy_index + 1) % 6  # 大型敌机有六张损毁图片
                        if e3_destroy_index == 0:
                            # 如果损毁图片播放完毕，则重置飞机属性
                            score += 30000  # 如果大型飞机坠毁,加500分
                            each.reset()
                            # ====================飞机坠毁====================
            for each in mid_enemies:  # 绘制中型敌机并自动移动
                if each.active:
                    each.move()
                    if not each.hit:
                        screen.blit(each.image, each.rect)
                    else:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    # ====================绘制血槽====================
                    pygame.draw.line(screen, color_black,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5),
                                     2)
                    energy_remain2 = each.energy / enemy.MidEnemy.energy
                    if energy_remain2 > 0.2:
                        energy_color = color_green
                    else:
                        energy_color = color_red
                    pygame.draw.line(screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain2,
                                      each.rect.top - 5),
                                     2)
                    # ====================绘制血槽====================
                else:
                    # ====================飞机坠毁====================

                    if e2_destroy_index == 0:
                        enemy2_down_sound.play()
                    if switch_image:
                        screen.blit(each.destroy_images[
                            e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 6000  # 如果中型飞机坠毁,加200分
                            each.reset()
                            # ====================飞机坠毁====================

            for each in small_enemies:  # 绘制小型敌机并自动移动
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # ====================飞机坠毁====================

                    if e1_destroy_index == 0:
                        enemy1_down_sound.play()
                    if switch_image:
                        screen.blit(each.destroy_images[
                            e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 1000  # 如果小型敌机坠毁,加100分
                            each.reset()
                            # ====================飞机坠毁====================
                            # =================敌方飞机===================

        elif life_num == 0:
            # ================绘制gameover画面================
            screen.blit(gameover_image, gameover_rect)
            pygame.mixer.music.stop()  # 关闭背景音乐
            pygame.mixer.stop()  # 关闭所有音效
            pygame.time.set_timer(supply_timer, 0)  # 关闭补给机制

            if not flag_record:  # 读取历史最高分
                save_score(score)
                record_score = load_best_score()
                flag_record = True

            record_score_text = score_font.render(
                '{}'.format(record_score), True, color_white)
            screen.blit(record_score_text, (150, 41))
            game_over_score_text = score_font.render(
                "{: ^10}".format(score), True, color_white)
            screen.blit(game_over_score_text, (175, 370))
            screen.blit(regame_image, regame_rect)
            # ================绘制gameover画面================
        pygame.display.flip()  # 将绘制好的surface对象一次全部刷新到屏幕上
        clock.tick(60)  # 设置帧数为60


# =================主程序===================

if __name__ == '__main__':
    try:
        main()
    except SystemError:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
