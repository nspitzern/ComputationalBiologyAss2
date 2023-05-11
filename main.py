from pprint import pprint
from typing import List

from files_parser import parse_encoded, parse_dict, parse_letters_freq
from generator import Generator, Sample
from decoder import Decoder
from fitness import check_words_in_dict_ratio
from selector import Selector


if __name__ == '__main__':
    enc_words, enc_letters = parse_encoded('data/enc.txt')
    dictionary = parse_dict('data/dict.txt')
    freq_1_letter = parse_letters_freq('data/Letter_Freq.txt')
    freq_2_letter = parse_letters_freq('data/Letter2_Freq.txt')

    g = Generator(list(freq_1_letter.keys()), len(enc_letters))
    selector = Selector()

    samples: List[Sample] = g.generate_random(50)

    # print(Decoder.decode(enc_letters, samples[0].dec_map))
    # s = g.generate_mutation(samples[0])
    # print(Decoder.decode(enc_letters, s.dec_map))

    decs_words = [Decoder.decode_words(enc_words, s.dec_map) for s in samples]
    fitness_scores = [check_words_in_dict_ratio(dec, dictionary) for dec in decs_words]
    while all(fitness_scores) < 95:
        print(f'{max(fitness_scores)}%')

        elite_samples = selector.select_elite(samples, fitness_scores, 0.95)

        for s in samples:
            s = g.generate_mutation(s)

        # Decode the encrypted file
        decs_words = [Decoder.decode_words(enc_words, s.dec_map) for s in samples]
        # Calculate fitness score for each decode
        fitness_scores = [check_words_in_dict_ratio(dec, dictionary) for dec in decs_words]