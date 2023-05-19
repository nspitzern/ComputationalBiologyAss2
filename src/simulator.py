import os
import statistics
import numpy as np
import matplotlib.pyplot as plt
from string import punctuation
from typing import Dict, List, Set, Tuple
from datetime import datetime
from src.evolver import Evolver
from src.files_parser import parse_dict, parse_encoded, parse_letters_freq
from src.generator import generate_random
from src.sample import Sample
from src.selector import Selector
from src.decoder import Decoder
from src.fitness import check_words_in_dict_ratio
from src.scheduler import Scheduler


OUTPUT_DIR_PATH = 'output'


class Simulator:
    def __init__(self, num_samples: int, fitness_goal: float, mutation_percentage: float = 0.5, elite_percentage: float = 0.75) -> None:
        self.enc = parse_encoded('enc.txt')
        self.dictionary: Set[str] = set(parse_dict('dict.txt'))
        freq_1_letter: Dict[str, float] = parse_letters_freq('Letter_Freq.txt')
        freq_2_letter: Dict[str, float] = parse_letters_freq('Letter2_Freq.txt')

        self.__letters = list(sorted(freq_1_letter.keys()))
        self.__fitness_goal: float = fitness_goal
        self.__evolver: Evolver = Evolver(self.__letters)
        self.__scheduler = Scheduler(mutation_percentage, decay=1e-3, min_val=0.2)
        self.__num_samples = num_samples
        self.__mutation_percentage = mutation_percentage
        self.__elite_percentage = elite_percentage

        self.__count_fitness_calls = 0

    def __plot_current(self, round_worst, round_average, round_best):
        plt.plot(round_worst)
        plt.plot(round_average)
        plt.plot(round_best)
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
                new_samples.append(Sample(self.__letters, decode_letters=o))

            samples_len += len(co)

        return new_samples

    def __save(self, samples: List[Sample], dec: List[str], fitness_scores: List[float], generations: int) -> None:
        i = np.argmax(fitness_scores)
        best = samples[i]

        if not os.path.exists(OUTPUT_DIR_PATH):
            os.mkdir(OUTPUT_DIR_PATH)

        filename = os.path.join(OUTPUT_DIR_PATH, f'dec_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt')
        with open(filename, '+wt', encoding='utf-8') as f:
            f.write(f'sample size: {self.__num_samples}{os.linesep}')
            f.write(f'fitness score: {fitness_scores[i] * 100:.3f}{os.linesep}')
            f.write(f'fitness calls: {self.__count_fitness_calls}{os.linesep}')
            f.write(f'generations: {generations}{os.linesep}')
            f.write(f'elite percentage: {self.__elite_percentage}{os.linesep}')
            f.write(f'initial mutation rate: {self.__mutation_percentage}{os.linesep}')
            f.write(f'minimum mutation rate: {self.__scheduler.min_val}{os.linesep}')
            f.write(f'mutation decay: {self.__scheduler.decay}{os.linesep}')
            f.write(f'letters: {self.__letters}{os.linesep}')
            f.write(f'dec: {best.decode_letters}{os.linesep}')
            f.writelines(dec[i])

        plt.savefig(os.path.join(OUTPUT_DIR_PATH, f'plot_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png'), format='png')

    def __decode(self, samples: List[Sample]) -> Tuple[List[str], List[List[str]]]:
        dec = [Decoder.decode_words(self.enc, s.dec_map_int) for s in samples]
        dec_words = [d.strip().translate(str.maketrans('', '', punctuation)).split(' ') for d in dec]
        return dec, dec_words
    
    def __fitness(self, dec_words: List[List[str]]) -> List[float]:
        return [check_words_in_dict_ratio(dec, self.dictionary) for dec in dec_words]

    def __add_current_iteration_data(self, fitness_scores: List[float], 
                                     round_worst: List[float], round_average: List[float], 
                                     round_best: List[float]):
        round_worst.append(min(fitness_scores) * 100)
        round_average.append(statistics.mean(fitness_scores) * 100)
        round_best.append(max(fitness_scores) * 100)

    def run(self):
        round_worst = []
        round_average = []
        round_best = []
        # mutation_amount = int(self.__num_samples * self.__mutation_percentage)
        step = 0

        plt.title(f'Initial mutation percentage: {self.__mutation_percentage * 100}%, elite selection: {self.__elite_percentage * 100}%')
        
        # Generate initial population
        samples: List[Sample] = generate_random(self.__letters, self.__num_samples)
        
        # Compute fitness
        dec, dec_words = self.__decode(samples)
        fitness_scores = self.__fitness(dec_words)
        
        self.__add_current_iteration_data(fitness_scores, round_worst, round_average, round_best)
        self.__plot_current(round_worst, round_average, round_best)

        while all(fitness_score < self.__fitness_goal for fitness_score in fitness_scores):
            # Selection
            elite_samples = Selector.select_elite(samples, fitness_scores, self.__elite_percentage)
            
            # Crossover
            samples = self.__generate_crossovers(samples, fitness_scores, self.__num_samples - len(elite_samples))
            samples.extend(elite_samples)
            
            # Mutation
            mutation_prob = self.__scheduler.calculate(step)
            mutation_amount = int(self.__num_samples * mutation_prob)

            for i in Selector.choose_n_random(samples, mutation_amount):
                s = samples[i]
                _, c1, c2 = self.__evolver.mutate(s.dec_map)
                s.swap(c1, c2)
            
            # Compute fitness
            dec, dec_words = self.__decode(samples)
            fitness_scores = self.__fitness(dec_words)
            
            self.__add_current_iteration_data(fitness_scores, round_worst, round_average, round_best)
            self.__plot_current(round_worst, round_average, round_best)

            print(f'Best: {max(fitness_scores) * 100}%, Worst: {min(fitness_scores) * 100}%, Mean: {statistics.mean(fitness_scores) * 100}%')
            self.__count_fitness_calls += len(dec_words)
            print(f'fitness calls: {self.__count_fitness_calls}')
            print(f'generation: {step}')
            print(f'Current Mutation rate: {mutation_prob}')

            step += 1

        self.__save(samples, dec, fitness_scores, step)

    def run_multiple(self, num_runs):
        best_results = dict()

        for i in range(num_runs):
            fitnesses, samples = self.run()

            best_results[i] = {
                'fitness': fitnesses,
                'samples': samples
            }

        best_fitness = 0
        best_samples = None

        for i in range(num_runs):
            fitnesses = best_results[i]['fitness']

            if max(fitnesses) >= best_fitness:
                best_fitness = fitnesses
                best_samples = best_results[i]['samples']

        dec, dec_words = self.__decode(best_samples)

        self.__save(best_samples, dec, best_fitness, len(best_fitness))

