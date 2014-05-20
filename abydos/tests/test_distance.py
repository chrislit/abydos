# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
import unittest
from abydos.distance import levenshtein, levenshtein_normalized, hamming, \
    tversky_index, sorensen_coeff, sorensen, jaccard_coeff, jaccard, \
    tanimoto_coeff, tanimoto, strcmp95, jaro_winkler, lcs, mra_compare


class levenshtein_test_cases(unittest.TestCase):
    def test_levenshtein(self):
        self.assertEquals(levenshtein('', ''), 0)

        # http://oldfashionedsoftware.com/tag/levenshtein-distance/
        self.assertEquals(levenshtein('a', ''), 1)
        self.assertEquals(levenshtein('', 'a'), 1)
        self.assertEquals(levenshtein('abc', ''), 3)
        self.assertEquals(levenshtein('', 'abc'), 3)
        self.assertEquals(levenshtein('', ''), 0)
        self.assertEquals(levenshtein('a', 'a'), 0)
        self.assertEquals(levenshtein('abc', 'abc'), 0)
        self.assertEquals(levenshtein('', 'a'), 1)
        self.assertEquals(levenshtein('a', 'ab'), 1)
        self.assertEquals(levenshtein('b', 'ab'), 1)
        self.assertEquals(levenshtein('ac', 'abc'), 1)
        self.assertEquals(levenshtein('abcdefg', 'xabxcdxxefxgx'), 6)
        self.assertEquals(levenshtein('a', ''), 1)
        self.assertEquals(levenshtein('ab', 'a'), 1)
        self.assertEquals(levenshtein('ab', 'b'), 1)
        self.assertEquals(levenshtein('abc', 'ac'), 1)
        self.assertEquals(levenshtein('xabxcdxxefxgx', 'abcdefg'), 6)
        self.assertEquals(levenshtein('a', 'b'), 1)
        self.assertEquals(levenshtein('ab', 'ac'), 1)
        self.assertEquals(levenshtein('ac', 'bc'), 1)
        self.assertEquals(levenshtein('abc', 'axc'), 1)
        self.assertEquals(levenshtein('xabxcdxxefxgx', '1ab2cd34ef5g6'), 6)
        self.assertEquals(levenshtein('example', 'samples'), 3)
        self.assertEquals(levenshtein('sturgeon', 'urgently'), 6)
        self.assertEquals(levenshtein('levenshtein', 'frankenstein'), 6)
        self.assertEquals(levenshtein('distance', 'difference'), 5)
        self.assertEquals(levenshtein('java was neat', 'scala is great'), 7)

        # https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
        self.assertEquals(levenshtein('CA', 'ABC', 'dam'), 2)
        self.assertEquals(levenshtein('CA', 'ABC', 'osa'), 3)

        # test cost of insert
        self.assertEquals(levenshtein('', 'b', 'lev', cost=(5,7,10,10)), 5)
        self.assertEquals(levenshtein('', 'b', 'osa', cost=(5,7,10,10)), 5)
        self.assertEquals(levenshtein('', 'b', 'dam', cost=(5,7,10,10)), 5)
        self.assertEquals(levenshtein('a', 'ab', 'lev', cost=(5,7,10,10)), 5)
        self.assertEquals(levenshtein('a', 'ab', 'osa', cost=(5,7,10,10)), 5)
        self.assertEquals(levenshtein('a', 'ab', 'dam', cost=(5,7,10,10)), 5)

        # test cost of delete
        self.assertEquals(levenshtein('b', '', 'lev', cost=(5,7,10,10)), 7)
        self.assertEquals(levenshtein('b', '', 'osa', cost=(5,7,10,10)), 7)
        self.assertEquals(levenshtein('b', '', 'dam', cost=(5,7,10,10)), 7)
        self.assertEquals(levenshtein('ab', 'a', 'lev', cost=(5,7,10,10)), 7)
        self.assertEquals(levenshtein('ab', 'a', 'osa', cost=(5,7,10,10)), 7)
        self.assertEquals(levenshtein('ab', 'a', 'dam', cost=(5,7,10,10)), 7)

        # test cost of substitute
        self.assertEquals(levenshtein('a', 'b', 'lev', cost=(10,10,5,10)), 5)
        self.assertEquals(levenshtein('a', 'b', 'osa', cost=(10,10,5,10)), 5)
        self.assertEquals(levenshtein('a', 'b', 'dam', cost=(10,10,5,10)), 5)
        self.assertEquals(levenshtein('ac', 'bc', 'lev', cost=(10,10,5,10)), 5)
        self.assertEquals(levenshtein('ac', 'bc', 'osa', cost=(10,10,5,10)), 5)
        self.assertEquals(levenshtein('ac', 'bc', 'dam', cost=(10,10,5,10)), 5)

        # test cost of transpose
        self.assertEquals(levenshtein('ab', 'ba', 'lev', cost=(10,10,10,5)), 20)
        self.assertEquals(levenshtein('ab', 'ba', 'osa', cost=(10,10,10,5)), 5)
        self.assertEquals(levenshtein('ab', 'ba', 'dam', cost=(5,5,10,5)), 5)
        self.assertEquals(levenshtein('abc', 'bac', 'lev', cost=(10,10,10,5)), 20)
        self.assertEquals(levenshtein('abc', 'bac', 'osa', cost=(10,10,10,5)), 5)
        self.assertEquals(levenshtein('abc', 'bac', 'dam', cost=(5,5,10,5)), 5)
        self.assertEquals(levenshtein('cab', 'cba', 'lev', cost=(10,10,10,5)), 20)
        self.assertEquals(levenshtein('cab', 'cba', 'osa', cost=(10,10,10,5)), 5)
        self.assertEquals(levenshtein('cab', 'cba', 'dam', cost=(5,5,10,5)), 5)

        # test exception
        self.assertRaises(ValueError, levenshtein, 'ab', 'ba', 'dam', cost=(10,10,10,5))

    def test_levenshtein_normalized(self):
        self.assertEquals(levenshtein_normalized('', ''), 0)
        self.assertEquals(levenshtein_normalized('a', 'a'), 0)
        self.assertEquals(levenshtein_normalized('ab', 'ab'), 0)
        self.assertEquals(levenshtein_normalized('', 'a'), 1)
        self.assertEquals(levenshtein_normalized('', 'ab'), 1)
        self.assertEquals(levenshtein_normalized('a', 'c'), 1)
        self.assertEquals(levenshtein_normalized('abc', 'ac'), 1/3)
        self.assertEquals(levenshtein_normalized('abbc', 'ac'), 1/2)
        self.assertEquals(levenshtein_normalized('abbc', 'abc'), 1/4)


class hamming_test_cases(unittest.TestCase):
    def test_hamming(self):
        pass

class tversky_index_test_cases(unittest.TestCase):
    def test_tversky_index(self):
        pass


class sorensen_test_cases(unittest.TestCase):
    def test_sorensen_coeff(self):
        pass

    def test_sorensen(self):
        pass


class jaccard_test_cases(unittest.TestCase):
    def test_jaccard_coeff(self):
        pass

    def test_jaccard(self):
        pass


class tanimoto_test_cases(unittest.TestCase):
    def test_tanimoto_coeff(self):
        pass

    def test_tanimoto(self):
        pass


class jaro_winkler_test_cases(unittest.TestCase):
    def test_strcmp95(self):
        pass

    def test_jaro_winkler(self):
        pass


class lcs_test_cases(unittest.TestCase):
    def test_lcs(self):
        pass


class mra_compare_test_cases(unittest.TestCase):
    def test_mra_compare(self):
        pass
