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
        self.width = 50
        self.height = 50
        self.barycentre = (0,0)

        self.position = position
        self.vitesse = (0,0)
        self.masse = masse
        self.acceleration = (0,0)
        self.isColliding = False

    def calcul_barycentre(self):
        barycentre_x = ((self.position[0] + self.width) - self.position[0]) //2
        barycentre_y = ((self.position[1] + self.height) - self.position[1])//2
        self.barycentre = (barycentre_x, barycentre_y)

    def calcul_position(self):
        self.position = (self.position[0] + self.vitesse[0], self.position[1] + self.vitesse[1])

    def calcul_vitesse(self):
        self.vitesse = (self.vitesse[0] + self.acceleration[0], self.vitesse[1] + self.acceleration[1])

    def calcul_acceleration(self):
        self.acceleration = (0/self.masse , 9.806/self.masse)

    def draw(self):

        if not self.isColliding:
            self.calcul_acceleration()
            self.calcul_vitesse()
            self.calcul_position()
            self.calcul_barycentre()

        pygame.draw.rect(screen, color_red, (self.position[0], self.position[1], self.width, self.height), thickness)


class Ground:
    def __init__(self, position):
        self.position = position
        self.width = width_ground
        self.height = height_ground

    def draw_ground(self):
        pygame.draw.rect(screen, color_blue, (self.position[0], self.position[1], self.width, self.height), thickness)


class Scene:
    def __init__(self):
        self.boxes = []
        self.grounds = []

    def add_box(self, box):
        self.boxes.append(box)

    def add_ground(self,ground):
        self.grounds.append(ground)

    def draw_scene(self):
        screen.fill((0, 0, 0))
        for box in self.boxes:
            box.draw()

        for ground in self.grounds:
            ground.draw_ground()

    def calcul_collision(self):
        #collision box vs ground
        for box in self.boxes:
            for ground in self.grounds:
                if box.position[1] + box.height >= ground.position[1]:
                    if ground.position[0] <= box.position[0] <= ground.position[0]+ ground.width:
                        box.isColliding = True
                        box.position = (box.position[0],ground.position[1] - box.height)

        #collision box vs box
        for box1 in self.boxes:
            for box2 in self.boxes:
                if box1 is not box2:
                    if box1.position[1] + box1.height >= box2.position[1]:
                        if box2.position[0] <= box1.position[0] <= (box2.position[0] + box2.width) or box2.position[0] <= box1.position[0] + box1.width <= (box2.position[0] + box2.width):
                            if box2.isColliding:
                                if not box1.isColliding:
                                    box1.isColliding = True
                                    box1.position = (box1.position[0], box2.position[1] - box1.height)




def init():
    pygame.init()
    pygame.display.update()


def main():

    init()

    scene = Scene()

    box1 = Box((50, 50), 1000)
    box2 = Box((90, 50),10000)
    box3 = Box((132, 50),100000)
    box4 = Box((800, 50), 10000)

    ground1 = Ground((0, 760))

    scene.add_box(box1)
    scene.add_box(box2)
    scene.add_box(box3)
    scene.add_box(box4)

    scene.add_ground(ground1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        scene.calcul_collision()
        scene.draw_scene()
        pygame.display.update()

main()