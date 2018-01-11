import pygame
import sys
import math
import random

from pygame.locals import *
from qtconsole.styles import dark_color
from scipy.spatial import distance

screen = pygame.display.set_mode((1024, 768))
angles = [0, 90, 45]
angles_courants = [0, 0, 0]


def draw():
    pygame.init()
    pygame.display.update()

    global angles
    global angles_courants

    distances = [200, 50, 100]
    joins = [(int(1024/2), int(768/2))]

    x_temp = 1024/2
    y_temp = 768/2

    for i in range(0,len(angles)):
        print(joins)
        angle_res = 0
        distance_res = 0

        if i == 0:
            angles_courants[i] = angles[i]
        else :
            angles_courants[i] = angles_courants[i-1] + angles[i]

        print("angle_res")
        print(angle_res)

        distance_res += distances[i]
        print("distance_res")
        print(distance_res)

        x_temp += math.cos(math.radians(angles_courants[i])) * distance_res
        y_temp += math.sin(math.radians(angles_courants[i])) * distance_res

        print("x")
        print(x_temp)
        print("y")
        print(y_temp)

        joins.append((int(x_temp), int(y_temp)))
    screen.fill((0,0,0))
    for join in joins:
        pygame.draw.circle(screen, (255,0,0), join, 3, 1)
    pygame.draw.lines(screen, (255,255,255), False, joins, 1)

    pygame.display.flip()


def main():

    global angles
    while (True) :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.time.delay(10)
        angles[0] += 1
        draw()

main()