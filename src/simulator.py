from typing import Dict, List
from src.files_parser import parse_dict, parse_encoded, parse_letters_freq
from src.generator import Generator, Sample
from src.selector import Selector
from src.decoder import Decoder
from src.fitness import check_words_in_dict_ratio


class Simulator:
    def __init__(self, num_samples: int, fitness_goal: int) -> None:
        self.enc_words, enc_letters = parse_encoded('enc.txt')
        self.dictionary: List[str] = parse_dict('dict.txt')
        freq_1_letter: Dict[str, float] = parse_letters_freq('Letter_Freq.txt')
        freq_2_letter: Dict[str, float] = parse_letters_freq('Letter2_Freq.txt')

        self.fitness_goal: int = fitness_goal
        self.generator: Generator = Generator(list(freq_1_letter.keys()), len(enc_letters))
        self.selector: Selector = Selector()
        self.samples: List[Sample] = self.generator.generate_random(num_samples)

    def run(self):
        decs_words = [Decoder.decode_words(self.enc_words, s.dec_map) for s in self.samples]
        fitness_scores = [check_words_in_dict_ratio(dec, self.dictionary) for dec in decs_words]
        while all(fitness_scores) < self.fitness_goal:
            print(f'{max(fitness_scores)}%')

            elite_samples = self.selector.select_elite(self.samples, fitness_scores, self.fitness_goal / 100)

            for s in self.samples:
                s = self.generator.generate_mutation(s)

            # Decode the encrypted file
            decs_words = [Decoder.decode_words(self.enc_words, s.dec_map) for s in self.samples]
            # Calculate fitness score for each decode
            fitness_scores = [check_words_in_dict_ratio(dec, self.dictionary) for dec in decs_words]
