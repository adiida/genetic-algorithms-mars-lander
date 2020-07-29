from population import Population


def init():
    gene_size = 100
    mutation_rate = 0.08
    pop_size = 200
    population = Population(gene_size, mutation_rate, pop_size)
    ground_points = ["0 100", "1000 500", "1500 1500", "3000 1000",
                     "4000 150", "5500 150", "6999 800"]
    init_position = (2500, 2700)
    fuel = 5000

    # Compute trajectories and lander state,
    # for every member of the initial population
    population.simulate(init_position, fuel, ground_points)

    # Calculate fitness score for every member of the intial population
    population.calculate_fitness()

    return population


def evolve(population):
    """Find trajectory to the landing zone"""
    ground_points = ["0 100", "1000 500", "1500 1500", "3000 1000",
                     "4000 150", "5500 150", "6999 800"]
    init_position = (2500, 2700)
    fuel = 5000

    while(not population.evolved):
        # Generate parents array
        population.selection()

        # Create next generation
        population.next_generation()

        # Compute trajectories and lander state,
        # for every member of the population
        population.simulate(init_position, fuel, ground_points)

        # Calculate fitness score for every member of the population
        population.calculate_fitness()

        # Check if any of the landers reached the landing zone
        population.landing_zone_reached()

        print(population)

    # Plot the trajectory of every member of all populations
    population.display_all_populations_simulation()


def main():
    population = init()
    evolve(population)


if __name__ == "__main__":
    main()
