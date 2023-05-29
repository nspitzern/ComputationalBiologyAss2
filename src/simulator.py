import os
import statistics
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Set
from datetime import datetime

from src.fitness import check_words_in_dict_ratio
from src.memory import Memory
from src.decoder import Decoder
from src.evolver import Evolver
from src.files_parser import parse_dict, parse_encoded, parse_letters_freq
from src.generator import generate_random
from src.sample import Sample
from src.selector import Selector
from src.scheduler import Scheduler
from src.strategy import GeneticAlgorithmType


OUTPUT_DIR_PATH = 'output'


class MutationArgs:
    def __init__(self, mutation_percentage: float, mutation_decay: float, mutation_min_percentage: float) -> None:
        self.mutation_percentage = mutation_percentage
        self.mutation_decay = mutation_decay
        self.mutation_min_percentage = mutation_min_percentage


class SimulationArgs:
    def __init__(self, fitness_goal: float, elite_percentile: float, 
                 mutation_percentage: float, mutation_decay: float, mutation_min_percentage: float,
                 generation_tolerance: int, generation_tolerance_percentage: float) -> None:
        self.fitness_goal = fitness_goal
        self.elite_percentile = elite_percentile
        self.mutation = MutationArgs(mutation_percentage, mutation_decay, mutation_min_percentage)

        self.generation_tolerance = generation_tolerance
        self.generation_tolerance_percentage = generation_tolerance_percentage * 100


class SimulationHistory:
    def __init__(self) -> None:
        self.__worst: List[float] = []
        self.__average: List[float] = []
        self.__best: List[float] = []

    @property
    def worst(self) -> List[float]:
        return self.__worst
    
    @property
    def average(self) -> List[float]:
        return self.__average
    
    @property
    def best(self) -> List[float]:
        return self.__best
    
    def add(self, worst, average, best) -> None:
        self.__worst.append(worst)
        self.__average.append(average)
        self.__best.append(best)
    
    def last_n_best_change(self, n: int) -> float:
        last_n = self.__best[-n:]
        return max(last_n) - min(last_n)

    def __len__(self):
        return len(self.__average)


class Simulator:
    def __init__(self, algo_type: GeneticAlgorithmType, num_samples: int, simulation_args: SimulationArgs) -> None:
        self.enc = parse_encoded('enc.txt')
        self.dictionary: Set[str] = set(parse_dict('dict.txt'))
        freq_1_letter: Dict[str, float] = parse_letters_freq('Letter_Freq.txt')
        freq_2_letter: Dict[str, float] = parse_letters_freq('Letter2_Freq.txt')

        self.__args: SimulationArgs = simulation_args
        self.__letters = list(sorted(freq_1_letter.keys()))
        self.__fitness_goal: float = simulation_args.fitness_goal
        self.__evolver: Evolver = Evolver(self.__letters)
        self.__scheduler = Scheduler(simulation_args.mutation.mutation_percentage, 
                                     decay=simulation_args.mutation.mutation_decay, 
                                     min_val=simulation_args.mutation.mutation_min_percentage)
        self.__memory = Memory()
        self.algo_type = algo_type
        self.__strategy = GeneticAlgorithmType.get_strategy(algo_type, self.dictionary, self.enc, self.__letters, freq_1_letter, freq_2_letter)
        self.__num_samples = num_samples
        self.__elite_percentile = simulation_args.elite_percentile

    def __should_run(self, step: int, history: SimulationHistory, 
                     fitness_scores: List[float], fitness_goals: Dict[int, float] = None):
        if fitness_goals:
            max_fitness = max(fitness_scores)
            for k, v in sorted(fitness_goals.items(), reverse=True):
                if step >= k and max_fitness < v:
                    return False

        tolerance = self.__args.generation_tolerance
        if step > tolerance and history.last_n_best_change(tolerance) < self.__args.generation_tolerance_percentage:
            return False

        return max(fitness_scores) < self.__fitness_goal

    def __plot_current(self, history: SimulationHistory):
        plt.plot(history.worst)
        plt.plot(history.average)
        plt.plot(history.best)
        plt.xlabel('Generation number')
        plt.ylabel('Fitness Score %')
        plt.draw()
        plt.pause(0.01)

    def __generate_crossovers(self, samples: List[Sample], fitness_scores: List[float], n: int) -> List[Sample]:
        """
        Generate n crossovers from given elite samples.

        Args:
            elite_samples (List[Sample]): samples on which to generate crossovers
            n (int): number of samples to generate

        Returns:
            List[Sample]: valid crossover samples
        """
        new_samples: List[Sample] = []
        samples_len = 0

        while samples_len < n:
            co = self.__evolver.generate_pmx_crossover(samples, fitness_scores)

            for o in co:
                if o not in self.__memory:
                    new_samples.append(Sample(self.__letters, decode_letters=o))
                    self.__memory.add(o)

            samples_len += len(co)

        return new_samples

    def __save(self, samples: List[Sample], dec: List[str], fitness_scores: List[float], generations: int, run_num: int = 0) -> None:
        i = np.argmax(fitness_scores)
        best = samples[i]

        if not os.path.exists(OUTPUT_DIR_PATH):
            os.mkdir(OUTPUT_DIR_PATH)

        filename = os.path.join(OUTPUT_DIR_PATH, f'dec_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt')
        with open(filename, '+wt', encoding='utf-8') as f:
            f.write(f'run number: {run_num + 1}{os.linesep}')
            f.write(f'strategy: {GeneticAlgorithmType.map_to_str(self.algo_type)}{os.linesep}')
            f.write(f'sample size: {self.__num_samples}{os.linesep}')
            f.write(f'fitness score: {fitness_scores[i] * 100:.3f}{os.linesep}')
            f.write(f'fitness calls: {self.__strategy.fitness_calls}{os.linesep}')
            f.write(f'generations: {generations}{os.linesep}')
            f.write(f'elite percentage: {self.__elite_percentile}{os.linesep}')
            f.write(f'initial mutation rate: {self.__args.mutation.mutation_percentage}{os.linesep}')
            f.write(f'minimum mutation rate: {self.__scheduler.min_val}{os.linesep}')
            f.write(f'mutation decay: {self.__scheduler.decay}{os.linesep}')
            f.write(f'letters: {self.__letters}{os.linesep}')
            f.write(f'dec: {best.decode_letters}{os.linesep}')
            f.writelines(Decoder.decode_words(self.enc, best.dec_map_int))

        plt.savefig(os.path.join(OUTPUT_DIR_PATH, f'plot_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png'), format='png')

    def __add_current_iteration_data(self, fitness_scores: List[float], 
                                     history: SimulationHistory):
        worst: float = min(fitness_scores) * 100
        average: float = statistics.mean(fitness_scores) * 100
        best: float = max(fitness_scores) * 100
        history.add(worst, average, best)

    def __step(self, step: int, samples: List[Sample], fitness_scores: List[float]):
        # Selection
        elite_samples = Selector.select_elite(samples, fitness_scores, self.__elite_percentile)
        
        # Crossover
        samples = self.__generate_crossovers(samples, fitness_scores, self.__num_samples - len(elite_samples))
        
        # Mutation
        mutation_prob = self.__scheduler.calculate(step)
        mutation_amount = int(len(samples) * mutation_prob)

        for i in Selector.choose_n_random(samples, mutation_amount):
            s = samples[i]
            mutation, swaps = self.__evolver.swap_mutation(s.dec_map)
            if mutation not in self.__memory:
                s.swap(swaps)
                self.__memory.add(mutation)

        samples.extend(elite_samples)
        # Compute fitness
        fitness_scores = self.__strategy.fitness(samples)

        print(f'Current Mutation rate: {mutation_prob}')

        return samples, fitness_scores

    def run(self, fitness_goals: Dict[int, float] = None):
        history: SimulationHistory = SimulationHistory()
        step = 0

        plt.title(f'Initial mutation percentage: {self.__args.mutation.mutation_percentage * 100}%, elite percentile: {self.__elite_percentile * 100}%')
        
        # Generate initial population
        samples: List[Sample] = generate_random(self.__letters, self.__num_samples)
        
        # Compute fitness
        fitness_scores = self.__strategy.fitness(samples)
        
        self.__add_current_iteration_data(fitness_scores, history)
        self.__plot_current(history)

        while self.__should_run(step, history, fitness_scores, fitness_goals):
            step_func = lambda s, f: self.__step(step, s, f)
            samples, fitness_scores = self.__strategy.activate(step_func, samples, fitness_scores)
            
            self.__add_current_iteration_data(fitness_scores, history)
            self.__plot_current(history)

            print(f'Best: {max(fitness_scores) * 100}%, Worst: {min(fitness_scores) * 100}%, Mean: {statistics.mean(fitness_scores) * 100}%')
            print(f'fitness calls: {self.__strategy.fitness_calls}')
            print(f'generation: {step}')

            step += 1

        plt.cla()
        return fitness_scores, samples, history

    def run_multiple(self, num_runs, **kwargs):
        best_fitness = [0]
        best_samples = []
        best_history = SimulationHistory()

        for i in range(num_runs):
            fitnesses, samples, history = self.run(**kwargs)

            if max(fitnesses) > max(best_fitness):
                best_fitness = fitnesses
                best_samples = samples
                best_history = history

                if max(best_fitness) >= self.__fitness_goal:
                    break

        dec, dec_words = self.__strategy.decode(best_samples)
        print(f'Best Words Fitness: {100 * max([check_words_in_dict_ratio(dec, self.dictionary) for dec in dec_words])}%')

        self.__plot_current(best_history)
        self.__save(best_samples, dec, best_fitness, len(best_history), run_num=i)
