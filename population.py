from plane import Point, Vector, Line
from lander import ControlCommands, State, FlyState, Lander
from motion import Speed, Particle
from chromosome import Chromosome
import matplotlib.pyplot as plt
from collections import namedtuple
from copy import deepcopy
import numpy as np
import math

CMD_TUPLE = namedtuple("Command", ["angle", "power"])


def coerce_range(value, min_value, max_value):
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value


def ground_inputs_to_line(ground_points):
    points = []
    for point in ground_points:
        points.append(Point(*map(int, point.split())))
    return Line(points)


class Population():
    """A class to describe a population, where each member
    is an instance of a chromosome class
    """
    def __init__(self, gene_size, mutation_rate, pop_size):
        self.population_size = pop_size
        self.population = []  # List to store the current population
        self.population_fitness = []  # List to store fit score for each member
        self.parents = []  # List from which we choose parents to create childs
        self.probability = []  # Probability of each parent to be choosen
        self.generations = 0
        self.evolved = False  # Are we finished evolving
        self.mutation_rate = mutation_rate
        self.best_phrase = ""  # The current member with highest fitness score
        self.gene_size = gene_size
        self.simulations = []  # all simulations for current population
        self.ground_points = []
        self.all_simulations = []
        # ratio of best chromosomes in current population
        # that we copy into new population
        self.elitism_ratio = 0.1

        for _ in range(self.population_size):
            self.population.append(Chromosome(gene_size))

    def __str__(self):
        info = f"\nTotal generations: {self.generations}"
        info += f"\nPopulation size: {self.population_size}"
        info += f"\nMutation rate: {math.floor(self.mutation_rate * 100)}%"
        info += f"\nPopulation max fitness score: {self.get_max_fitness():.2f}"
        return info

    def simulate(self, init_position, fuel, ground_points):
        """From each chromosome in population we create object
        of Lander class and compute trajectory
        """
        x, y = init_position[0], init_position[1]
        lander_init_state = State(fuel, 0, 0, Particle(Point(x, y),
                                  Speed(Vector(0, 0))))
        ground_line = ground_inputs_to_line(ground_points)
        self.ground_points = ground_line
        self.simulations = []
        for member in self.population:
            commands = []
            previous_gene = CMD_TUPLE(0, 0)
            for gene in member.genes:
                angle = previous_gene.angle + coerce_range(
                    gene.angle - previous_gene.angle, -15, 15)
                power = previous_gene.power + coerce_range(
                    gene.power - previous_gene.power, -15, 15)
                commands.append(ControlCommands(angle, power))
                previous_gene = gene

            new_lander = Lander(lander_init_state, commands, ground_line)
            self.simulations.append(new_lander)
        self.all_simulations.append(deepcopy(self.simulations))

    def display_all_populations_simulation(self):
        """Plot trajectory of every chromosome of population
        for all generations
        """
        plt.ion()
        plt.title(f"Simulation of generation - {self.generations}")
        for simulations in self.all_simulations:
            plt.clf()
            x, y = [], []
            for point in self.ground_points.points:
                x.append(point.x)
                y.append(point.y)
            plt.plot(x, y)

            for simulation in simulations:
                x, y = [], []
                for state in simulation.trajectory:
                    x.append(state.position.x)
                    y.append(state.position.y)
                plt.plot(x, y)

            plt.xlim([0, 7000])
            plt.ylim([0, 3000])
            plt.draw()
            plt.pause(0.01)

    def calculate_fitness(self):
        """calculate fitness function for every chromosome in population"""
        self.population_fitness = []
        for simulation, member in zip(self.simulations, self.population):
            member.fitness = simulation.fitness
            self.population_fitness.append(member.fitness)

    def selection(self):
        """Create parents array and probability array
        each element (normilized probability based on fitness score)
        """
        self.parents = []
        self.probability = []
        max_fitness = max(self.population_fitness)
        total_fitness = 0.0

        # Based on fitness score calculate probability
        # for each parent to be choosen:
        # a higher fitness score = higher probability to be picked as a parent
        # a lower fitness score = lower probability to be picked as a parent
        for member in self.population:
            if member.fitness > 0:
                self.parents.append(member)
                normalized_fitness = member.fitness / max_fitness
                self.probability.append(normalized_fitness)
                total_fitness += normalized_fitness

        for i in range(len(self.probability)):
            normalized_probability = self.probability[i] / total_fitness
            self.probability[i] = normalized_probability

    def next_generation(self):
        """Create a new generation using crossover and mutation on parents"""
        new_population = []
        for i in range(self.population_size // 2):
            parent_a = np.random.choice(self.parents, p=self.probability)
            parent_b = np.random.choice(self.parents, p=self.probability)

            child1, child2 = parent_a.crossover(parent_b)
            child1.mutate(self.mutation_rate)
            child2.mutate(self.mutation_rate)
            new_population.extend([child1, child2])

        # Copy best members from current population to the new population
        # based on elitism ratio
        pop_sort_by_fitness = sorted(self.population,
                                     key=lambda x: x.fitness, reverse=True)
        for j in range(int(self.population_size * self.elitism_ratio)):
            new_population[j] = pop_sort_by_fitness[j]

        self.population = new_population
        self.generations += 1

    def landing_zone_reached(self):
        """Did any lander in simulations landed in landing zone?"""
        for simulation in self.simulations:
            if simulation.flystate == FlyState.Landed:
                self.evolved = True
                break

    def get_max_fitness(self):
        """Find highest fitness score for the current population"""
        max_fitness = 0
        for member in self.population:
            max_fitness = max(max_fitness, member.fitness)
        return max_fitness
