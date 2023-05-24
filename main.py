from src.simulator import Simulator, SimulationArgs, GeneticAlgorithmType

if __name__ == '__main__':
    args: SimulationArgs = SimulationArgs(0.97, elite_percentile=0.9, mutation_percentage=0.1,
                                          mutation_decay=1e-3, mutation_min_percentage=0.1, 
                                          generation_tolerance=50, generation_tolerance_percentage=0.01)
    simulator: Simulator = Simulator(GeneticAlgorithmType.DARWIN , 100, args)

    dict = {}
    simulator.run_multiple(num_runs=50, **dict)
