from pprint import pprint

from files_parser import parse_encoded, parse_dict, parse_letters_freq
from generator import Generator


if __name__ == '__main__':
    enc_words, enc_letters = parse_encoded('data/enc.txt')
    dictionary = parse_dict('data/dict.txt')
    freq_1_letter = parse_letters_freq('data/Letter_Freq.txt')
    freq_2_letter = parse_letters_freq('data/Letter2_Freq.txt')

    g = Generator(len(enc_letters))

    pprint(g.generate_random(50))
