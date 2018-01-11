import pygame
import sys
import math
import random

from pygame.locals import *
from qtconsole.styles import dark_color
from scipy.spatial import distance

screen = pygame.display.set_mode((1024, 768))

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

colorC = (0,0,0)

nb_joins_max = 2
nb_bones_max = 1

nb_joins = 0
nb_bones = 0

joins = []
bones = []

is_moving = False


def calcul_angle(p1,p2):
    angle = math.atan((p2[1]-p1[1]) / (p2[0]-p1[0]))
    return math.degrees(angle)


def calcul_distance(p1,p2):
    distance = math.sqrt((p2[0]-p1[0])**2 + (p2[1] - p1[1])**2)
    return distance

def calcul_nouveau_point(pos):

    i = 1
    angle = calcul_angle(joins[i],joins[i-1])
    print("angle")
    print(angle)
    distance = calcul_distance(joins[i],joins[i-1])
    print("distance")
    print(distance)

    cos_new_point = math.cos(angle) * distance
    sin_new_point = math.sin(angle) * distance
    new_point = (int(cos_new_point + pos[0]), int(sin_new_point + pos[1]))

    print("new point")
    print(new_point)

    joins[i] = new_point

    draw_joins()
    draw_bones()

    return new_point

def add_bones():
    print("add_bones")
    global bones
    bones.append((joins[len(joins)-2], joins[len(joins)-1]))


def add_joins():
    global nb_joins
    global joins
    global nb_bones
    global bones

    if(len(joins) < 4 ):
        global nb_joins
        nb_joins += 1
        pos = pygame.mouse.get_pos()
        joins.append(pos)
        if(len(joins) > 1):
            add_bones()


def draw_bones():
    global joins
    global nb_joins
    pygame.draw.lines(screen, white, False, joins, 1)


def draw_joins():
    global joins
    global nb_joins
    for join in joins:
        pygame.draw.circle(screen, red, join, 3, 1)

def move_join(i):
    global joins
    pos = pygame.mouse.get_pos()
    joins[i] = pos

def main():
    pygame.init()
    pygame.display.update()

    colorR = random.randrange(1, 255, 1)
    colorG = random.randrange(1, 255, 1)
    colorB = random.randrange(1, 255, 1)

    colorC = (colorR, colorG, colorB)

    global nb_joins
    global is_moving

    while (True):

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and is_moving:
                calcul_nouveau_point(pygame.mouse.get_pos())
                is_moving = False
            if event.type == pygame.MOUSEBUTTONUP:
                if(nb_joins < nb_joins_max):
                    add_joins()
                    if(nb_joins > 1):
                        draw_bones()
                    draw_joins()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print("K_left")
                    is_moving = True

        pygame.display.flip()
        pygame.time.delay(10)

main()