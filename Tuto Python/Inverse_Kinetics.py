from html.parser import interesting_normal

import pygame
import sys
import math

screen = pygame.display.set_mode((1024, 768))

angles = [0, 0, 0]
angles_courants = [0, 0, 0]

target_point = (int(1024/2) - 200, int(768/2) - 200)
init_point = (int(1024/2), int(768/2))

distances = [200, 50, 100]
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

    #A'
    joins[len(joins) - 1] = target_point
    draw()
    #d
    direction = calcul_direction(joins[len(joins)-1], joins[len(joins)-2])
    print(direction)

    #l
    dist = distances[2]

    #B'
    joins[len(joins) - 2] = (target_point[0] + int(dist * direction[0]), target_point[1]+ int(dist * direction[1]))
    target_point = joins[len(joins) - 2]


def step_two():

    global target_point

    #A'
    joins[len(joins) - 2] = target_point
    draw()
    #d
    direction = calcul_direction(joins[len(joins)-2], joins[len(joins)-3])
    print(direction)

    #l
    dist = distances[1]

    #B'
    joins[len(joins) - 3] = (target_point[0] + int(dist * direction[0]), target_point[1]+ int(dist * direction[1]))
    target_point = joins[len(joins) - 3]

def step_three():

    global target_point

    #A'
    joins[len(joins) - 3] = target_point
    draw()
    #d
    direction = calcul_direction(joins[len(joins)-3], joins[len(joins)-4])
    print(direction)

    #l
    dist = distances[0]

    #B'
    joins[len(joins) - 4] = (target_point[0] + int(dist * direction[0]), target_point[1]+ int(dist * direction[1]))
    target_point = joins[len(joins) - 4]


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

    distances = [200, 50, 100]
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
    init()
    draw()
    pygame.time.wait(200)
    step_one()
    draw()
    pygame.time.wait(200)
    step_two()
    draw()
    print(joins)
    pygame.draw.lines(screen, (255, 255, 255), False, joins, 1)

    while (True) :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


main()