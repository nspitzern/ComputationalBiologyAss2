import unittest

from src.fitness import check_words_in_dict_ratio, letters_freq_ratio, MSE


class TestFitness(unittest.TestCase):
    def test_fitness_100(self):
        dec = ['you', 'are', 'great']
        d = ['of', 'course', 'I', 'am', 'great', 'I', 'am', 'you', 'and', 'you', 'are', 'me']

        res = check_words_in_dict_ratio(dec, d)
        assert res == 100

    def test_fitness_50(self):
        dec = ['you', 'are', 'great', 'also']
        d = ['of', 'course', 'I', 'am', 'great', 'I', 'am', 'you']

        res = check_words_in_dict_ratio(dec, d)
        assert res == 50

    def test_fitness_0(self):
        dec = ['you', 'are', 'great', 'also']
        d = ['stop', 'doing', 'this', 'it', 'is', 'not', 'funny']

        res = check_words_in_dict_ratio(dec, d)
        assert res == 0

    def test_MSE_not_0(self):
        d_f = {'a': 0.3, 'b': 0.01}
        c_f = {'a': 0.2, 'b': 0.4}

        assert letters_freq_ratio(d_f, c_f, MSE) != 0

    def test_MSE_0(self):
        d_f = {'a': 0.2, 'b': 0.4}
        c_f = {'a': 0.2, 'b': 0.4}

        assert letters_freq_ratio(d_f, c_f, MSE) == 0


if __name__ == '__main__':
    unittest.main()
