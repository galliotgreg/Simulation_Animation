from html.parser import interesting_normal

import pygame
import sys
import math
from random import randint

screen = pygame.display.set_mode((1024, 768))

angles = [0,0,0,0]
angles_courants = [0,0,0,0]

target_point = (int(1024/2) - 300, int(768/2) - 300)
init_point = (int(1024/2), int(768/2))

distances = [50,50,50,50]
joins = [init_point]

def calcul_norme(p):
    norme = math.sqrt(p[0]**2 + p[1]**2)
    if norme == 0:
        norme = 1
    return norme


def calcul_direction(p1,p2):
    res = (p2[0] - p1[0], p2[1] - p1[1])
    norme = calcul_norme(res)
    res_norm_x = (res[0]/ norme)
    res_norm_y = (res[1] / norme)

    res_norm = (res_norm_x, res_norm_y)
    return res_norm


def step_one():

    global target_point

    for i in range(1, len(joins)):
        if i == 1:
            #A'
            joins[len(joins) - i] = target_point

        #d
        direction = calcul_direction(joins[len(joins)-i], joins[len(joins)-i-1])
        print(direction)

        #l
        dist = distances[3-i]

        #B'
        joins[len(joins) -i-1] = (joins[len(joins) -i][0] + int(dist * direction[0]), joins[len(joins) -i][1]+ int(dist * direction[1]))


def step_two():

    global init_point

    for i in range(0, len(joins)-1):
        if i == 0:
            #A'
            joins[i] = init_point

        #d
        direction = calcul_direction(joins[i], joins[i+1])
        print(direction)

        #l
        dist = distances[i]

        #B'
        joins[i+1] = (joins[i][0] + int(dist * direction[0]), joins[i][1] + int(dist * direction[1]))


def draw():
    screen.fill((0,0,0))
    for join in joins:
        pygame.draw.circle(screen, (255,0,0), join, 3, 1)
    pygame.draw.lines(screen, (255,255,255), False, joins, 1)
    pygame.draw.circle(screen, (120,0,125), target_point, 3, 1)

    pygame.display.flip()


def init():
    pygame.init()
    pygame.display.update()

    global angles
    global angles_courants
    global distances
    global joins

    distances = [50,50,50,50]
    joins = [init_point]

    x_temp = 1024 / 2
    y_temp = 768 / 2

    for i in range(0, len(angles)):
        print(joins)
        angle_res = 0
        distance_res = 0

        if i == 0:
            angles_courants[i] = angles[i]
        else:
            angles_courants[i] = angles_courants[i - 1] + angles[i]

        distance_res += distances[i]

        x_temp += math.cos(math.radians(angles_courants[i])) * distance_res
        y_temp += math.sin(math.radians(angles_courants[i])) * distance_res

        joins.append((int(x_temp), int(y_temp)))


def main():

    global angles
    global target_point
    init()
    draw()

    while (True) :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.time.wait(200)

        for i in range(0, 14):
            step_one()
            print(joins)
            step_two()
            print(joins)
        draw()

        rand_x = randint(0,300)
        rand_y = randint(0,300)

        target_point = (int(1024/2) - rand_x, int(768/2) - rand_y)



main()