import random
from collections import namedtuple

CMD_TUPLE = namedtuple("Command", ["angle", "power"])


def coerce_range(value, min_value, max_value):
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value


class Chromosome():
    """A class represents a chromosome as an array
    of pairs(angle, power (thrust))
    - angle : -90, -75, ... , 0, +15, +30, ..., +75, +90
    - power : 0, 1, 2, 3, 4
    - convert chromosome into a string
    - crossover: combine one chromosome with another
    - mutate chromosome
    """
    def __init__(self, gene_size):
        self.genes = []
        self.size = gene_size
        self.fitness = 0

        self.genes.append(CMD_TUPLE(0, 0))  # Init values

        # filling with random angle and power for initial population
        # for each turn the actual value of the angle is limited
        # to the value of the previous turn +/- 15° and power is
        # the value of the previous turn +/-1 (min = 0, max = 4)
        for i in range(1, self.size):
            angle = coerce_range(
                self.genes[i-1].angle + random.randint(-15, 15), -90, 90)
            power = coerce_range(
                self.genes[i-1].power + random.randint(-1, 1), 0, 4)
            self.genes.append(CMD_TUPLE(angle, power))

    def __str__(self):
        info = "Gene sequence (angle, power): "
        info += " ".join(map(lambda x: f"({x[0]}, {x[1]})", self.genes))
        info += "\nFitness score: " + str(self.fitness)
        return info

    def __len__(self):
        return len(self.genes)

    def crossover(self, partner):
        """Combine by taking part from one parent and part from another
        based on weight (random number)
        """
        weight = random.random()
        weight_compl = 1 - weight
        child1 = Chromosome(len(self.genes))
        child2 = Chromosome(len(self.genes))

        for i in range(1, len(self.genes)):
            w_angle = int(self.genes[i].angle * weight
                          + partner.genes[i].angle * weight_compl)
            w_power = int(self.genes[i].power * weight
                          + partner.genes[i].power * weight_compl)
            child1.genes[i] = CMD_TUPLE(w_angle, w_power)

            w_angle = int(self.genes[i].angle * weight_compl
                          + partner.genes[i].angle * weight)
            w_power = int(self.genes[i].power * weight_compl
                          + partner.genes[i].power * weight)
            child2.genes[i] = CMD_TUPLE(w_angle, w_power)
        return (child1, child2)

    def mutate(self, mutation_rate):
        """Change angle and power based on a mutation probability"""
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                new_angle = coerce_range(
                    self.genes[i].angle + random.randint(-15, 15), -90, 90)
                new_power = coerce_range(
                    self.genes[i].power + random.randint(-1, 1), 0, 4)
                self.genes[i] = (CMD_TUPLE(new_angle, new_power))
