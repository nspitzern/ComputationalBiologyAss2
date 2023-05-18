import os
import statistics
import numpy as np
import matplotlib.pyplot as plt
from string import punctuation
from typing import Dict, List, Set
from datetime import datetime
from src.evolver import Evolver
from src.files_parser import parse_dict, parse_encoded, parse_letters_freq
from src.generator import generate_random
from src.memory import Memory
from src.sample import Sample
from src.selector import Selector
from src.decoder import Decoder
from src.fitness import check_words_in_dict_ratio


class Simulator:
    def __init__(self, num_samples: int, fitness_goal: float) -> None:
        self.enc = parse_encoded('enc.txt')
        self.dictionary: Set[str] = set(parse_dict('dict.txt'))
        freq_1_letter: Dict[str, float] = parse_letters_freq('Letter_Freq.txt')
        freq_2_letter: Dict[str, float] = parse_letters_freq('Letter2_Freq.txt')

        self.__letters = list(sorted(freq_1_letter.keys()))
        self.__fitness_goal: float = fitness_goal
        self.__evolver: Evolver = Evolver(self.__letters)
        self.__samples: List[Sample] = generate_random(self.__letters, num_samples)
        self.__num_samples = num_samples

        self.__count_fitness_calls = 0

    def __plot_current(self, round_worst, round_average, round_best):
        plt.plot(round_worst)
        plt.plot(round_average)
        plt.plot(round_best)
        plt.draw()
        plt.pause(0.01)

    def __generate_crossovers(self, elite_samples: List[Sample], n: int) -> List[Sample]:
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
            co1, co2 = self.__evolver.generate_valid_crossover(elite_samples)
            new_samples.append(Sample(self.__letters, decode_letters=co1))
            new_samples.append(Sample(self.__letters, decode_letters=co2))
            samples_len += 2

        return new_samples

    def __save(self, dec: List[str], fitness_scores: List[float]) -> None:
        i = np.argmax(fitness_scores)
        best = self.__samples[i]

        filename = f'output/dec_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt'
        with open(filename, '+wt', encoding='utf-8') as f:
            f.write(f'fitness score: {fitness_scores[i]}{os.linesep}')
            f.write(f'fitness calls: {self.__count_fitness_calls}{os.linesep}')
            f.write(f'letters: {self.__letters}{os.linesep}')
            f.write(f'dec: {best.decode_letters}{os.linesep}')
            f.writelines(dec[i])

        plt.savefig(f'output/plot_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png', format='png')

    def run(self):
        round_worst = []
        round_average = []
        round_best = []

        mutation_percentage = 0.5
        elite_percentage = 0.75
        mutation_amount = int(len(self.__samples) * mutation_percentage)

        plt.title(f'mutation percentage: {mutation_percentage}%, elite selection: {elite_percentage}%')

        while True:
            for i in Selector.choose_n_random(self.__samples, mutation_amount):
                s = self.__samples[i]
                _, c1, c2 = self.__evolver.mutate(s.dec_map)
                s.swap(c1, c2)

            # Decode the encrypted file
            dec = [Decoder.decode_words(self.enc, s.dec_map_int) for s in self.__samples]
            dec_words = [d.strip().translate(str.maketrans('', '', punctuation)).split(' ') for d in dec]
            # Calculate fitness score for each decode
            fitness_scores = [check_words_in_dict_ratio(dec, self.dictionary) for dec in dec_words]

            round_worst.append(min(fitness_scores))
            round_average.append(statistics.mean(fitness_scores))
            round_best.append(max(fitness_scores))
            self.__plot_current(round_worst, round_average, round_best)

            print(f'Best: {max(fitness_scores) * 100}%, Worst: {min(fitness_scores) * 100}%, Mean: {statistics.mean(fitness_scores) * 100}%')
            self.__count_fitness_calls += len(dec_words)
            print(f'fitness calls: {self.__count_fitness_calls}')

            if not all(fitness_score < self.__fitness_goal for fitness_score in fitness_scores):
                break

            elite_samples = Selector.select_elite(self.__samples, fitness_scores, elite_percentage)
            self.__samples = self.__generate_crossovers(elite_samples, self.__num_samples - len(elite_samples))
            self.__samples.extend(elite_samples)

        # Decode the encrypted file
        dec = [Decoder.decode_words(self.enc, s.dec_map_int) for s in self.__samples]
        dec_words = [d.strip().translate(str.maketrans('', '', punctuation)).split(' ') for d in dec]
        # Calculate fitness score for each decode
        fitness_scores = [check_words_in_dict_ratio(dec, self.dictionary) for dec in dec_words]

        self.__save(dec, fitness_scores)
