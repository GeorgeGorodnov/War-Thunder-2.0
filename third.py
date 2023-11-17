import math
import random
import time
from random import choice
from random import uniform as rnd
import numpy as np
import sys
from tkinter import *
from tkinter import messagebox

import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK1 = 0xFFC91F
WHITE = 0xFFFFFF
GREY = 0x000000
g = 9 / 10
GAME_COLORS = [BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

pygame.init()
mouse_x, mouse_y = pygame.mouse.get_pos()

image_orig = pygame.Surface((100, 20))
image_orig.set_colorkey(YELLOW)
image_orig.fill(GREY)
# creating a copy of orignal image for smooth rotation
image = image_orig.copy()
image.set_colorkey(GREEN)
# define rect for placing the rectangle at the desired position
rect = image.get_rect()
rect.center = (80, 400)
balltypes = ['basic', 'fast', 'heavy', 'anti']
dulo = pygame.image.load(r'C:\Users\gorod\PycharmProjects\pythonProject\чисто дуло1.png')
tank = pygame.image.load(r'C:\Users\gorod\PycharmProjects\pythonProject\танк внатуре.png')
knat = pygame.image.load(r'C:\Users\gorod\PycharmProjects\pythonProject\ерутанв кнат.png')
dron = pygame.image.load(r'C:\Users\gorod\PycharmProjects\pythonProject\litak.png')
expl = pygame.image.load(r'C:\Users\gorod\PycharmProjects\pythonProject\БАБАХ.png')
bomb = pygame.image.load(r'C:\Users\gorod\PycharmProjects\pythonProject\конкретная бомба.png')
dmg_fighter = pygame.image.load(r'C:\Users\gorod\PycharmProjects\pythonProject\бочок потик.png')
dstr_tank = pygame.image.load(r'C:\Users\gorod\PycharmProjects\pythonProject\прихлопнули таракашку.png')
fighter = pygame.image.load(r'C:\Users\gorod\PycharmProjects\pythonProject\воздущный чертила.png')
shotx = 0
shoty = 0




class Ball(object):
    def __init__(self, screen: pygame.Surface, x=shotx, y=shoty, type='basic'):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.type = type
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.livetime = 0
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.weight = 1
        self.g = 9 / 10
        print(self.x, self.y)

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if self.x - obj.rx >= -self.r:
            return 1
        elif self.y - obj.y <= self.r:
            return 2
        elif obj.lx - self.x >= -self.r:
            return 3
        elif obj.dy - self.y <= self.r:
            return 4
        else:
            return False

    def targettest(self, trg):
        if (self.x - trg.rx) ** 2 + (self.y - trg.y) ** 2 <= (self.r + trg.r) ** 2:
            return True
        else:
            return False

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        global wall
        # FIXME
        self.flag = self.hittest(wall)
        if not self.flag:
            self.vy -= self.g
        else:
            if self.flag == 1 or self.flag == 3:
                self.vx = -self.vx
                self.vy -= self.g
            elif self.flag == 2:
                if self.type != 'anti':
                    self.vy = (-self.vy - self.g)
                else:
                    balls.remove(self)
            elif self.flag == 4:
                if abs(self.vy ** 2 + self.vx ** 2) > 0.05:
                    self.vx = self.vx * 0.6
                    self.vy = max(0, -self.vy * 0.6 - self.g)
                    print(3)
                else:
                    self.vx = 0
                    self.vy = 0
                    self.livetime += 1
                    if self.livetime > 20:
                        balls.remove(self)
        if self in balls:
            self.x += self.vx
            self.y -= self.vy

class HeavyBall(Ball):
    def __init__(self, screen: pygame.Surface):
        Ball.__init__(self, screen, type='heavy', x=shotx, y=shoty)
        self.color = GREY
        self.r = 25
        self.weight = 3.15



class FastBall(Ball):
    def __init__(self, screen: pygame.Surface):
        Ball.__init__(self, screen, type='fast', x=shotx, y=shoty)
        self.color = YELLOW
        self.r = 5
        self.weight = 1.5
class AntiBall(Ball):
    def __init__(self, screen: pygame.Surface):
        Ball.__init__(self, screen, type='anti', x=shotx, y=shoty)
        self.color = CYAN
        self.r = 10
        self.weight = 2
        self.g = - 9 / 10



class Gun:
    def __init__(self, screen: pygame.Surface, x=40, y=500):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 200
        self.y = y
        self.vx = 0

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        global changed_type
        if balltypes[changed_type] == 'basic':
            new_ball = Ball(self.screen)
        elif balltypes[changed_type] == 'anti':
            new_ball = AntiBall(self.screen)
        elif balltypes[changed_type] == 'fast':
            new_ball = FastBall(self.screen)
        elif balltypes[changed_type] == 'heavy':
            new_ball = HeavyBall(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an) / new_ball.weight
        new_ball.vy = - self.f2_power * math.sin(self.an) / new_ball.weight
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10


    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1] - 450) // (event.pos[0] - 20) + 0.01)
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        global shotx, shoty
        global rect
        rel_x, rel_y = mouse_x - self.x - 45, mouse_y - 510
        phi = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        if 90 > phi >= -90:
            screen.blit(tank, (self.x - 40, 483))
        else:
            screen.blit(knat, (self.x - 40, 483))
        tank_size = [140, 74]
        dulo_size = [109, 10]
        image_orig = dulo
        rect = image_orig.get_rect()
        if 180 >= phi > 90:
            rect.center = (self.x + 65 + 109 * math.cos(phi / 180 * math.pi), 510 - 109 * math.sin(phi / 180 * math.pi))
        elif (90 >= phi > 0):
            rect.center = (self.x + 105, 510 - 109 * math.sin(phi / 180 * math.pi))
        elif (-90 > phi >= -180):
            rect.center = (self.x + 65 + 109 * math.cos(phi / 180 * math.pi), 510)
        elif (0 > phi >= -90):
            rect.center = (self.x + 105, 510)
        shotx = self.x + 45 + 109 * math.cos(phi/ 180 * math.pi)
        shoty = 510 - 109 * math.sin(phi / 180 * math.pi)
        new_image = pygame.transform.rotate(image_orig, phi)
        screen.blit(new_image, rect)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 80:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY
    def move(self):
        self.x += self.vx



class Target:
    def __init__(self, seed=1, Image=dron):
        self.max_health = 1
        self.health = 1
        self.points = 0
        self.live = 1
        self.rx = rnd(200, 700)
        self.lx = 100
        self.y = rnd(200, 350)
        self.r = 50
        self.seed = seed
        self.screen = screen
        self.vx = 0
        self.vy = 0
        self.image = Image
        self.destroy_image = expl
        self.active_image = None
        self.new_target()

    def move(self):
        if 30 < self.rx < 770:
            self.rx += self.vx
        else:
            self.vx = -self.vx
            self.rx += self.vx
        if 50 < self.y < 350:
            self.y += self.vy
        else:
            self.vy = -self.vy
            self.y += self.vy

    def new_target(self, minvx=1, maxvx=15, minvy=1, maxvy=15):
        """ Инициализация новой цели. """

        rx = self.rx = rnd(200, 700)
        y = self.y = rnd(200, 350)
        r = self.r = rnd(9, 50)
        self.vx = rnd(minvx, maxvx)
        self.vy = rnd(minvy, maxvy)
        self.active_image = self.image
        self.health = self.max_health

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        rect = self.active_image.get_rect()
        rect.center = (self.rx, self.y)
        screen.blit(self.active_image, rect)


class Fighter(Target):
    def __init__(self):
        Target.__init__(self, Image=fighter)
        self.vx = rnd(20,35)
        self.vy = rnd(4, 12)
        self.r = 115
        self.max_health = 2
        self.health = 2
        self.damage_image = dmg_fighter
    def new_target(self):
        Target.new_target(self, minvx = 20, maxvx =35, minvy =3, maxvy =12)
    def bombing(self):
        global bombs
        print('bomb')
        new_bomb = Bomb(self.screen, self.rx, y = self.y - 20)
        bombs.append(new_bomb)




class Bomb:
    def __init__(self,screen: pygame.Surface, x=0, y=0):
        self.x = x
        self.screen = screen
        self.y = y
        self.vy = 0
        self.r = 20
    def draw(self):
        #pygame.draw.circle(self.screen, MAGENTA, (self.x, self.y), self.r)
        screen.blit(bomb, (self.x, self.y))
    def move(self):
        self.vy += 5/10
        self.y += self.vy
    def hittest(self, ob):
        self.dist_to_tank = [ob.x - self.x, ob.y - self.y]
        hit_check = (abs(self.dist_to_tank[0]) > 60) + (abs(self.dist_to_tank[1]) > 30)
        if not hit_check:
            screen.blit(dstr_tank, (ob.x - 167, 361))
            pygame.display.update()
            Tk().wm_withdraw()
            messagebox.showinfo('pygame', 'You lose!')
            quit()




class Wall:
    def __init__(self):
        self.rx = 780
        self.lx = 20
        self.y = -2000
        self.dy = 580
        self.r = 10


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
bombs = []

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Fighter()
target2 = Target(seed=777)
wall = Wall()
finished = False
check1 = False
check2 = False
changed_type = 1
damage_timer = 0
bombing_timer = 0

while not finished:
    screen.fill(WHITE)
    gun.draw()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    target1.draw()
    target1.move()
    target2.draw()
    target2.move()
    bombing_timer += 1
    damage_timer+=1
    gun.move()
    for b in balls:
        b.draw()
    for b in bombs:
        b.draw()
    pygame.display.update()

    if target1.health != 0 and bombing_timer > 100:
        target1.bombing()
        bombing_timer = 0

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                changed_type = 1
            elif event.key == pygame.K_2:
                changed_type = 2
            elif event.key == pygame.K_3:
                changed_type = 3

        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            gun.vx = 10
        elif keys[pygame.K_a]:
            gun.vx = -10
        else:
            gun.vx = 0
    for b in bombs:
        b.move()
        b.hittest(gun)
    for b in balls:
        b.move()
        if check1:
            timer1 += 1
            if timer1 == 25:
                target1.new_target()
        if check2:
            timer2 += 1
            if timer2 == 25:
                target2.new_target()
        if b.targettest(target1):
            if damage_timer > 40:
                target1.health -= 1
                damage_timer = 0
                bombing_timer -= 50
                if target1.health <= 0:
                    target1.hit()
                    bombing_timer -= 120
                    check1 = True
                    timer1 = 0
                    target1.active_image = target1.destroy_image
                else:
                    target1.active_image = target1.damage_image
                    target1.vx = target1.vx // 2
                    target1.vy = target1.vy // 2
        if b.targettest(target2):
            check2 = True
            target2.hit()
            timer2 = 0
            target2.active_image = target2.destroy_image
    gun.power_up()

pygame.quit()
