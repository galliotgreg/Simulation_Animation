import pygame
import sys
import math
import random

from pygame.locals import *
from qtconsole.styles import dark_color
from scipy.spatial import distance

screen = pygame.display.set_mode((1024, 768))

def main():
    pygame.init()
    pygame.display.update()

    angles = [0, 90, 45]
    distances = [200, 50, 100]
    joins = [(int(1024/2), int(768/2))]

    x_temp = 1024/2
    y_temp = 768/2

    for i in range(0,len(angles)):
        print(joins)
        angle_res = 0
        distance_res = 0

        angle_res += math.radians(angles[i])
        print("angle_res")
        print(angle_res)

        distance_res += distances[i]
        print("distance_res")
        print(distance_res)

        x_temp += math.cos(angle_res) * distance_res
        y_temp += math.sin(angle_res) * distance_res

        print("x")
        print(x_temp)
        print("y")
        print(y_temp)

        joins.append((int(x_temp), int(y_temp)))
    for join in joins:
        pygame.draw.circle(screen, (255,0,0), join, 3, 1)
    pygame.draw.lines(screen, (255,255,255), False, joins, 1)

    pygame.display.flip()

    while (True) :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

main()