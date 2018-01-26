import pygame
import sys
import math
from random import randint

width = 600
height = 600
_max_int = 10000

screen = pygame.display.set_mode((width, height))

deltaTime = 50

k_spring = 0.25

g = (0, 9)


class Particule:
    def __init__(self, pos):
        self.position = pos
        self.past_position = pos
        self.vitesse = (0, 0)
        self.forces = [g]
        self.color = (255, 255, 255)

    def draw(self):
        print("Draw")
        print(self.position)
        self.compute_position()
        pygame.draw.circle(screen, self.color, self.position, 5, 3)

    def compute_position(self):
        print("Compute Position")

        #apply gravity
        #vi ← vi +∆tg
        self.vitesse = (self.vitesse[0] + (deltaTime/50) * g[0],
                        self.vitesse[1] + (deltaTime/50) * g[1])

        #save previous position
        #x prev i ← x i
        self.past_position = self.position

        #advance to predicted position
        self.position = (self.position[0] + (deltaTime/50) * self.vitesse[0],
                         self.position[1] + (deltaTime/50) * self.vitesse[1])


        #add spring and modify position according to springs
        self.compute_spring_wall_force()

        self.clamp_position()

        #use previous position to compute next velocity
        #vi ← (xi −x prev i) / ∆t
        self.compute_vitesse()

    def compute_spring_wall_force(self):
        print("Compute Spring")
        if self.position[1] > height-100:
            distance = compute_distance(self.position, (self.position[0], height-100))
            direction = (0, -1)
            force = (distance * k_spring * direction[0], distance * k_spring * direction[1])
            self.position = (self.position[0] + force[0], self.position[1] + force[1])

        if self.position[0] > width - 10:
            distance = compute_distance(self.position, (width - 10, self.position[1]))
            direction = (-1, 0)
            force = (distance * k_spring * direction[0], distance * k_spring * direction[1])
            self.position = (self.position[0] + force[0], self.position[1] + force[1])

        if self.position[0] < 10:
            distance = compute_distance(self.position, (10, self.position[1]))
            direction = (1, 0)
            force = (distance * k_spring * direction[0], distance * k_spring * direction[1])
            self.position = (self.position[0] + force[0], self.position[1] + force[1])

    def compute_vitesse(self):
        print("Compute Vitesse")
        self.vitesse = ((self.position[0] - self.past_position[0]),
                        (self.position[1] - self.past_position[1]))
        print(self.vitesse)

    def clamp_position(self):
        self.position = (float_to_int_clamp(self.position[0]),
                         float_to_int_clamp(self.position[1]))


class Scene:
    def __init__(self, nb_particules, nb_colonne):
        self.particules = []
        self.grid = {}
        self.grid_step = width // nb_colonne

        for i in range(0, nb_particules):
            self.create_particule()

    def create_particule(self):
        x = randint(0, width)
        y = randint(0, height)
        v_x = randint(-5, 5)
        v_y = randint(-5, 5)
        particule = Particule((x, y))
        particule.vitesse = (v_x, v_y)
        self.particules.append(particule)

    def draw(self):
        screen.fill((0, 0, 0))
        for particule in self.particules:
            particule.draw()


def compute_distance(p1, p2):
    distance = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
    return distance


def float_to_int_clamp(nb):
    return min(int(nb), _max_int)


def init():
    pygame.init()
    pygame.display.update()


def main():
    init()
    scene = Scene(1000, 10)

    while True:
        pygame.time.delay(deltaTime)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        scene.draw()
        pygame.display.update()

main()
