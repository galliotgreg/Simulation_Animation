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


def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(math.radians(angle)) * (px - ox) - math.sin(math.radians(angle)) * (py - oy)
    qy = oy + math.sin(math.radians(angle)) * (px - ox) + math.cos(math.radians(angle)) * (py - oy)
    return qx, qy


class Box:
    def __init__(self, position, masse):
        self.width = 50
        self.height = 50
        self.barycentre = (0,0)
        self.angle = 0

        self.position = position
        self.vitesse = (0,0)
        self.masse = masse
        self.acceleration = (0,0)
        self.isColliding = False
        self.hasToRotate = False

        self.point1 = self.position
        self.point2 = (self.position[0] + self.width, self.position[1])
        self.point3 = (self.position[0] + self.width, self.position[1] + self.height)
        self.point4 = (self.position[0], self.position[1] + self.height)

        self.points = [self.point1, self.point2, self.point3, self.point4, self.point1]

        self.forces = [(0, 9.806)]

    def calcul_barycentre(self):
        barycentre_x = int((self.position[0] + (self.width//2)))
        barycentre_y = int((self.position[1] + (self.width//2)))
        self.barycentre = (barycentre_x, barycentre_y)

    def calcul_rotation(self):
        self.point1 = rotate(self.barycentre, self.point1, self.angle)
        self.point2 = rotate(self.barycentre, self.point2, self.angle)
        self.point3 = rotate(self.barycentre, self.point3, self.angle)
        self.point4 = rotate(self.barycentre, self.point4, self.angle)

        self.points = [self.point1, self.point2, self.point3, self.point4, self.point1]

    def calcul_position(self,):

        self.position = (self.position[0] + self.vitesse[0], self.position[1] + self.vitesse[1])

        self.point1 = self.position
        self.point2 = (self.position[0] + self.width, self.position[1])
        self.point3 = (self.position[0] + self.width, self.position[1] + self.height)
        self.point4 = (self.position[0], self.position[1] + self.height)

        self.points = [self.point1, self.point2, self.point3, self.point4, self.point1]

    def calcul_vitesse(self):
        self.vitesse = (self.vitesse[0] + self.acceleration[0], self.vitesse[1] + self.acceleration[1])

    def calcul_acceleration(self):
        force_total = (0,0)
        for force in self.forces:
            force_total = (force_total[0] + force[0], force_total[1] + force[1])
        self.acceleration = (force_total[0]/self.masse, force_total[1]/self.masse)

    def draw(self):

        self.calcul_acceleration()
        self.calcul_vitesse()
        self.calcul_position()
        self.calcul_barycentre()
        self.calcul_rotation()

        pygame.draw.lines(screen, color_red, False, self.points, 1)
        pygame.draw.circle(screen, (120, 0, 125), self.barycentre, 3, 1)


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
                    if ground.position[0] <= box.position[0] <= ground.position[0] + ground.width:
                        if not box.isColliding :
                            box.isColliding = True
                            box.position = (box.position[0], ground.position[1] - box.height)
                            box.vitesse = (0,0)
                            box.forces.append((0,-9.806))
                            print(box.forces)

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
                                    box1.vitesse = (0, 0)
                                    box1.forces.append((0, -9.806))
                                    print(box1.forces)
                                    box1.hasToRotate = True
                                    self.calcul_rotation(box1, box2)
                                elif box1.hasToRotate:
                                    box1.forces = [(0,9.806)]
                                    self.calcul_rotation(box1, box2)


    def calcul_rotation(self,up_box,down_box):
        if up_box.barycentre[0] <= down_box.position[0] + down_box.width:
            up_box.angle -= 1
            up_box.calcul_rotation()
            pygame.draw.lines(screen, color_red, False, up_box.points, 1)

        elif down_box.position[0] <= up_box.barycentre[0]:
            up_box.angle += 1
            up_box.calcul_rotation()
            pygame.draw.lines(screen, color_red, False, up_box.points, 1)


def init():
    pygame.init()
    pygame.display.update()


def main():

    init()

    scene = Scene()

    box1 = Box((50, 50), 1000)
    box2 = Box((90, 50),10000)
    #box3 = Box((132, 50),100000)
    box4 = Box((800, 50), 10000)

    ground1 = Ground((0, 760))

    scene.add_box(box1)
    scene.add_box(box2)
    #scene.add_box(box3)
    scene.add_box(box4)

    scene.add_ground(ground1)

    angle = 0

    box2.draw()
    angle += 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        scene.calcul_collision()
        scene.draw_scene()
        pygame.display.update()

main()