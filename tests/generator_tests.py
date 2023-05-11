import unittest

from generator import Sample, Generator


class GeneratorTests(unittest.TestCase):
    def test_mutation(self):
        s1 = Sample(['a', 'b'])
        s1.dec_map = {'a': 'b', 'b': 'a'}
        s1_map = s1.dec_map.copy()

        g = Generator(['a', 'b'], 2)

        s2 = g.generate_mutation(s1)

        assert s2.dec_map != s1_map

