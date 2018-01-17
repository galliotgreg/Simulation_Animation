import pygame
import sys
import math
from random import randint

screen = pygame.display.set_mode((1024, 768))

color_red = (255,0,0)

color_blue = (0,0,255)
width_ground = 500
height_ground = 10

thickness = 1

delta_t = 0.1


class Box:

    def __init__(self, position, masse):
        self.width_box = 50
        self.height_box = 50

        self.position = position
        self.vitesse = (0,0)
        self.masse = masse
        self.acceleration = (0,0)
        self.isColliding = False

    def calcul_position(self):
        self.position = (self.position[0] + self.vitesse[0], self.position[1] + self.vitesse[1])

    def calcul_vitesse(self):
        self.vitesse = (self.vitesse[0] + self.acceleration[0], self.vitesse[1] + self.acceleration[1])

    def calcul_acceleration(self):
        self.acceleration = (0/self.masse , 9.806/self.masse)

    def draw_box(self):

        if not self.isColliding:
            self.calcul_acceleration()
            self.calcul_vitesse()
            self.calcul_position()

        pygame.draw.rect(screen, color_red, (self.position[0], self.position[1], self.width_box, self.height_box), thickness)
        pygame.display.update()


class Ground:
    def __init__(self, position):
        self.position = position

    def draw_ground(self):
        pygame.draw.rect(screen, color_blue, (self.position[0], self.position[1], width_ground, height_ground), thickness)
        pygame.display.update()


class Scene:
    def __init__(self):
        self.boxes = []
        self.grounds = []

    def add_box(self, box):
        self.boxes.append(box)

    def add_ground(self,ground):
        self.grounds.append(ground)

    def draw_scene(self):
        for box in self.boxes:
            box.draw_box()

        for ground in self.grounds:
            ground.draw_ground()

    def calcul_collision(self):
        for box in self.boxes :
            for ground in self.grounds :
                if(box.position[1] + box.height_box >= ground.position[1]) :
                    box.isColliding = True





def init():
    pygame.init()
    pygame.display.update()


def main():

    init()

    scene = Scene()

    box1 = Box((50, 50), 1000)
    box2 = Box((101, 50),10000)
    box3 = Box((152, 50),100000)

    ground1 = Ground((0, 760))

    scene.add_box(box1)
    scene.add_box(box2)
    scene.add_box(box3)

    scene.add_ground(ground1)

    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        scene.calcul_collision()
        scene.draw_scene()

main()