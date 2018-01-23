import pygame
import sys
import math
from random import randint

screen = pygame.display.set_mode((1024, 768))

g = (0, 2)


class Particle:
    def __init__(self, position, masse):
        self.position = position
        self.vitesse = (0, 0)
        self.masse = masse
        self.acceleration = (0, 0)
        self.color = (0,255,0)

    def calcul_vitesse(self):
        self.vitesse = (self.vitesse[0] + self.acceleration[0], self.vitesse[1] + self.acceleration[1])

    def calcul_position(self):
        x = self.position[0] + self.vitesse[0]
        y = self.position[1] + self.vitesse[1]
        self.position = (x, y)

    def calcul_acceleration(self):
        self.acceleration = (self.masse * g[0], self.masse * g[1])

    def draw(self):
        if self.position[0] > 1024:
            self.vitesse = (-self.vitesse[0], self.vitesse[1])
        if self.position[0] < 0:
            self.vitesse = (-self.vitesse[0], self.vitesse[1])

        if self.position[1] > 768:
            self.vitesse = (self.vitesse[0], -self.vitesse[1])

        else:
            self.calcul_acceleration()
            self.calcul_vitesse()

        self.calcul_position()

        pygame.draw.circle(screen, self.color, self.position, 5, 3)


class Scene:
    def __init__(self, nb_particles):
        self.particles = []
        for i in range(0, nb_particles):
            rand_v_x = randint(0,100)
            rand_v_y = randint(0,100)
            rand_v_x_signe = randint(-1,1)
            rand_v_y_signe = randint(-1, 1)
            rand_r = randint(0, 255)
            rand_g = randint(0, 255)
            rand_b = randint(0, 255)
            rand_x = randint(0, 1024)
            rand_y = randint(0, 768)
            rand_masse = randint(1, 2)
            p = Particle((rand_x, rand_y), rand_masse)
            p.color = (rand_r, rand_g, rand_b)
            p.vitesse = (rand_v_x_signe * rand_v_x, rand_v_y_signe * rand_v_y)
            self.particles.append(p)

    def draw(self):
        screen.fill((0, 0, 0))
        for p in self.particles:
            p.draw()


def init():
    pygame.init()
    pygame.display.update()


def main():

    init()
    scene = Scene(500)

    while True:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        scene.draw()
        pygame.display.update()

main()
