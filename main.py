from src.simulator import Simulator


if __name__ == '__main__':
    simulator: Simulator = Simulator(50, 0.95)
    simulator.run()
