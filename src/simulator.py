import statistics
from string import punctuation
from typing import Dict, List, Set
from src.files_parser import parse_dict, parse_encoded, parse_letters_freq
from src.generator import Generator, Sample
from src.memory import Memory
from src.selector import Selector
from src.decoder import Decoder
from src.fitness import check_words_in_dict_ratio


class Simulator:
    def __init__(self, num_samples: int, fitness_goal: int) -> None:
        self.enc = parse_encoded('enc.txt')
        self.dictionary: Set[str] = set(parse_dict('dict.txt'))
        freq_1_letter: Dict[str, float] = parse_letters_freq('Letter_Freq.txt')
        freq_2_letter: Dict[str, float] = parse_letters_freq('Letter2_Freq.txt')

        self.__letters = list(sorted(freq_1_letter.keys()))
        self.__memory: Memory = Memory()
        self.__fitness_goal: float = fitness_goal
        self.__generator: Generator = Generator(self.__letters)
        self.__samples: List[Sample] = self.__generator.generate_random(num_samples)

        self.__count_fitness_calls = 0

    def run(self):
        should_run = True
        
        while should_run:
            for s in self.__samples:
                mutation, c1, c2 = self.__generator.generate_mutation(s.dec_map)
                while mutation in self.__memory.records:
                    mutation, c1, c2 = self.__generator.generate_mutation(s.dec_map)
                self.__memory.add(mutation)
                s.swap(c1, c2)

            # Decode the encrypted file
            dec = [Decoder.decode_words(self.enc, s.dec_map_int) for s in self.__samples]
            dec_words = [d.strip().translate(str.maketrans('', '', punctuation)).split(' ') for d in dec]
            # Calculate fitness score for each decode
            fitness_scores = [check_words_in_dict_ratio(dec, self.dictionary) for dec in dec_words]

            print(f'Best: {max(fitness_scores)}%, Worst: {min(fitness_scores)}%, Mean: {statistics.mean(fitness_scores)}%')
            self.__count_fitness_calls += len(dec_words)
            print(f'fitness calls: {self.__count_fitness_calls}')
            should_run = all(fitness_score < self.__fitness_goal for fitness_score in fitness_scores)

            elite_samples = Selector.select_elite(self.__samples, fitness_scores, self.__fitness_goal)
