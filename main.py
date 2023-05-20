from src.simulator import Simulator, SimulationArgs

if __name__ == '__main__':
    args: SimulationArgs = SimulationArgs(1, elite_percentile=0.1, mutation_percentage=0.75, 
                                          mutation_decay=1e-3, mutation_min_percentage=0.05, 
                                          generation_tolerance=10, generation_tolerance_percentage=0.05)
    simulator: Simulator = Simulator(2000, args)

    dict = {}
    simulator.run(dict)
