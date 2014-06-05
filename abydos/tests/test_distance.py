# -*- coding: utf-8 -*-
"""abydos.tests.test_distance

This module contains unit tests for abydos.distance

Copyright 2014 by Christopher C. Little.
This file is part of Abydos.

Abydos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Abydos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Abydos. If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals
from __future__ import division
import unittest
from abydos.distance import levenshtein, dist_levenshtein, sim_levenshtein, \
    hamming, dist_hamming, sim_hamming, sim_tversky, dist_tversky, sim_dice, \
    dist_dice, sim_jaccard, dist_jaccard, sim_overlap, dist_overlap, \
    sim_tanimoto, tanimoto, sim_cosine, dist_cosine, sim_strcmp95, \
    dist_strcmp95, sim_jaro_winkler, dist_jaro_winkler, lcsseq, sim_lcsseq, \
    dist_lcsseq, lcsstr, sim_lcsstr, dist_lcsstr, sim_ratcliffobershelp, \
    dist_ratcliffobershelp, mra_compare, sim_compression, dist_compression, \
    sim_monge_elkan, dist_monge_elkan, sim_ident, dist_ident, sim_matrix, \
    needleman_wunsch
import math
from difflib import SequenceMatcher
import os

TESTDIR = os.path.dirname(__file__)


class LevenshteinTestCases(unittest.TestCase):
    """test cases for abydos.distance.levenshtein,
    abydos.distance.dist_levenshtein, & abydos.distance.sim_levenshtein
    """
    def test_levenshtein(self):
        """test abydos.distance.levenshtein
        """
        self.assertEqual(levenshtein('', ''), 0)

        # http://oldfashionedsoftware.com/tag/levenshtein-distance/
        self.assertEqual(levenshtein('a', ''), 1)
        self.assertEqual(levenshtein('', 'a'), 1)
        self.assertEqual(levenshtein('abc', ''), 3)
        self.assertEqual(levenshtein('', 'abc'), 3)
        self.assertEqual(levenshtein('', ''), 0)
        self.assertEqual(levenshtein('a', 'a'), 0)
        self.assertEqual(levenshtein('abc', 'abc'), 0)
        self.assertEqual(levenshtein('', 'a'), 1)
        self.assertEqual(levenshtein('a', 'ab'), 1)
        self.assertEqual(levenshtein('b', 'ab'), 1)
        self.assertEqual(levenshtein('ac', 'abc'), 1)
        self.assertEqual(levenshtein('abcdefg', 'xabxcdxxefxgx'), 6)
        self.assertEqual(levenshtein('a', ''), 1)
        self.assertEqual(levenshtein('ab', 'a'), 1)
        self.assertEqual(levenshtein('ab', 'b'), 1)
        self.assertEqual(levenshtein('abc', 'ac'), 1)
        self.assertEqual(levenshtein('xabxcdxxefxgx', 'abcdefg'), 6)
        self.assertEqual(levenshtein('a', 'b'), 1)
        self.assertEqual(levenshtein('ab', 'ac'), 1)
        self.assertEqual(levenshtein('ac', 'bc'), 1)
        self.assertEqual(levenshtein('abc', 'axc'), 1)
        self.assertEqual(levenshtein('xabxcdxxefxgx', '1ab2cd34ef5g6'), 6)
        self.assertEqual(levenshtein('example', 'samples'), 3)
        self.assertEqual(levenshtein('sturgeon', 'urgently'), 6)
        self.assertEqual(levenshtein('levenshtein', 'frankenstein'), 6)
        self.assertEqual(levenshtein('distance', 'difference'), 5)
        self.assertEqual(levenshtein('java was neat', 'scala is great'), 7)

        # https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
        self.assertEqual(levenshtein('CA', 'ABC', 'dam'), 2)
        self.assertEqual(levenshtein('CA', 'ABC', 'osa'), 3)

        # test cost of insert
        self.assertEqual(levenshtein('', 'b', 'lev', cost=(5, 7, 10, 10)), 5)
        self.assertEqual(levenshtein('', 'b', 'osa', cost=(5, 7, 10, 10)), 5)
        self.assertEqual(levenshtein('', 'b', 'dam', cost=(5, 7, 10, 10)), 5)
        self.assertEqual(levenshtein('a', 'ab', 'lev', cost=(5, 7, 10, 10)), 5)
        self.assertEqual(levenshtein('a', 'ab', 'osa', cost=(5, 7, 10, 10)), 5)
        self.assertEqual(levenshtein('a', 'ab', 'dam', cost=(5, 7, 10, 10)), 5)

        # test cost of delete
        self.assertEqual(levenshtein('b', '', 'lev', cost=(5, 7, 10, 10)), 7)
        self.assertEqual(levenshtein('b', '', 'osa', cost=(5, 7, 10, 10)), 7)
        self.assertEqual(levenshtein('b', '', 'dam', cost=(5, 7, 10, 10)), 7)
        self.assertEqual(levenshtein('ab', 'a', 'lev', cost=(5, 7, 10, 10)), 7)
        self.assertEqual(levenshtein('ab', 'a', 'osa', cost=(5, 7, 10, 10)), 7)
        self.assertEqual(levenshtein('ab', 'a', 'dam', cost=(5, 7, 10, 10)), 7)

        # test cost of substitute
        self.assertEqual(levenshtein('a', 'b', 'lev', cost=(10, 10, 5, 10)), 5)
        self.assertEqual(levenshtein('a', 'b', 'osa', cost=(10, 10, 5, 10)), 5)
        self.assertEqual(levenshtein('a', 'b', 'dam', cost=(10, 10, 5, 10)), 5)
        self.assertEqual(levenshtein('ac', 'bc', 'lev',
                                      cost=(10, 10, 5, 10)), 5)
        self.assertEqual(levenshtein('ac', 'bc', 'osa',
                                      cost=(10, 10, 5, 10)), 5)
        self.assertEqual(levenshtein('ac', 'bc', 'dam',
                                      cost=(10, 10, 5, 10)), 5)

        # test cost of transpose
        self.assertEqual(levenshtein('ab', 'ba', 'lev',
                                      cost=(10, 10, 10, 5)), 20)
        self.assertEqual(levenshtein('ab', 'ba', 'osa',
                                      cost=(10, 10, 10, 5)), 5)
        self.assertEqual(levenshtein('ab', 'ba', 'dam',
                                      cost=(5, 5, 10, 5)), 5)
        self.assertEqual(levenshtein('abc', 'bac', 'lev',
                                      cost=(10, 10, 10, 5)), 20)
        self.assertEqual(levenshtein('abc', 'bac', 'osa',
                                      cost=(10, 10, 10, 5)), 5)
        self.assertEqual(levenshtein('abc', 'bac', 'dam',
                                      cost=(5, 5, 10, 5)), 5)
        self.assertEqual(levenshtein('cab', 'cba', 'lev',
                                      cost=(10, 10, 10, 5)), 20)
        self.assertEqual(levenshtein('cab', 'cba', 'osa',
                                      cost=(10, 10, 10, 5)), 5)
        self.assertEqual(levenshtein('cab', 'cba', 'dam',
                                      cost=(5, 5, 10, 5)), 5)

        # test exception
        self.assertRaises(ValueError, levenshtein, 'ab', 'ba', 'dam',
                          cost=(10, 10, 10, 5))

    def test_dist_levenshtein(self):
        """test abydos.distance.dist_levenshtein
        """
        self.assertEqual(dist_levenshtein('', ''), 0)

        self.assertEqual(dist_levenshtein('a', 'a'), 0)
        self.assertEqual(dist_levenshtein('ab', 'ab'), 0)
        self.assertEqual(dist_levenshtein('', 'a'), 1)
        self.assertEqual(dist_levenshtein('', 'ab'), 1)
        self.assertEqual(dist_levenshtein('a', 'c'), 1)

        self.assertAlmostEqual(dist_levenshtein('abc', 'ac'), 1/3)
        self.assertAlmostEqual(dist_levenshtein('abbc', 'ac'), 1/2)
        self.assertAlmostEqual(dist_levenshtein('abbc', 'abc'), 1/4)

    def test_sim_levenshtein(self):
        """test abydos.distance.sim_levenshtein
        """
        self.assertEqual(sim_levenshtein('', ''), 1)

        self.assertEqual(sim_levenshtein('a', 'a'), 1)
        self.assertEqual(sim_levenshtein('ab', 'ab'), 1)
        self.assertEqual(sim_levenshtein('', 'a'), 0)
        self.assertEqual(sim_levenshtein('', 'ab'), 0)
        self.assertEqual(sim_levenshtein('a', 'c'), 0)

        self.assertAlmostEqual(sim_levenshtein('abc', 'ac'), 2/3)
        self.assertAlmostEqual(sim_levenshtein('abbc', 'ac'), 1/2)
        self.assertAlmostEqual(sim_levenshtein('abbc', 'abc'), 3/4)


class HammingTestCases(unittest.TestCase):
    """test cases for abydos.distance.hamming,
    abydos.distance.dist_hamming, & abydos.distance.sim_hamming
    """
    def test_hamming(self):
        """test abydos.distance.hamming
        """
        self.assertEqual(hamming('', ''), 0)
        self.assertEqual(hamming('', '', False), 0)

        self.assertEqual(hamming('a', ''), 1)
        self.assertEqual(hamming('a', 'a'), 0)
        self.assertEqual(hamming('a', 'a', False), 0)
        self.assertEqual(hamming('a', 'b'), 1)
        self.assertEqual(hamming('a', 'b', False), 1)
        self.assertEqual(hamming('abc', 'cba'), 2)
        self.assertEqual(hamming('abc', 'cba', False), 2)
        self.assertEqual(hamming('abc', ''), 3)
        self.assertEqual(hamming('bb', 'cbab'), 3)

        # test exception
        self.assertRaises(ValueError, hamming, 'ab', 'a', False)

        # https://en.wikipedia.org/wiki/Hamming_distance
        self.assertEqual(hamming('karolin', 'kathrin'), 3)
        self.assertEqual(hamming('karolin', 'kerstin'), 3)
        self.assertEqual(hamming('1011101', '1001001'), 2)
        self.assertEqual(hamming('2173896', '2233796'), 3)

    def test_dist_hamming(self):
        """test abydos.distance.dist_hamming
        """
        self.assertEqual(dist_hamming('', ''), 0)
        self.assertEqual(dist_hamming('', '', False), 0)

        self.assertEqual(dist_hamming('a', ''), 1)
        self.assertEqual(dist_hamming('a', 'a'), 0)
        self.assertEqual(dist_hamming('a', 'a', False), 0)
        self.assertEqual(dist_hamming('a', 'b'), 1)
        self.assertEqual(dist_hamming('a', 'b', False), 1)
        self.assertAlmostEqual(dist_hamming('abc', 'cba'), 2/3)
        self.assertAlmostEqual(dist_hamming('abc', 'cba', False), 2/3)
        self.assertEqual(dist_hamming('abc', ''), 1)
        self.assertAlmostEqual(dist_hamming('bb', 'cbab'), 3/4)

        # test exception
        self.assertRaises(ValueError, dist_hamming, 'ab', 'a', False)

        # https://en.wikipedia.org/wiki/Hamming_distance
        self.assertAlmostEqual(dist_hamming('karolin', 'kathrin'), 3/7)
        self.assertAlmostEqual(dist_hamming('karolin', 'kerstin'), 3/7)
        self.assertAlmostEqual(dist_hamming('1011101', '1001001'), 2/7)
        self.assertAlmostEqual(dist_hamming('2173896', '2233796'), 3/7)

    def test_sim_hamming(self):
        """test abydos.distance.sim_hamming
        """
        self.assertEqual(sim_hamming('', ''), 1)
        self.assertEqual(sim_hamming('', '', False), 1)

        self.assertEqual(sim_hamming('a', ''), 0)
        self.assertEqual(sim_hamming('a', 'a'), 1)
        self.assertEqual(sim_hamming('a', 'a', False), 1)
        self.assertEqual(sim_hamming('a', 'b'), 0)
        self.assertEqual(sim_hamming('a', 'b', False), 0)
        self.assertAlmostEqual(sim_hamming('abc', 'cba'), 1/3)
        self.assertAlmostEqual(sim_hamming('abc', 'cba', False), 1/3)
        self.assertEqual(sim_hamming('abc', ''), 0)
        self.assertAlmostEqual(sim_hamming('bb', 'cbab'), 1/4)

        # test exception
        self.assertRaises(ValueError, sim_hamming, 'ab', 'a', False)

        # https://en.wikipedia.org/wiki/Hamming_distance
        self.assertAlmostEqual(sim_hamming('karolin', 'kathrin'), 4/7)
        self.assertAlmostEqual(sim_hamming('karolin', 'kerstin'), 4/7)
        self.assertAlmostEqual(sim_hamming('1011101', '1001001'), 5/7)
        self.assertAlmostEqual(sim_hamming('2173896', '2233796'), 4/7)


class TverskyIndexTestCases(unittest.TestCase):
    """test cases for abydos.distance.sim_tversky & abydos.distance.dist_tversky
    """
    def test_sim_tversky(self):
        """test abydos.distance.sim_tversky
        """
        self.assertEqual(sim_tversky('', ''), 1)
        self.assertEqual(sim_tversky('nelson', ''), 0)
        self.assertEqual(sim_tversky('', 'neilsen'), 0)
        self.assertAlmostEqual(sim_tversky('nelson', 'neilsen'), 4/11)
        # TODO: Add bias test(s) and unequal alpha & beta tests

    def test_dist_tversky(self):
        """test abydos.distance.dist_tversky
        """
        self.assertEqual(dist_tversky('', ''), 0)
        self.assertEqual(dist_tversky('nelson', ''), 1)
        self.assertEqual(dist_tversky('', 'neilsen'), 1)
        self.assertAlmostEqual(dist_tversky('nelson', 'neilsen'), 7/11)
        # TODO: Add bias test(s) and unequal alpha & beta tests


class DiceTestCases(unittest.TestCase):
    """test cases for abydos.distance.sim_dice & abydos.distance.dist_dice
    """
    def test_sim_dice(self):
        """test abydos.distance.sim_dice
        """
        self.assertEqual(sim_dice('', ''), 1)
        self.assertEqual(sim_dice('nelson', ''), 0)
        self.assertEqual(sim_dice('', 'neilsen'), 0)
        self.assertAlmostEqual(sim_dice('nelson', 'neilsen'), 8/15)

    def test_dist_dice(self):
        """test abydos.distance.dist_dice
        """
        self.assertEqual(dist_dice('', ''), 0)
        self.assertEqual(dist_dice('nelson', ''), 1)
        self.assertEqual(dist_dice('', 'neilsen'), 1)
        self.assertAlmostEqual(dist_dice('nelson', 'neilsen'), 7/15)


class JaccardTestCases(unittest.TestCase):
    """test cases for abydos.distance.sim_jaccard & abydos.distance.dist_jaccard
    """
    def test_sim_jaccard(self):
        """test abydos.distance.sim_jaccard
        """
        self.assertEqual(sim_jaccard('', ''), 1)
        self.assertEqual(sim_jaccard('nelson', ''), 0)
        self.assertEqual(sim_jaccard('', 'neilsen'), 0)
        self.assertAlmostEqual(sim_jaccard('nelson', 'neilsen'), 4/11)

    def test_dist_jaccard(self):
        """test abydos.distance.dist_jaccard
        """
        self.assertEqual(dist_jaccard('', ''), 0)
        self.assertEqual(dist_jaccard('nelson', ''), 1)
        self.assertEqual(dist_jaccard('', 'neilsen'), 1)
        self.assertAlmostEqual(dist_jaccard('nelson', 'neilsen'), 7/11)


class OverlapTestCases(unittest.TestCase):
    """test cases for abydos.distance.sim_overlap & abydos.distance.dist_overlap
    """
    def test_sim_overlap(self):
        """test abydos.distance.sim_overlap
        """
        self.assertEqual(sim_overlap('', ''), 1)
        self.assertEqual(sim_overlap('nelson', ''), 0)
        self.assertEqual(sim_overlap('', 'neilsen'), 0)
        self.assertAlmostEqual(sim_overlap('nelson', 'neilsen'), 4/7)

    def test_dist_overlap(self):
        """test abydos.distance.dist_overlap
        """
        self.assertEqual(dist_overlap('', ''), 0)
        self.assertEqual(dist_overlap('nelson', ''), 1)
        self.assertEqual(dist_overlap('', 'neilsen'), 1)
        self.assertAlmostEqual(dist_overlap('nelson', 'neilsen'), 3/7)


class TanimotoTestCases(unittest.TestCase):
    """test cases for abydos.distance.sim_tanimoto & abydos.distance.tanimoto
    """
    def test_tanimoto_coeff(self):
        """test abydos.distance.tanimoto_coeff
        """
        self.assertEqual(sim_tanimoto('', ''), 1)
        self.assertEqual(sim_tanimoto('nelson', ''), 0)
        self.assertEqual(sim_tanimoto('', 'neilsen'), 0)
        self.assertAlmostEqual(sim_tanimoto('nelson', 'neilsen'), 4/11)

    def test_tanimoto(self):
        """test abydos.distance.tanimoto
        """
        self.assertEqual(tanimoto('', ''), 0)
        self.assertEqual(tanimoto('nelson', ''), float('-inf'))
        self.assertEqual(tanimoto('', 'neilsen'), float('-inf'))
        self.assertAlmostEqual(tanimoto('nelson', 'neilsen'), math.log(4/11, 2))


class CosineSimilarityTestCases(unittest.TestCase):
    """test cases for abydos.distance.sim_cosine & abydos.distance.dist_cosine
    """
    def test_sim_cosine(self):
        """test abydos.distance.sim_cosine
        """
        self.assertEqual(sim_cosine('', ''), 1)
        self.assertEqual(sim_cosine('nelson', ''), 0)
        self.assertEqual(sim_cosine('', 'neilsen'), 0)
        self.assertAlmostEqual(sim_cosine('nelson', 'neilsen'), 4/math.sqrt(7*8))

    def test_dist_cosine(self):
        """test abydos.distance.dist_cosine
        """
        self.assertEqual(dist_cosine('', ''), 0)
        self.assertEqual(dist_cosine('nelson', ''), 1)
        self.assertEqual(dist_cosine('', 'neilsen'), 1)
        self.assertAlmostEqual(dist_cosine('nelson', 'neilsen'),
                               1-(4/math.sqrt(7*8)))


class JaroWinklerTestCases(unittest.TestCase):
    """test cases for abydos.distance.sim_strcmp95,
    abydos.distance.dist_strcmp95, abydos.distance.sim_jaro_winkler,
    & abydos.distance.dist_jaro_winkler
    """
    def test_sim_strcmp95(self):
        """test abydos.distance.sim_strcmp95
        """
        self.assertEqual(sim_strcmp95('', ''), 1)
        self.assertEqual(sim_strcmp95('MARTHA', ''), 0)
        self.assertEqual(sim_strcmp95('', 'MARTHA'), 0)
        self.assertEqual(sim_strcmp95('MARTHA', 'MARTHA'), 1)

        # TODO: find non-trivial strcmp95 tests or manufacture some

    def test_dist_strcmp95(self):
        """test abydos.distance.dist_strcmp95
        """
        self.assertEqual(dist_strcmp95('', ''), 0)
        self.assertEqual(dist_strcmp95('MARTHA', ''), 1)
        self.assertEqual(dist_strcmp95('', 'MARTHA'), 1)
        self.assertEqual(dist_strcmp95('MARTHA', 'MARTHA'), 0)

        # TODO: find non-trivial strcmp95 tests or manufacture some

    def test_sim_jaro_winkler(self):
        """test abydos.distance.sim_jaro_winkler
        """
        self.assertEqual(sim_jaro_winkler('', '', mode='jaro'), 1)
        self.assertEqual(sim_jaro_winkler('', '', mode='winkler'), 1)
        self.assertEqual(sim_jaro_winkler('MARTHA', '', mode='jaro'), 0)
        self.assertEqual(sim_jaro_winkler('MARTHA', '', mode='winkler'), 0)
        self.assertEqual(sim_jaro_winkler('', 'MARHTA', mode='jaro'), 0)
        self.assertEqual(sim_jaro_winkler('', 'MARHTA', mode='winkler'), 0)
        self.assertEqual(sim_jaro_winkler('MARTHA', 'MARTHA', mode='jaro'), 1)
        self.assertEqual(sim_jaro_winkler('MARTHA', 'MARTHA', mode='winkler'),
                         1)

        # https://en.wikipedia.org/wiki/Jaro-Winkler_distance
        self.assertAlmostEqual(sim_jaro_winkler('MARTHA', 'MARHTA',
                                             mode='jaro'), 0.94444444)
        self.assertAlmostEqual(sim_jaro_winkler('MARTHA', 'MARHTA',
                                             mode='winkler'), 0.96111111)
        self.assertAlmostEqual(sim_jaro_winkler('DWAYNE', 'DUANE',
                                             mode='jaro'), 0.82222222)
        self.assertAlmostEqual(sim_jaro_winkler('DWAYNE', 'DUANE',
                                             mode='winkler'), 0.84)
        self.assertAlmostEqual(sim_jaro_winkler('DIXON', 'DICKSONX',
                                             mode='jaro'), 0.76666666)
        self.assertAlmostEqual(sim_jaro_winkler('DIXON', 'DICKSONX',
                                             mode='winkler'), 0.81333333)

    def test_dist_jaro_winkler(self):
        """test abydos.distance.dist_jaro_winkler
        """
        self.assertEqual(dist_jaro_winkler('', '', mode='jaro'), 0)
        self.assertEqual(dist_jaro_winkler('', '', mode='winkler'), 0)
        self.assertEqual(dist_jaro_winkler('MARTHA', '', mode='jaro'), 1)
        self.assertEqual(dist_jaro_winkler('MARTHA', '', mode='winkler'), 1)
        self.assertEqual(dist_jaro_winkler('', 'MARHTA', mode='jaro'), 1)
        self.assertEqual(dist_jaro_winkler('', 'MARHTA', mode='winkler'), 1)
        self.assertEqual(dist_jaro_winkler('MARTHA', 'MARTHA', mode='jaro'), 0)
        self.assertEqual(dist_jaro_winkler('MARTHA', 'MARTHA', mode='winkler'),
                         0)

        # https://en.wikipedia.org/wiki/Jaro-Winkler_distance
        self.assertAlmostEqual(dist_jaro_winkler('MARTHA', 'MARHTA',
                                             mode='jaro'), 0.05555555)
        self.assertAlmostEqual(dist_jaro_winkler('MARTHA', 'MARHTA',
                                             mode='winkler'), 0.03888888)
        self.assertAlmostEqual(dist_jaro_winkler('DWAYNE', 'DUANE',
                                             mode='jaro'), 0.17777777)
        self.assertAlmostEqual(dist_jaro_winkler('DWAYNE', 'DUANE',
                                             mode='winkler'), 0.16)
        self.assertAlmostEqual(dist_jaro_winkler('DIXON', 'DICKSONX',
                                             mode='jaro'), 0.23333333)
        self.assertAlmostEqual(dist_jaro_winkler('DIXON', 'DICKSONX',
                                             mode='winkler'), 0.18666666)


class LcsseqTestCases(unittest.TestCase):
    """test cases for abydos.distance.lcsseq, abydos.distance.sim_lcsseq, &
    abydos.distance.dist_lcsseq
    """
    def test_lcsseq(self):
        """test abydos.distance.lcsseq
        """
        self.assertEqual(lcsseq('', ''), '')
        self.assertEqual(lcsseq('A', ''), '')
        self.assertEqual(lcsseq('', 'A'), '')
        self.assertEqual(lcsseq('A', 'A'), 'A')
        self.assertEqual(lcsseq('ABCD', ''), '')
        self.assertEqual(lcsseq('', 'ABCD'), '')
        self.assertEqual(lcsseq('ABCD', 'ABCD'), 'ABCD')
        self.assertEqual(lcsseq('ABCD', 'BC'), 'BC')
        self.assertEqual(lcsseq('ABCD', 'AD'), 'AD')
        self.assertEqual(lcsseq('ABCD', 'AC'), 'AC')
        self.assertEqual(lcsseq('AB', 'CD'), '')
        self.assertEqual(lcsseq('ABC', 'BCD'), 'BC')

        self.assertEqual(lcsseq('DIXON', 'DICKSONX'), 'DION')

        # https://en.wikipedia.org/wiki/Longest_common_subsequence_problem
        self.assertEqual(lcsseq('AGCAT', 'GAC'), 'AC')
        self.assertEqual(lcsseq('XMJYAUZ', 'MZJAWXU'), 'MJAU')

        # https://github.com/jwmerrill/factor/blob/master/basis/lcs/lcs-tests.factor
        self.assertEqual(lcsseq('hell', 'hello'), 'hell')
        self.assertEqual(lcsseq('hello', 'hell'), 'hell')
        self.assertEqual(lcsseq('ell', 'hell'), 'ell')
        self.assertEqual(lcsseq('hell', 'ell'), 'ell')
        self.assertEqual(lcsseq('faxbcd', 'abdef'), 'abd')

        # http://www.unesco.org/culture/languages-atlas/assets/_core/php/qcubed_unit_tests.php
        self.assertEqual(lcsseq('hello world', 'world war 2'), 'world')
        self.assertEqual(lcsseq('foo bar', 'bar foo'), 'foo')
        self.assertEqual(lcsseq('aaa', 'aa'), 'aa')
        self.assertEqual(lcsseq('cc', 'bbbbcccccc'), 'cc')
        self.assertEqual(lcsseq('ccc', 'bcbb'), 'c')

    def test_sim_lcsseq(self):
        """test abydos.distance.sim_lcsseq
        """
        self.assertEqual(sim_lcsseq('', ''), 1)
        self.assertEqual(sim_lcsseq('A', ''), 0)
        self.assertEqual(sim_lcsseq('', 'A'), 0)
        self.assertEqual(sim_lcsseq('A', 'A'), 1)
        self.assertEqual(sim_lcsseq('ABCD', ''), 0)
        self.assertEqual(sim_lcsseq('', 'ABCD'), 0)
        self.assertEqual(sim_lcsseq('ABCD', 'ABCD'), 1)
        self.assertAlmostEqual(sim_lcsseq('ABCD', 'BC'), 2/4)
        self.assertAlmostEqual(sim_lcsseq('ABCD', 'AD'), 2/4)
        self.assertAlmostEqual(sim_lcsseq('ABCD', 'AC'), 2/4)
        self.assertAlmostEqual(sim_lcsseq('AB', 'CD'), 0)
        self.assertAlmostEqual(sim_lcsseq('ABC', 'BCD'), 2/3)

        self.assertAlmostEqual(sim_lcsseq('DIXON', 'DICKSONX'), 4/8)

        # https://en.wikipedia.org/wiki/Longest_common_subsequence_problem
        self.assertAlmostEqual(sim_lcsseq('AGCAT', 'GAC'), 2/5)
        self.assertAlmostEqual(sim_lcsseq('XMJYAUZ', 'MZJAWXU'), 4/7)

        # https://github.com/jwmerrill/factor/blob/master/basis/lcs/lcs-tests.factor
        self.assertAlmostEqual(sim_lcsseq('hell', 'hello'), 4/5)
        self.assertAlmostEqual(sim_lcsseq('hello', 'hell'), 4/5)
        self.assertAlmostEqual(sim_lcsseq('ell', 'hell'), 3/4)
        self.assertAlmostEqual(sim_lcsseq('hell', 'ell'), 3/4)
        self.assertAlmostEqual(sim_lcsseq('faxbcd', 'abdef'), 3/6)

        # http://www.unesco.org/culture/languages-atlas/assets/_core/php/qcubed_unit_tests.php
        self.assertAlmostEqual(sim_lcsseq('hello world', 'world war 2'), 5/11)
        self.assertAlmostEqual(sim_lcsseq('foo bar', 'bar foo'), 3/7)
        self.assertAlmostEqual(sim_lcsseq('aaa', 'aa'), 2/3)
        self.assertAlmostEqual(sim_lcsseq('cc', 'bbbbcccccc'), 2/10)
        self.assertAlmostEqual(sim_lcsseq('ccc', 'bcbb'), 1/4)

    def test_dist_lcsseq(self):
        """test abydos.distance.dist_lcsseq
        """
        self.assertEqual(dist_lcsseq('', ''), 0)
        self.assertEqual(dist_lcsseq('A', ''), 1)
        self.assertEqual(dist_lcsseq('', 'A'), 1)
        self.assertEqual(dist_lcsseq('A', 'A'), 0)
        self.assertEqual(dist_lcsseq('ABCD', ''), 1)
        self.assertEqual(dist_lcsseq('', 'ABCD'), 1)
        self.assertEqual(dist_lcsseq('ABCD', 'ABCD'), 0)
        self.assertAlmostEqual(dist_lcsseq('ABCD', 'BC'), 2/4)
        self.assertAlmostEqual(dist_lcsseq('ABCD', 'AD'), 2/4)
        self.assertAlmostEqual(dist_lcsseq('ABCD', 'AC'), 2/4)
        self.assertAlmostEqual(dist_lcsseq('AB', 'CD'), 1)
        self.assertAlmostEqual(dist_lcsseq('ABC', 'BCD'), 1/3)

        self.assertAlmostEqual(dist_lcsseq('DIXON', 'DICKSONX'), 4/8)

        # https://en.wikipedia.org/wiki/Longest_common_subsequence_problem
        self.assertAlmostEqual(dist_lcsseq('AGCAT', 'GAC'), 3/5)
        self.assertAlmostEqual(dist_lcsseq('XMJYAUZ', 'MZJAWXU'), 3/7)

        # https://github.com/jwmerrill/factor/blob/master/basis/lcs/lcs-tests.factor
        self.assertAlmostEqual(dist_lcsseq('hell', 'hello'), 1/5)
        self.assertAlmostEqual(dist_lcsseq('hello', 'hell'), 1/5)
        self.assertAlmostEqual(dist_lcsseq('ell', 'hell'), 1/4)
        self.assertAlmostEqual(dist_lcsseq('hell', 'ell'), 1/4)
        self.assertAlmostEqual(dist_lcsseq('faxbcd', 'abdef'), 3/6)

        # http://www.unesco.org/culture/languages-atlas/assets/_core/php/qcubed_unit_tests.php
        self.assertAlmostEqual(dist_lcsseq('hello world', 'world war 2'), 6/11)
        self.assertAlmostEqual(dist_lcsseq('foo bar', 'bar foo'), 4/7)
        self.assertAlmostEqual(dist_lcsseq('aaa', 'aa'), 1/3)
        self.assertAlmostEqual(dist_lcsseq('cc', 'bbbbcccccc'), 8/10)
        self.assertAlmostEqual(dist_lcsseq('ccc', 'bcbb'), 3/4)


class LcsstrTestCases(unittest.TestCase):
    """test cases for abydos.distance.lcsstr, abydos.distance.sim_lcsstr, &
    abydos.distance.dist_lcsstr
    """
    def test_lcsstr(self):
        """test abydos.distance.lcsstr
        """
        self.assertEqual(lcsstr('', ''), '')
        self.assertEqual(lcsstr('A', ''), '')
        self.assertEqual(lcsstr('', 'A'), '')
        self.assertEqual(lcsstr('A', 'A'), 'A')
        self.assertEqual(lcsstr('ABCD', ''), '')
        self.assertEqual(lcsstr('', 'ABCD'), '')
        self.assertEqual(lcsstr('ABCD', 'ABCD'), 'ABCD')
        self.assertEqual(lcsstr('ABCD', 'BC'), 'BC')
        self.assertEqual(lcsstr('ABCD', 'AD'), 'A')
        self.assertEqual(lcsstr('ABCD', 'AC'), 'A')
        self.assertEqual(lcsstr('AB', 'CD'), '')
        self.assertEqual(lcsstr('ABC', 'BCD'), 'BC')

        self.assertEqual(lcsstr('DIXON', 'DICKSONX'), 'DI')

        # https://en.wikipedia.org/wiki/Longest_common_subsequence_problem
        self.assertEqual(lcsstr('AGCAT', 'GAC'), 'A')
        self.assertEqual(lcsstr('XMJYAUZ', 'MZJAWXU'), 'X')

        # https://github.com/jwmerrill/factor/blob/master/basis/lcs/lcs-tests.factor
        self.assertEqual(lcsstr('hell', 'hello'), 'hell')
        self.assertEqual(lcsstr('hello', 'hell'), 'hell')
        self.assertEqual(lcsstr('ell', 'hell'), 'ell')
        self.assertEqual(lcsstr('hell', 'ell'), 'ell')
        self.assertEqual(lcsstr('faxbcd', 'abdef'), 'f')

        # http://www.unesco.org/culture/languages-atlas/assets/_core/php/qcubed_unit_tests.php
        self.assertEqual(lcsstr('hello world', 'world war 2'), 'world')
        self.assertEqual(lcsstr('foo bar', 'bar foo'), 'foo')
        self.assertEqual(lcsstr('aaa', 'aa'), 'aa')
        self.assertEqual(lcsstr('cc', 'bbbbcccccc'), 'cc')
        self.assertEqual(lcsstr('ccc', 'bcbb'), 'c')

        # http://www.maplesoft.com/support/help/Maple/view.aspx?path=StringTools/LongestCommonSubString
        self.assertEqual(lcsstr('abax', 'bax'), 'bax')
        self.assertEqual(lcsstr("tsaxbaxyz", "axcaxy"), 'axy')
        self.assertEqual(lcsstr("abcde", "uvabxycde"), 'cde')
        self.assertEqual(lcsstr("abc", "xyz"), '')
        self.assertEqual(lcsstr('TAAGGTCGGCGCGCACGCTGGCGAGTATGGTGCGGAGGCCCTGGAG\
AGGTGAGGCTCCCTCCCCTGCTCCGACCCGGGCTCCTCGCCCGCCCGGACCCAC', 'AAGCGCCGCGCAGTCTGGGCT\
CCGCACACTTCTGGTCCAGTCCGACTGAGAAGGAACCACCATGGTGCTGTCTCCCGCTGACAAGACCAACATCAAGACT\
GCCTGGGAAAAGATCGGCAGCCACGGTGGCGAGTATGGCGCCGAGGCCGT'), 'TGGCGAGTATGG')


    def test_sim_lcsstr(self):
        """test abydos.distance.sim_lcsstr
        """
        self.assertEqual(sim_lcsstr('', ''), 1)
        self.assertEqual(sim_lcsstr('A', ''), 0)
        self.assertEqual(sim_lcsstr('', 'A'), 0)
        self.assertEqual(sim_lcsstr('A', 'A'), 1)
        self.assertEqual(sim_lcsstr('ABCD', ''), 0)
        self.assertEqual(sim_lcsstr('', 'ABCD'), 0)
        self.assertEqual(sim_lcsstr('ABCD', 'ABCD'), 1)
        self.assertAlmostEqual(sim_lcsstr('ABCD', 'BC'), 2/4)
        self.assertAlmostEqual(sim_lcsstr('ABCD', 'AD'), 1/4)
        self.assertAlmostEqual(sim_lcsstr('ABCD', 'AC'), 1/4)
        self.assertAlmostEqual(sim_lcsstr('AB', 'CD'), 0)
        self.assertAlmostEqual(sim_lcsstr('ABC', 'BCD'), 2/3)

        self.assertAlmostEqual(sim_lcsstr('DIXON', 'DICKSONX'), 2/8)

        # https://en.wikipedia.org/wiki/Longest_common_subsequence_problem
        self.assertAlmostEqual(sim_lcsstr('AGCAT', 'GAC'), 1/5)
        self.assertAlmostEqual(sim_lcsstr('XMJYAUZ', 'MZJAWXU'), 1/7)

        # https://github.com/jwmerrill/factor/blob/master/basis/lcs/lcs-tests.factor
        self.assertAlmostEqual(sim_lcsstr('hell', 'hello'), 4/5)
        self.assertAlmostEqual(sim_lcsstr('hello', 'hell'), 4/5)
        self.assertAlmostEqual(sim_lcsstr('ell', 'hell'), 3/4)
        self.assertAlmostEqual(sim_lcsstr('hell', 'ell'), 3/4)
        self.assertAlmostEqual(sim_lcsstr('faxbcd', 'abdef'), 1/6)

        # http://www.unesco.org/culture/languages-atlas/assets/_core/php/qcubed_unit_tests.php
        self.assertAlmostEqual(sim_lcsstr('hello world', 'world war 2'), 5/11)
        self.assertAlmostEqual(sim_lcsstr('foo bar', 'bar foo'), 3/7)
        self.assertAlmostEqual(sim_lcsstr('aaa', 'aa'), 2/3)
        self.assertAlmostEqual(sim_lcsstr('cc', 'bbbbcccccc'), 2/10)
        self.assertAlmostEqual(sim_lcsstr('ccc', 'bcbb'), 1/4)

    def test_dist_lcsstr(self):
        """test abydos.distance.dist_lcsstr
        """
        self.assertEqual(dist_lcsstr('', ''), 0)
        self.assertEqual(dist_lcsstr('A', ''), 1)
        self.assertEqual(dist_lcsstr('', 'A'), 1)
        self.assertEqual(dist_lcsstr('A', 'A'), 0)
        self.assertEqual(dist_lcsstr('ABCD', ''), 1)
        self.assertEqual(dist_lcsstr('', 'ABCD'), 1)
        self.assertEqual(dist_lcsstr('ABCD', 'ABCD'), 0)
        self.assertAlmostEqual(dist_lcsstr('ABCD', 'BC'), 2/4)
        self.assertAlmostEqual(dist_lcsstr('ABCD', 'AD'), 3/4)
        self.assertAlmostEqual(dist_lcsstr('ABCD', 'AC'), 3/4)
        self.assertAlmostEqual(dist_lcsstr('AB', 'CD'), 1)
        self.assertAlmostEqual(dist_lcsstr('ABC', 'BCD'), 1/3)

        self.assertAlmostEqual(dist_lcsstr('DIXON', 'DICKSONX'), 6/8)

        # https://en.wikipedia.org/wiki/Longest_common_subsequence_problem
        self.assertAlmostEqual(dist_lcsstr('AGCAT', 'GAC'), 4/5)
        self.assertAlmostEqual(dist_lcsstr('XMJYAUZ', 'MZJAWXU'), 6/7)

        # https://github.com/jwmerrill/factor/blob/master/basis/lcs/lcs-tests.factor
        self.assertAlmostEqual(dist_lcsstr('hell', 'hello'), 1/5)
        self.assertAlmostEqual(dist_lcsstr('hello', 'hell'), 1/5)
        self.assertAlmostEqual(dist_lcsstr('ell', 'hell'), 1/4)
        self.assertAlmostEqual(dist_lcsstr('hell', 'ell'), 1/4)
        self.assertAlmostEqual(dist_lcsstr('faxbcd', 'abdef'), 5/6)

        # http://www.unesco.org/culture/languages-atlas/assets/_core/php/qcubed_unit_tests.php
        self.assertAlmostEqual(dist_lcsstr('hello world', 'world war 2'), 6/11)
        self.assertAlmostEqual(dist_lcsstr('foo bar', 'bar foo'), 4/7)
        self.assertAlmostEqual(dist_lcsstr('aaa', 'aa'), 1/3)
        self.assertAlmostEqual(dist_lcsstr('cc', 'bbbbcccccc'), 8/10)
        self.assertAlmostEqual(dist_lcsstr('ccc', 'bcbb'), 3/4)


class RatcliffObershelpTestCases(unittest.TestCase):
    """test cases for abydos.distance.sim_ratcliffobershelp, &
    abydos.distance.dist_ratcliffobershelp
    """
    def test_sim_ratcliffobershelp(self):
        """test abydos.distance.sim_ratcliffobershelp
        """
        # https://github.com/rockymadden/stringmetric/blob/master/core/src/test/scala/com/rockymadden/stringmetric/similarity/RatcliffObershelpMetricSpec.scala
        self.assertEqual(sim_ratcliffobershelp('', ''), 1)
        self.assertEqual(sim_ratcliffobershelp('abc', ''), 0)
        self.assertEqual(sim_ratcliffobershelp('', 'xyz'), 0)
        self.assertEqual(sim_ratcliffobershelp('abc', 'abc'), 1)
        self.assertEqual(sim_ratcliffobershelp('123', '123'), 1)
        self.assertEqual(sim_ratcliffobershelp('abc', 'xyz'), 0)
        self.assertEqual(sim_ratcliffobershelp('123', '456'), 0)
        self.assertAlmostEqual(sim_ratcliffobershelp('aleksander', 'alexandre'),
                               0.7368421052631579)
        self.assertAlmostEqual(sim_ratcliffobershelp('alexandre', 'aleksander'),
                               0.7368421052631579)
        self.assertAlmostEqual(sim_ratcliffobershelp('pennsylvania',
                                                     'pencilvaneya'),
                               0.6666666666666666)
        self.assertAlmostEqual(sim_ratcliffobershelp('pencilvaneya',
                                                     'pennsylvania'),
                               0.6666666666666666)
        self.assertAlmostEqual(sim_ratcliffobershelp('abcefglmn', 'abefglmo'),
                               0.8235294117647058)
        self.assertAlmostEqual(sim_ratcliffobershelp('abefglmo', 'abcefglmn'),
                               0.8235294117647058)

        with open(TESTDIR+'/variantNames.csv') as cav_testset:
            next(cav_testset)
            for line in cav_testset:
                line = line.split(',')
                word1, word2 = line[0], line[4]
                self.assertAlmostEqual(sim_ratcliffobershelp(word1, word2),
                                       SequenceMatcher(None, word1,
                                                       word2).ratio())

        with open(TESTDIR+'/wikipediaCommonMisspellings.csv') as misspellings:
            next(misspellings)
            for line in misspellings:
                line = line.upper()
                line = ''.join([_ for _ in line.strip() if _ in
                                tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ,')])
                word1, word2 = line.split(',')
                #print word1, word2e
                self.assertAlmostEqual(sim_ratcliffobershelp(word1, word2),
                                       SequenceMatcher(None, word1,
                                                       word2).ratio())

    def test_dist_ratcliffobershelp(self):
        """test abydos.distance.dist_ratcliffobershelp
        """
        # https://github.com/rockymadden/stringmetric/blob/master/core/src/test/scala/com/rockymadden/stringmetric/similarity/RatcliffObershelpMetricSpec.scala
        self.assertEqual(dist_ratcliffobershelp('', ''), 0)
        self.assertEqual(dist_ratcliffobershelp('abc', ''), 1)
        self.assertEqual(dist_ratcliffobershelp('', 'xyz'), 1)
        self.assertEqual(dist_ratcliffobershelp('abc', 'abc'), 0)
        self.assertEqual(dist_ratcliffobershelp('123', '123'), 0)
        self.assertEqual(dist_ratcliffobershelp('abc', 'xyz'), 1)
        self.assertEqual(dist_ratcliffobershelp('123', '456'), 1)
        self.assertAlmostEqual(dist_ratcliffobershelp('aleksander',
                                                      'alexandre'),
                               0.2631578947368421)
        self.assertAlmostEqual(dist_ratcliffobershelp('alexandre',
                                                      'aleksander'),
                               0.2631578947368421)
        self.assertAlmostEqual(dist_ratcliffobershelp('pennsylvania',
                                                     'pencilvaneya'),
                               0.3333333333333333)
        self.assertAlmostEqual(dist_ratcliffobershelp('pencilvaneya',
                                                     'pennsylvania'),
                               0.3333333333333333)
        self.assertAlmostEqual(dist_ratcliffobershelp('abcefglmn', 'abefglmo'),
                               0.1764705882352941)
        self.assertAlmostEqual(dist_ratcliffobershelp('abefglmo', 'abcefglmn'),
                               0.1764705882352941)


class MraCompareTestCases(unittest.TestCase):
    """test cases for abydos.distance.mra_compare
    """
    def test_mra_compare(self):
        """test abydos.distance.mra_compare
        """
        self.assertEqual(mra_compare('', ''), 6)
        self.assertEqual(mra_compare('a', 'a'), 6)
        self.assertEqual(mra_compare('abcdefg', 'abcdefg'), 6)
        self.assertEqual(mra_compare('abcdefg', ''), 0)
        self.assertEqual(mra_compare('', 'abcdefg'), 0)

        # https://en.wikipedia.org/wiki/Match_rating_approach
        self.assertEqual(mra_compare('Byrne', 'Boern'), 5)
        self.assertEqual(mra_compare('Smith', 'Smyth'), 5)
        self.assertEqual(mra_compare('Catherine', 'Kathryn'), 4)

class CompressionTestCases(unittest.TestCase):
    """test cases for abydos.distance.dist_compression &
    abydos.distance.sim_compression
    """
    def test_dist_compression(self):
        """test abydos.distance.dist_compression
        """
        self.assertEqual(dist_compression('', ''), 0)
        self.assertEqual(dist_compression('', '', 'bzip2'), 0)
        self.assertEqual(dist_compression('', '', 'lzma'), 0)
        self.assertEqual(dist_compression('', '', 'zlib'), 0)

        self.assertGreater(dist_compression('a', ''), 0)
        self.assertGreater(dist_compression('a', '', 'bzip2'), 0)
        self.assertGreater(dist_compression('a', '', 'lzma'), 0)
        self.assertGreater(dist_compression('a', '', 'zlib'), 0)

        self.assertGreater(dist_compression('abcdefg', 'fg'), 0)
        self.assertGreater(dist_compression('abcdefg', 'fg', 'bzip2'), 0)
        self.assertGreater(dist_compression('abcdefg', 'fg', 'lzma'), 0)
        self.assertGreater(dist_compression('abcdefg', 'fg', 'zlib'), 0)

    def test_sim_compression(self):
        """test abydos.distance.sim_compression
        """
        self.assertEqual(sim_compression('', ''), 1)
        self.assertEqual(sim_compression('', '', 'bzip2'), 1)
        self.assertEqual(sim_compression('', '', 'lzma'), 1)
        self.assertEqual(sim_compression('', '', 'zlib'), 1)

        self.assertLess(sim_compression('a', ''), 1)
        self.assertLess(sim_compression('a', '', 'bzip2'), 1)
        self.assertLess(sim_compression('a', '', 'lzma'), 1)
        self.assertLess(sim_compression('a', '', 'zlib'), 1)

        self.assertLess(sim_compression('abcdefg', 'fg'), 1)
        self.assertLess(sim_compression('abcdefg', 'fg', 'bzip2'), 1)
        self.assertLess(sim_compression('abcdefg', 'fg', 'lzma'), 1)
        self.assertLess(sim_compression('abcdefg', 'fg', 'zlib'), 1)


class MongeElkanTestCases(unittest.TestCase):
    """test cases for abydos.distance.sim_monge_elkan &
    abydos.distance.dist_monge_elkan
    """
    def test_sim_monge_elkan(self):
        """test abydos.distance.sim_monge_elkan
        """
        self.assertEqual(sim_monge_elkan('', ''), 1)
        self.assertEqual(sim_monge_elkan('', 'a'), 0)
        #TODO: Add non-trivial tests

    def test_dist_monge_elkan(self):
        """test abydos.distance.dist_monge_elkan
        """
        self.assertEqual(dist_monge_elkan('', ''), 0)
        self.assertEqual(dist_monge_elkan('', 'a'), 1)
        #TODO: Add non-trivial tests


class IdentityTestCases(unittest.TestCase):
    """test cases for abydos.distance.sim_ident &
    abydos.distance.dist_ident
    """
    def test_sim_ident(self):
        """test abydos.distance.sim_ident
        """
        self.assertEqual(sim_ident('', ''), 1)
        self.assertEqual(sim_ident('', 'a'), 0)
        self.assertEqual(sim_ident('a', ''), 0)
        self.assertEqual(sim_ident('a', 'a'), 1)
        self.assertEqual(sim_ident('abcd', 'abcd'), 1)
        self.assertEqual(sim_ident('abcd', 'dcba'), 0)
        self.assertEqual(sim_ident('abc', 'cba'), 0)

    def test_dist_ident(self):
        """test abydos.distance.dist_ident
        """
        self.assertEqual(dist_ident('', ''), 0)
        self.assertEqual(dist_ident('', 'a'), 1)
        self.assertEqual(dist_ident('a', ''), 1)
        self.assertEqual(dist_ident('a', 'a'), 0)
        self.assertEqual(dist_ident('abcd', 'abcd'), 0)
        self.assertEqual(dist_ident('abcd', 'dcba'), 1)
        self.assertEqual(dist_ident('abc', 'cba'), 1)


def _sim_wikipedia(src, tar):
    # Values copied from:
    # https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm
    nw_matrix = {('A', 'A'):10, ('G', 'G'):7,
                 ('C', 'C'):9, ('T', 'T'):8,
                 ('A', 'G'):-1, ('A', 'C'):-3, ('A', 'T'):-4,
                 ('G', 'C'):-5, ('G', 'T'):-3,
                 ('C', 'T'):0}
    return sim_matrix(src, tar, nw_matrix, symmetric=True, alphabet='CGAT')

class MatrixSimTestCases(unittest.TestCase):
    """test cases for abydos.distance.sim_matrix
    """
    def test_sim_matrix(self):
        """test abydos.distance.sim_matrix
        """
        self.assertEqual(sim_matrix('', ''), 1)
        self.assertEqual(sim_matrix('', 'a'), 0)
        self.assertEqual(sim_matrix('a', ''), 0)
        self.assertEqual(sim_matrix('a', 'a'), 1)
        self.assertEqual(sim_matrix('abcd', 'abcd'), 1)
        self.assertEqual(sim_matrix('abcd', 'dcba'), 0)
        self.assertEqual(sim_matrix('abc', 'cba'), 0)

        # https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm
        self.assertEqual(_sim_wikipedia('A','C'), -3)
        self.assertEqual(_sim_wikipedia('G','G'), 7)
        self.assertEqual(_sim_wikipedia('A','A'), 10)
        self.assertEqual(_sim_wikipedia('T','A'), -4)
        self.assertEqual(_sim_wikipedia('T','C'), 0)
        self.assertEqual(_sim_wikipedia('A','G'), -1)
        self.assertEqual(_sim_wikipedia('C','T'), 0)


class NeedlemanWunschTestCases(unittest.TestCase):
    """test cases for abydos.distance.needleman_wunsch
    """
    def test_needleman_wunsch(self):
        """test abydos.distance.needleman_wunsch
        """
        _sim_nw = lambda x,y: 2*float(x is y)-1

        self.assertEqual(needleman_wunsch('', ''), 0)

        # https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm
        self.assertEqual(needleman_wunsch('GATTACA', 'GCATGCU',
                                          -1, _sim_nw), 0)
        self.assertEqual(needleman_wunsch('AGACTAGTTAC', 'CGAGACGT',
                                          -5, _sim_wikipedia), 16)

        # checked against http://ds9a.nl/nwunsch/ (mismatch=1, gap=5, skew=5)
        self.assertEqual(needleman_wunsch('CGATATCAG', 'TGACGSTGC',
                                          -5, _sim_nw), -5)
        self.assertEqual(needleman_wunsch('AGACTAGTTAC', 'TGACGSTGC',
                                          -5, _sim_nw), -7)
        self.assertEqual(needleman_wunsch('AGACTAGTTAC', 'CGAGACGT',
                                          -5, _sim_nw), -15)

        # checked against http://ds9a.nl/nwunsch/ (mismatch=1, gap=2, skew=2)
        self.assertEqual(needleman_wunsch('Niall', 'Njall', -2, _sim_nw), 3)
        self.assertEqual(needleman_wunsch('Niall', 'Njáll', -2, _sim_nw), 1)
        self.assertEqual(needleman_wunsch('Niall', 'Neil', -2, _sim_nw), -2)
        self.assertEqual(needleman_wunsch('Niall', 'Neal', -2, _sim_nw), 0)
        self.assertEqual(needleman_wunsch('Niall', 'Niall Noígíallach',
                                          -2, _sim_nw), -19)
        self.assertEqual(needleman_wunsch('Niall', 'Uí Néill', -2, _sim_nw), -5)
        self.assertEqual(needleman_wunsch('Niall', 'Nigel', -2, _sim_nw), 1)
        self.assertEqual(needleman_wunsch('Niall', 'O\'Neill', -2, _sim_nw), -3)
        self.assertEqual(needleman_wunsch('Niall', 'MacNeil', -2, _sim_nw), -7)
        self.assertEqual(needleman_wunsch('Niall', 'MacNele', -2, _sim_nw), -7)
        self.assertEqual(needleman_wunsch('Niall', 'Neel', -2, _sim_nw), -2)
        self.assertEqual(needleman_wunsch('Niall', 'Nele', -2, _sim_nw), -2)
        self.assertEqual(needleman_wunsch('Niall', 'Nigelli', -2, _sim_nw), -1)
        self.assertEqual(needleman_wunsch('Niall', 'Nel', -2, _sim_nw), -3)
        self.assertEqual(needleman_wunsch('Niall', 'Kneale', -2, _sim_nw), -3)

if __name__ == '__main__':
    unittest.main()
