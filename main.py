import argparse

from src.simulator import Simulator, SimulationArgs, GeneticAlgorithmType


def main(n_iter: int, alg: GeneticAlgorithmType, population_size: int, fitness_goal: float):
    args: SimulationArgs = SimulationArgs(fitness_goal, elite_percentile=0.9, mutation_percentage=0.2,
                                          mutation_decay=1e-3, mutation_min_percentage=0.2,
                                          generation_tolerance=50, generation_tolerance_percentage=0.01)
    simulator: Simulator = Simulator(alg, population_size, args)

    dict = {}
    simulator.run_multiple(num_runs=n_iter, **dict)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', help='Set number of iterations to run (>1)', default=10, type=int)
    parser.add_argument('-ps', help='Set number of population size (>1)', default=300, type=int)
    parser.add_argument('-acc', help='Set the fitness accuracy goal [0-1]', default=0.99, type=float)

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', help='Run regular GA', action='store_true')
    group.add_argument('-d', help='Run darwin GA', action='store_true')
    group.add_argument('-l', help='Run lamarck GA', action='store_true')

    args = parser.parse_args()

    if args.d:
        alg = GeneticAlgorithmType.DARWIN
    elif args.l:
        alg = GeneticAlgorithmType.LAMARCK
    elif args.r:
        alg = GeneticAlgorithmType.REGULAR
    else:
        raise ValueError('Please pick GA to run [-r/-d/-l]')
    main(args.n, alg, args.ps, args.acc)
