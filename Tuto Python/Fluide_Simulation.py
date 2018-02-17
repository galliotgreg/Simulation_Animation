import pygame
import sys
import math
from random import randint

width = 600
height = 600
_max_int = 10000

screen = pygame.display.set_mode((width, height))

deltaTime = 1

k = 0.004
k_spring = 0.3
k_near = 0.01

g = (0, 9)
density_zero = 10


class Particule:
    def __init__(self, pos):
        self.position = pos
        self.past_position = pos
        self.vitesse = (0, 0)
        self.forces = [g]
        self.color = (0, 255, 0)
        self.density = 0
        self.pressure = 0

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), 10, 3)

    def compute_position(self):

        #apply gravity
        #vi ← vi +∆tg
        self.vitesse = (self.vitesse[0] + deltaTime * g[0],
                        self.vitesse[1] + deltaTime * g[1])

        #save previous position
        #x prev i ← x i
        self.past_position = self.position

        #advance to predicted position
        self.position = (self.position[0] + deltaTime * self.vitesse[0],
                         self.position[1] + deltaTime * self.vitesse[1])


        #add spring and modify position according to springs
        self.compute_spring_wall_force()

        self.clamp_position()

        #use previous position to compute next velocity
        #vi ← (xi −x prev i) / ∆t
        self.compute_vitesse()

    def compute_spring_wall_force(self):
        if self.position[1] > height-100:
            distance = compute_distance(self.position, (self.position[0], height-100))
            direction = (0, -1)
            force = (distance * k_spring * direction[0],
                     distance * k_spring * direction[1])
            self.position = (self.position[0] + force[0],
                             self.position[1] + force[1])

        if self.position[0] > width - 10:
            distance = compute_distance(self.position, (width - 10, self.position[1]))
            direction = (-1, 0)
            force = (distance * k_spring * direction[0],
                     distance * k_spring * direction[1])
            self.position = (self.position[0] + force[0],
                             self.position[1] + force[1])

        if self.position[0] < 10:
            distance = compute_distance(self.position, (10, self.position[1]))
            direction = (1, 0)
            force = (distance * k_spring * direction[0],
                     distance * k_spring * direction[1])
            self.position = (self.position[0] + force[0],
                             self.position[1] + force[1])

    def compute_vitesse(self):
        self.vitesse = ((self.position[0] - self.past_position[0]),
                        (self.position[1] - self.past_position[1]))

    def clamp_position(self):
        self.position = (float_to_int_clamp(self.position[0]),
                         float_to_int_clamp(self.position[1]))


class Scene:
    def __init__(self, nb_particules, nb_colonne):
        self.particles = []
        self.grid = {}
        self.grid_step = width // nb_colonne

        for i in range(0, nb_particules):
            self.create_particle()

    def create_particle(self):
        x = randint(0, width)
        y = randint(0, height)
        particle = Particule((x, y))
        self.particles.append(particle)
        x = (particle.position[0] // self.grid_step)
        y = (particle.position[1] // self.grid_step)
        self.grid.setdefault((x, y), []).append(particle)
        self.particles.append(particle)

    def compute_double_density_relaxation(self,r):
        for particle1 in self.particles:
            density = 0
            density_near = 0

            x = particle1.position[0] // self.grid_step
            y = particle1.position[1] // self.grid_step

            #compute density and near - density
            for i in range(-1, 2):
                for j in range(-1, 2):
                    list_res = self.grid.setdefault((x + i, y + j), [])
                    for particle2 in list_res:
                        if particle1 is not particle2:
                            if compute_distance(particle1.position, particle2.position) <= r:
                                q = compute_distance(particle1.position, particle2.position) / r
                                if q < 1:
                                    density += (1-q)**2
                                    density_near += (1-q)**3

            #compute pressure and near-pressure
            pressure = k * (density - density_zero)
            pressure_near = k_near * density_near
            particle1.pressure = pressure_near
            dx = (0, 0)
            for i in range(-1, 2):
                for j in range(-1, 2):
                    list_res = self.grid.setdefault((x + i, y + j), [])
                    for particle2 in list_res:
                        if particle1 is not particle2:
                            if compute_distance(particle1.position, particle2.position) <= r:
                                q = compute_distance(particle1.position, particle2.position) / r
                                direction = compute_direction(particle1.position, particle2.position)
                                if q < 1:
                                    displacement = (deltaTime**2 * (pressure * (1-q) + pressure_near * (1-q)**2) * direction[0],
                                                    deltaTime**2 * (pressure * (1-q) + pressure_near * (1-q)**2) * direction[1]
                                                    )
                                    particle2.position = (particle2.position[0] + displacement[0]//2,
                                                          particle2.position[1] + displacement[1]//2)
                                    dx = (dx[0] - displacement[0]//2,
                                          dx[1] - displacement[1]//2)

            particle1.position = (particle1.position[0] + dx[0],
                                  particle1.position[1] + dx[1])
            particle1.color = (
                min(int(1 * abs(particle1.pressure) * 5000), 255),
                min(int(1 * abs(particle1.pressure) * 2500), 255),
                min(int(1 * abs(particle1.pressure) * 500), 255))

    def draw_grid(self):
        for i in range(0, width, self.grid_step):
            pygame.draw.lines(screen, (255, 255, 255), False, [(i, 0), (i, height)], 1)
            pygame.draw.lines(screen, (255, 255, 255), False, [(0, i), (width, i)], 1)

    def draw(self):
        screen.fill((25, 25, 112))
        self.draw_grid()
        for particle in self.particles:
            particle.compute_position()
        self.compute_double_density_relaxation(100)
        for particle in self.particles:
            particle.draw()
            print(particle.position)


def compute_distance(p1, p2):
    distance = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
    return distance


def compute_norme(p):
    norme = math.sqrt(p[0]**2 + p[1]**2)
    if norme == 0:
        norme = 1
    return norme


def compute_direction(p1, p2):
    res = (p2[0] - p1[0], p2[1] - p1[1])
    norme = compute_norme(res)
    res_norm_x = (res[0] / norme)
    res_norm_y = (res[1] / norme)

    res_norm = (res_norm_x, res_norm_y)
    return res_norm


def float_to_int_clamp(nb):
    return min(int(nb), _max_int)


def init():
    pygame.init()
    pygame.display.update()


def main():
    init()
    scene = Scene(100, 10)

    while True:
        pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        scene.draw()
        pygame.display.update()

main()
