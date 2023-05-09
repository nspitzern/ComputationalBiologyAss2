import unittest

from fitness import check_words_in_dict_ratio


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


if __name__ == '__main__':
    unittest.main()
