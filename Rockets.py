import math
import random

import pygame as p

population_Pool = []
POP_COUNT = 20
MUTATION_RATE = 0.01
LIFESPAN = 100
target = (320, 40)
LIFECOUNT = 0.0


def main():
    p.init()
    screen = p.display.set_mode((800, 600))
    clock = p.time.Clock()
    running = True
    population = Population(MUTATION_RATE, POP_COUNT)
    generation_Num = 1
    font = p.font.SysFont(("Times New Roman"), 30)
    text_Col = (255, 116, 0)
    global target
    global LIFECOUNT
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                target = p.mouse.get_pos()

        screen.fill((19, 24, 126))
        p.draw.circle(screen, (72, 178, 122), target, 20, width=5)
        if LIFECOUNT < LIFESPAN:
            population.live(screen)
            LIFECOUNT += 1
        else:
            LIFECOUNT = 0.0
            population.fitness()
            population.selection()
            population.reproduction()
            generation_Num += 1

        img = font.render(("Generation : " + str(generation_Num)), True, text_Col)
        screen.blit(img, (0,0))

        p.display.flip()
        clock.tick(60)

    p.quit()



#Creates Rockets with a position, velocity and acceleration. Fitness based on how far from target
class Rocket:
    def __init__(self, x, y, DNA):
        self.position = p.Vector2(x,y)
        self.velocity = p.Vector2(0,0)
        self.acceleration = p.Vector2(0,0)
        self.fitness = 0
        self.DNA = DNA
        self.geneCounter = 0

    def applyForce(self, force):
        self.acceleration =+ force

    def update(self):
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration = p.Vector2(0,0)

    def calculateFitness(self):
        distance = math.dist(self.position, target)
        self.fitness = 1/(distance**2)


    def run(self,screen):
        self.applyForce(self.DNA.genes[self.geneCounter])
        self.geneCounter += 1
        self.update()

        def findBase():
            unit_Vector = self.velocity.normalize()
            perp_Left = p.Vector2(-unit_Vector[1], unit_Vector[0])
            perp_Right = p.Vector2(unit_Vector[1], -unit_Vector[0])
            perp_Intercept = self.position + (-20*unit_Vector)

            base_Point1 = perp_Intercept + (5*perp_Left)
            base_Point2 = perp_Intercept + (5*perp_Right)
            return base_Point1, base_Point2

        bases = findBase()

        p.draw.polygon(screen, (136, 23, 148), [bases[0], bases[1], self.position],
                       width=0)  # coord (x-5, y+20) (x+5, y+20)

class DNA:
    def __init__(self):
        self.genes = []
        self.maxForce = 1
        for i in range(LIFESPAN):
            angle = random.uniform(0,2*math.pi)
            magnitude = random.uniform(0,self.maxForce)
            gene = p.Vector2(math.cos(angle), math.sin(angle))*magnitude
            self.genes.append(gene)



class Population:
    def __init__(self, mutation, size):
        self.mutationRate = mutation
        self.population = []
        self.size = size
        for i in range(POP_COUNT):
            new_Rocket = Rocket(320,240, DNA())
            self.population.append(new_Rocket)

    def fitness(self):
        for rocket in self.population:
            rocket.calculateFitness()

    #Normalize fitness
    def selection(self):
        totalFitness = 0
        for rocket in self.population:
            totalFitness += rocket.fitness

        for rocket in self.population:
            rocket.fitness /= totalFitness

    #select
    def weighted_Select(self):
        index = 0
        start = random.random()
        while start > 0:
            start = start - self.population[index].fitness
            index += 1
        index -= 1
        return self.population[index]

    def reproduction(self):
        newPopulation = []
        for i in range(self.size):
            parentA = self.weighted_Select()
            parentB = self.weighted_Select()
            child = self.breed(parentA, parentB)
            childRocket = Rocket(320, 240, child)
            newPopulation.append(childRocket)
        self.population = newPopulation

    def breed(self, parentA, parentB):
        child = DNA()
        i = random.randint(0, LIFESPAN)
        who_First = random.random()

        if who_First > .5:
            for j in range(i):
                child.genes[j] = parentA.DNA.genes[j]

            for j in range(i, LIFESPAN):
                child.genes[j] = parentB.DNA.genes[j]
        else:
            for j in range(i):
                child.genes[j] = parentB.DNA.genes[j]

            for j in range(i, LIFESPAN):
                child.genes[j] = parentA.DNA.genes[j]

        child = self.mutate(child)

        return child

    #Amount of genes is equivalent to LIFESPAN
    def mutate(self, child):
        mut_Chance = random.random()
        for i in range(LIFESPAN):
            if mut_Chance < MUTATION_RATE:
                angle = random.uniform(0, 2 * math.pi)
                magnitude = random.uniform(0, child.maxForce)
                gene = p.Vector2(math.cos(angle) * magnitude, math.sin(angle) * magnitude)
                child.genes.append(gene)
        return child

    def live(self,screen):
        for rocket in self.population:
            rocket.run(screen)

main()
