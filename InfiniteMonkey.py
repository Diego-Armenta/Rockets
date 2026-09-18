import math
import random
import string
from math import floor

Alphabet = list(string.ascii_letters + string.digits + string.punctuation + " ")

population_Pool = []
POP_COUNT = 1000

target_String = input("what is your target String? ")
GENE_COUNT = len(target_String)
GEN_NUM = 0
MUTATION_RATE = 0.01

target_Bred = False

#creates new phrases and checks how similar they are to target (fitness)
class DNA:
    def __init__(self, length):
        self.length = length
        self.genes = []
        self.fitness = 0

        for i in range(self.length):
            self.genes.append(random.choice(Alphabet))

    def calculateFitness(self):
        score = 0
        for i in range(0, self.length):
            if self.genes[i] == target_String[i]:
                score += 1
        self.fitness = 2**score
        return self.fitness



    


for i in range (POP_COUNT):
    phrase = DNA(GENE_COUNT)
    population_Pool.append(phrase)



def draw():
    global target_Bred
    global GEN_NUM

    GEN_NUM += 1
    #array of phrases showing up n times, n being proportional to fitness
    mating_Pool = []

    # print out generation
    for phrase in population_Pool:
        print(''.join(phrase.genes))
        n = floor(phrase.calculateFitness()*100)

        for i in range(n):
            mating_Pool.append(phrase)

    for i in range(len(population_Pool)):
        if ''.join(population_Pool[i].genes) == target_String:
            print("BEHOLD: " + ''.join(population_Pool[i].genes) + "\nThis took " + str(GEN_NUM) + " generations to breed")
            target_Bred = True
            return
        parentA = random.choice(mating_Pool)
        parentB = random.choice(mating_Pool)

        child = cross(parentA, parentB)
        population_Pool[i] = child


def cross(parentA, parentB):
    child = DNA(GENE_COUNT)
    i = random.randint(0,GENE_COUNT-1)
    who_First = random.random()

    if who_First > .5:
        for j in range(i):
            child.genes[j] = parentA.genes[j]

        for j in range(i, GENE_COUNT):
            child.genes[j] = parentB.genes[j]
    else:
        for j in range(i):
            child.genes[j] = parentB.genes[j]

        for j in range(i, GENE_COUNT):
            child.genes[j] = parentA.genes[j]

    child = mutate(child)

    return child

def mutate(child):
    mut_Chance = random.random()
    for i in range(child.length):
        if mut_Chance < MUTATION_RATE:
            child.genes[i] = random.choice(Alphabet)
    return child

while not target_Bred:
    draw()
