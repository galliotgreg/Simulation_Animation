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

nb_joins_max = 4
nb_bones_max = 3

nb_joins = 0
nb_bones = 0

joins = []
bones = []


def distance(p1,p2):
    dist = math.sqrt((p2[0]-p1[0])**2 + (p2[1] - p1[1])**2)
    return dist

def add_bones():
    global nb_joins
    global joins
    global nb_bones
    global bones

    print("add_bones")
    if(len(joins) < 4 ):
        global nb_joins
        nb_joins += 1
        pos = pygame.mouse.get_pos()
        joins.append(pos)


def draw_bones():
    print("draw_bones")
    global joins
    global nb_joins
    pygame.draw.lines(screen, white, False, joins, 1)

def draw_joins():
    print("draw_joins")
    global joins
    global nb_joins
    for join in joins :
        pygame.draw.circle(screen, red, join, 3, 1)

def main():
    print("main")
    pygame.init()
    pygame.display.update()

    colorR = random.randrange(1, 255, 1)
    colorG = random.randrange(1, 255, 1)
    colorB = random.randrange(1, 255, 1)

    colorC = (colorR, colorG, colorB)

    global nb_joins

    while (True):

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if(nb_joins < nb_joins_max):
                    add_bones()
                    if(nb_joins > 1):
                        draw_bones()
                    draw_joins()

        pygame.display.flip()
        pygame.time.delay(10)

main()