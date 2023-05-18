from src.simulator import Simulator


if __name__ == '__main__':
    simulator: Simulator = Simulator(10_000, 0.95, mutation_percentage=0.5, elite_percentage=0.75)
    simulator.run()
