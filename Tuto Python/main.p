import pygame
import sys
import math
import random

from pygame.locals import *
from qtconsole.styles import dark_color

pygame.init()

screen = pygame.display.set_mode((1024, 768))

pygame.display.update()

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

pygame.display.update()

while (True):

    colorR = random.randrange(1,255,1)
    colorG = random.randrange(1,255,1)
    colorB = random.randrange(1,255,1)

    pos = pygame.mouse.get_pos()

    distance = math.sqrt(pos[0] * pos[0] + pos[1] * pos[1])

    colorC = (colorR, colorG, colorB)
    pygame.draw.lines(screen, colorC, False, [(1024/2, 768/2), (pos[0], pos[1])], 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            screen.fill(black)
            pygame.draw.lines(screen, white, False, [(1024/2, 768/2), (pos[0], pos[1])], 1)

    pygame.display.flip()
    pygame.time.delay(10)
