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
from abydos._compat import _range
from abydos.distance import levenshtein, dist_levenshtein, sim_levenshtein, \
    damerau_levenshtein, dist_damerau, sim_damerau, hamming, dist_hamming, \
    sim_hamming, sim_tversky, dist_tversky, sim_dice, dist_dice, sim_jaccard, \
    dist_jaccard, sim_overlap, dist_overlap, sim_tanimoto, tanimoto, \
    sim_cosine, dist_cosine, sim_strcmp95, dist_strcmp95, sim_jaro_winkler, \
    dist_jaro_winkler, lcsseq, sim_lcsseq, dist_lcsseq, lcsstr, sim_lcsstr, \
    dist_lcsstr, sim_ratcliff_obershelp, dist_ratcliff_obershelp, mra_compare, \
    sim_mra, dist_mra, sim_compression, dist_compression, sim_monge_elkan, \
    dist_monge_elkan, sim_ident, dist_ident, sim_matrix, needleman_wunsch, \
    smith_waterman, gotoh, sim_length, dist_length, sim_prefix, dist_prefix, \
    sim_suffix, dist_suffix, sim_mlipns, dist_mlipns, bag, sim_bag, dist_bag, \
    sim, dist
from abydos.qgram import QGrams
import math
from difflib import SequenceMatcher
import os

TESTDIR = os.path.dirname(__file__)

NIALL = ('Niall', 'Neal', 'Neil', 'Njall', 'Njáll', 'Nigel', 'Neel', 'Nele',
         'Nigelli', 'Nel', 'Kneale', 'Uí Néill', 'O\'Neill', 'MacNeil',
         'MacNele', 'Niall Noígíallach')

class LevenshteinTestCases(unittest.TestCase):
    """test cases for abydos.distance.levenshtein,
    abydos.distance.dist_levenshtein, abydos.distance.sim_levenshtein,
    abydos.distance.damerau, abydos.distance.dist_damerau, &
    abydos.distance.sim_damerau
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

    def test_damerau_levenshtein(self):
        """test abydos.distance.damerau_levenshtein
        """
        self.assertEqual(damerau_levenshtein('CA', 'ABC'), 2)
        self.assertEqual(damerau_levenshtein('', 'b', cost=(5, 7, 10, 10)), 5)
        self.assertEqual(damerau_levenshtein('a', 'ab', cost=(5, 7, 10, 10)), 5)
        self.assertEqual(damerau_levenshtein('b', '', cost=(5, 7, 10, 10)), 7)
        self.assertEqual(damerau_levenshtein('ab', 'a', cost=(5, 7, 10, 10)), 7)
        self.assertEqual(damerau_levenshtein('a', 'b', cost=(10, 10, 5, 10)), 5)
        self.assertEqual(damerau_levenshtein('ac', 'bc',
                                             cost=(10, 10, 5, 10)), 5)
        self.assertEqual(damerau_levenshtein('ab', 'ba',
                                             cost=(5, 5, 10, 5)), 5)
        self.assertEqual(damerau_levenshtein('abc', 'bac',
                                             cost=(5, 5, 10, 5)), 5)
        self.assertEqual(damerau_levenshtein('cab', 'cba',
                                             cost=(5, 5, 10, 5)), 5)
        self.assertRaises(ValueError, damerau_levenshtein, 'ab', 'ba',
                          cost=(10, 10, 10, 5))

    def test_dist_damerau(self):
        """test abydos.distance.dist_damerau
        """
        self.assertEqual(dist_damerau('', ''), 0)

        self.assertEqual(dist_damerau('a', 'a'), 0)
        self.assertEqual(dist_damerau('ab', 'ab'), 0)
        self.assertEqual(dist_damerau('', 'a'), 1)
        self.assertEqual(dist_damerau('', 'ab'), 1)
        self.assertEqual(dist_damerau('a', 'c'), 1)

        self.assertAlmostEqual(dist_damerau('abc', 'ac'), 1/3)
        self.assertAlmostEqual(dist_damerau('abbc', 'ac'), 1/2)
        self.assertAlmostEqual(dist_damerau('abbc', 'abc'), 1/4)

        self.assertAlmostEqual(dist_damerau('CA', 'ABC'), 2/3)
        self.assertAlmostEqual(dist_damerau('', 'b', cost=(5, 7, 10, 10)), 1)
        self.assertAlmostEqual(dist_damerau('a', 'ab',
                                            cost=(5, 7, 10, 10)), 1/2)
        self.assertAlmostEqual(dist_damerau('b', '', cost=(5, 7, 10, 10)), 1)
        self.assertAlmostEqual(dist_damerau('ab', 'a',
                                            cost=(5, 7, 10, 10)), 1/2)
        self.assertAlmostEqual(dist_damerau('a', 'b',
                                            cost=(10, 10, 5, 10)), 1/2)
        self.assertAlmostEqual(dist_damerau('ac', 'bc',
                                             cost=(10, 10, 5, 10)), 1/4)
        self.assertAlmostEqual(dist_damerau('ab', 'ba',
                                             cost=(5, 5, 10, 5)), 1/2)
        self.assertAlmostEqual(dist_damerau('abc', 'bac',
                                             cost=(5, 5, 10, 5)), 1/3)
        self.assertAlmostEqual(dist_damerau('cab', 'cba',
                                             cost=(5, 5, 10, 5)), 1/3)
        self.assertRaises(ValueError, dist_damerau, 'ab', 'ba',
                          cost=(10, 10, 10, 5))

    def test_sim_damerau(self):
        """test abydos.distance.sim_damerau
        """
        self.assertEqual(sim_damerau('', ''), 1)

        self.assertEqual(sim_damerau('a', 'a'), 1)
        self.assertEqual(sim_damerau('ab', 'ab'), 1)
        self.assertEqual(sim_damerau('', 'a'), 0)
        self.assertEqual(sim_damerau('', 'ab'), 0)
        self.assertEqual(sim_damerau('a', 'c'), 0)

        self.assertAlmostEqual(sim_damerau('abc', 'ac'), 2/3)
        self.assertAlmostEqual(sim_damerau('abbc', 'ac'), 1/2)
        self.assertAlmostEqual(sim_damerau('abbc', 'abc'), 3/4)

        self.assertAlmostEqual(sim_damerau('CA', 'ABC'), 1/3)
        self.assertAlmostEqual(sim_damerau('', 'b', cost=(5, 7, 10, 10)), 0)
        self.assertAlmostEqual(sim_damerau('a', 'ab', cost=(5, 7, 10, 10)), 1/2)
        self.assertAlmostEqual(sim_damerau('b', '', cost=(5, 7, 10, 10)), 0)
        self.assertAlmostEqual(sim_damerau('ab', 'a', cost=(5, 7, 10, 10)), 1/2)
        self.assertAlmostEqual(sim_damerau('a', 'b', cost=(10, 10, 5, 10)), 1/2)
        self.assertAlmostEqual(sim_damerau('ac', 'bc',
                                             cost=(10, 10, 5, 10)), 3/4)
        self.assertAlmostEqual(sim_damerau('ab', 'ba',
                                             cost=(5, 5, 10, 5)), 1/2)
        self.assertAlmostEqual(sim_damerau('abc', 'bac',
                                             cost=(5, 5, 10, 5)), 2/3)
        self.assertAlmostEqual(sim_damerau('cab', 'cba',
                                             cost=(5, 5, 10, 5)), 2/3)
        self.assertRaises(ValueError, sim_damerau, 'ab', 'ba',
                          cost=(10, 10, 10, 5))


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


NONQ_FROM = 'The quick brown fox jumped over the lazy dog.'
NONQ_TO = 'That brown dog jumped over the fox.'

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

        self.assertEqual(sim_tversky('', '', 2), 1)
        self.assertEqual(sim_tversky('nelson', '', 2), 0)
        self.assertEqual(sim_tversky('', 'neilsen', 2), 0)
        self.assertAlmostEqual(sim_tversky('nelson', 'neilsen', 2), 4/11)

        # test valid alpha & beta
        self.assertRaises(ValueError, sim_tversky, 'abcd', 'dcba', 2, -1, -1)
        self.assertRaises(ValueError, sim_tversky, 'abcd', 'dcba', 2, -1, 0)
        self.assertRaises(ValueError, sim_tversky, 'abcd', 'dcba', 2, 0, -1)

        # test empty QGrams
        self.assertAlmostEqual(sim_tversky('nelson', 'neilsen', 7), 0.0)

        # test unequal alpha & beta
        self.assertAlmostEqual(sim_tversky('niall', 'neal', 2, 2, 1), 3/11)
        self.assertAlmostEqual(sim_tversky('niall', 'neal', 2, 1, 2), 3/10)
        self.assertAlmostEqual(sim_tversky('niall', 'neal', 2, 2, 2), 3/13)

        # test bias parameter
        self.assertAlmostEqual(sim_tversky('niall', 'neal', 2, 1, 1, 0.5), 7/11)
        self.assertAlmostEqual(sim_tversky('niall', 'neal', 2, 2, 1, 0.5), 7/9)
        self.assertAlmostEqual(sim_tversky('niall', 'neal', 2, 1, 2, 0.5), 7/15)
        self.assertAlmostEqual(sim_tversky('niall', 'neal', 2, 2, 2, 0.5), 7/11)

        # supplied q-gram tests
        self.assertEqual(sim_tversky(QGrams(''), QGrams('')), 1)
        self.assertEqual(sim_tversky(QGrams('nelson'), QGrams('')), 0)
        self.assertEqual(sim_tversky(QGrams(''), QGrams('neilsen')), 0)
        self.assertAlmostEqual(sim_tversky(QGrams('nelson'), QGrams('neilsen')),
                               4/11)

        # non-q-gram tests
        self.assertEqual(sim_tversky('', '', None), 1)
        self.assertEqual(sim_tversky('the quick', '', None), 0)
        self.assertEqual(sim_tversky('', 'the quick', None), 0)
        self.assertAlmostEqual(sim_tversky(NONQ_FROM, NONQ_TO, None), 1/3)
        self.assertAlmostEqual(sim_tversky(NONQ_TO, NONQ_FROM, None), 1/3)

    def test_dist_tversky(self):
        """test abydos.distance.dist_tversky
        """
        self.assertEqual(dist_tversky('', ''), 0)
        self.assertEqual(dist_tversky('nelson', ''), 1)
        self.assertEqual(dist_tversky('', 'neilsen'), 1)
        self.assertAlmostEqual(dist_tversky('nelson', 'neilsen'), 7/11)

        self.assertEqual(dist_tversky('', '', 2), 0)
        self.assertEqual(dist_tversky('nelson', '', 2), 1)
        self.assertEqual(dist_tversky('', 'neilsen', 2), 1)
        self.assertAlmostEqual(dist_tversky('nelson', 'neilsen', 2), 7/11)

        # test valid alpha & beta
        self.assertRaises(ValueError, dist_tversky, 'abcd', 'dcba', 2, -1, -1)
        self.assertRaises(ValueError, dist_tversky, 'abcd', 'dcba', 2, -1, 0)
        self.assertRaises(ValueError, dist_tversky, 'abcd', 'dcba', 2, 0, -1)

        # test empty QGrams
        self.assertAlmostEqual(dist_tversky('nelson', 'neilsen', 7), 1.0)

        # test unequal alpha & beta
        self.assertAlmostEqual(dist_tversky('niall', 'neal', 2, 2, 1), 8/11)
        self.assertAlmostEqual(dist_tversky('niall', 'neal', 2, 1, 2), 7/10)
        self.assertAlmostEqual(dist_tversky('niall', 'neal', 2, 2, 2), 10/13)

        # test bias parameter
        self.assertAlmostEqual(dist_tversky('niall', 'neal', 2, 1, 1, 0.5),
                               4/11)
        self.assertAlmostEqual(dist_tversky('niall', 'neal', 2, 2, 1, 0.5), 2/9)
        self.assertAlmostEqual(dist_tversky('niall', 'neal', 2, 1, 2, 0.5),
                               8/15)
        self.assertAlmostEqual(dist_tversky('niall', 'neal', 2, 2, 2, 0.5),
                               4/11)

        # supplied q-gram tests
        self.assertEqual(dist_tversky(QGrams(''), QGrams('')), 0)
        self.assertEqual(dist_tversky(QGrams('nelson'), QGrams('')), 1)
        self.assertEqual(dist_tversky(QGrams(''), QGrams('neilsen')), 1)
        self.assertAlmostEqual(dist_tversky(QGrams('nelson'),
                                            QGrams('neilsen')), 7/11)

        # non-q-gram tests
        self.assertEqual(dist_tversky('', '', None), 0)
        self.assertEqual(dist_tversky('the quick', '', None), 1)
        self.assertEqual(dist_tversky('', 'the quick', None), 1)
        self.assertAlmostEqual(dist_tversky(NONQ_FROM, NONQ_TO, None), 2/3)
        self.assertAlmostEqual(dist_tversky(NONQ_TO, NONQ_FROM, None), 2/3)


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

        self.assertEqual(sim_dice('', '', 2), 1)
        self.assertEqual(sim_dice('nelson', '', 2), 0)
        self.assertEqual(sim_dice('', 'neilsen', 2), 0)
        self.assertAlmostEqual(sim_dice('nelson', 'neilsen', 2), 8/15)

        # supplied q-gram tests
        self.assertEqual(sim_dice(QGrams(''), QGrams('')), 1)
        self.assertEqual(sim_dice(QGrams('nelson'), QGrams('')), 0)
        self.assertEqual(sim_dice(QGrams(''), QGrams('neilsen')), 0)
        self.assertAlmostEqual(sim_dice(QGrams('nelson'), QGrams('neilsen')),
                               8/15)

        # non-q-gram tests
        self.assertEqual(sim_dice('', '', None), 1)
        self.assertEqual(sim_dice('the quick', '', None), 0)
        self.assertEqual(sim_dice('', 'the quick', None), 0)
        self.assertAlmostEqual(sim_dice(NONQ_FROM, NONQ_TO, None), 1/2)
        self.assertAlmostEqual(sim_dice(NONQ_TO, NONQ_FROM, None), 1/2)

    def test_dist_dice(self):
        """test abydos.distance.dist_dice
        """
        self.assertEqual(dist_dice('', ''), 0)
        self.assertEqual(dist_dice('nelson', ''), 1)
        self.assertEqual(dist_dice('', 'neilsen'), 1)
        self.assertAlmostEqual(dist_dice('nelson', 'neilsen'), 7/15)

        self.assertEqual(dist_dice('', '', 2), 0)
        self.assertEqual(dist_dice('nelson', '', 2), 1)
        self.assertEqual(dist_dice('', 'neilsen', 2), 1)
        self.assertAlmostEqual(dist_dice('nelson', 'neilsen', 2), 7/15)

        # supplied q-gram tests
        self.assertEqual(dist_dice(QGrams(''), QGrams('')), 0)
        self.assertEqual(dist_dice(QGrams('nelson'), QGrams('')), 1)
        self.assertEqual(dist_dice(QGrams(''), QGrams('neilsen')), 1)
        self.assertAlmostEqual(dist_dice(QGrams('nelson'), QGrams('neilsen')),
                               7/15)

        # non-q-gram tests
        self.assertEqual(dist_dice('', '', None), 0)
        self.assertEqual(dist_dice('the quick', '', None), 1)
        self.assertEqual(dist_dice('', 'the quick', None), 1)
        self.assertAlmostEqual(dist_dice(NONQ_FROM, NONQ_TO, None), 1/2)
        self.assertAlmostEqual(dist_dice(NONQ_TO, NONQ_FROM, None), 1/2)


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

        self.assertEqual(sim_jaccard('', '', 2), 1)
        self.assertEqual(sim_jaccard('nelson', '', 2), 0)
        self.assertEqual(sim_jaccard('', 'neilsen', 2), 0)
        self.assertAlmostEqual(sim_jaccard('nelson', 'neilsen', 2), 4/11)

        # supplied q-gram tests
        self.assertEqual(sim_jaccard(QGrams(''), QGrams('')), 1)
        self.assertEqual(sim_jaccard(QGrams('nelson'), QGrams('')), 0)
        self.assertEqual(sim_jaccard(QGrams(''), QGrams('neilsen')), 0)
        self.assertAlmostEqual(sim_jaccard(QGrams('nelson'), QGrams('neilsen')),
                               4/11)

        # non-q-gram tests
        self.assertEqual(sim_jaccard('', '', None), 1)
        self.assertEqual(sim_jaccard('the quick', '', None), 0)
        self.assertEqual(sim_jaccard('', 'the quick', None), 0)
        self.assertAlmostEqual(sim_jaccard(NONQ_FROM, NONQ_TO, None), 1/3)
        self.assertAlmostEqual(sim_jaccard(NONQ_TO, NONQ_FROM, None), 1/3)

    def test_dist_jaccard(self):
        """test abydos.distance.dist_jaccard
        """
        self.assertEqual(dist_jaccard('', ''), 0)
        self.assertEqual(dist_jaccard('nelson', ''), 1)
        self.assertEqual(dist_jaccard('', 'neilsen'), 1)
        self.assertAlmostEqual(dist_jaccard('nelson', 'neilsen'), 7/11)

        self.assertEqual(dist_jaccard('', '', 2), 0)
        self.assertEqual(dist_jaccard('nelson', '', 2), 1)
        self.assertEqual(dist_jaccard('', 'neilsen', 2), 1)
        self.assertAlmostEqual(dist_jaccard('nelson', 'neilsen', 2), 7/11)

        # supplied q-gram tests
        self.assertEqual(dist_jaccard(QGrams(''), QGrams('')), 0)
        self.assertEqual(dist_jaccard(QGrams('nelson'), QGrams('')), 1)
        self.assertEqual(dist_jaccard(QGrams(''), QGrams('neilsen')), 1)
        self.assertAlmostEqual(dist_jaccard(QGrams('nelson'),
                                            QGrams('neilsen')), 7/11)

        # non-q-gram tests
        self.assertEqual(dist_jaccard('', '', None), 0)
        self.assertEqual(dist_jaccard('the quick', '', None), 1)
        self.assertEqual(dist_jaccard('', 'the quick', None), 1)
        self.assertAlmostEqual(dist_jaccard(NONQ_FROM, NONQ_TO, None), 2/3)
        self.assertAlmostEqual(dist_jaccard(NONQ_TO, NONQ_FROM, None), 2/3)


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

        self.assertEqual(sim_overlap('', '', 2), 1)
        self.assertEqual(sim_overlap('nelson', '', 2), 0)
        self.assertEqual(sim_overlap('', 'neilsen', 2), 0)
        self.assertAlmostEqual(sim_overlap('nelson', 'neilsen', 2), 4/7)

        # supplied q-gram tests
        self.assertEqual(sim_overlap(QGrams(''), QGrams('')), 1)
        self.assertEqual(sim_overlap(QGrams('nelson'), QGrams('')), 0)
        self.assertEqual(sim_overlap(QGrams(''), QGrams('neilsen')), 0)
        self.assertAlmostEqual(sim_overlap(QGrams('nelson'), QGrams('neilsen')),
                               4/7)

        # non-q-gram tests
        self.assertEqual(sim_overlap('', '', None), 1)
        self.assertEqual(sim_overlap('the quick', '', None), 0)
        self.assertEqual(sim_overlap('', 'the quick', None), 0)
        self.assertAlmostEqual(sim_overlap(NONQ_FROM, NONQ_TO, None), 4/7)
        self.assertAlmostEqual(sim_overlap(NONQ_TO, NONQ_FROM, None), 4/7)

    def test_dist_overlap(self):
        """test abydos.distance.dist_overlap
        """
        self.assertEqual(dist_overlap('', ''), 0)
        self.assertEqual(dist_overlap('nelson', ''), 1)
        self.assertEqual(dist_overlap('', 'neilsen'), 1)
        self.assertAlmostEqual(dist_overlap('nelson', 'neilsen'), 3/7)

        self.assertEqual(dist_overlap('', '', 2), 0)
        self.assertEqual(dist_overlap('nelson', '', 2), 1)
        self.assertEqual(dist_overlap('', 'neilsen', 2), 1)
        self.assertAlmostEqual(dist_overlap('nelson', 'neilsen', 2), 3/7)

        # supplied q-gram tests
        self.assertEqual(dist_overlap(QGrams(''), QGrams('')), 0)
        self.assertEqual(dist_overlap(QGrams('nelson'), QGrams('')), 1)
        self.assertEqual(dist_overlap(QGrams(''), QGrams('neilsen')), 1)
        self.assertAlmostEqual(dist_overlap(QGrams('nelson'),
                                            QGrams('neilsen')), 3/7)

        # non-q-gram tests
        self.assertEqual(dist_overlap('', '', None), 0)
        self.assertEqual(dist_overlap('the quick', '', None), 1)
        self.assertEqual(dist_overlap('', 'the quick', None), 1)
        self.assertAlmostEqual(dist_overlap(NONQ_FROM, NONQ_TO, None), 3/7)
        self.assertAlmostEqual(dist_overlap(NONQ_TO, NONQ_FROM, None), 3/7)


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

        self.assertEqual(sim_tanimoto('', '', 2), 1)
        self.assertEqual(sim_tanimoto('nelson', '', 2), 0)
        self.assertEqual(sim_tanimoto('', 'neilsen', 2), 0)
        self.assertAlmostEqual(sim_tanimoto('nelson', 'neilsen', 2), 4/11)

        # supplied q-gram tests
        self.assertEqual(sim_tanimoto(QGrams(''), QGrams('')), 1)
        self.assertEqual(sim_tanimoto(QGrams('nelson'), QGrams('')), 0)
        self.assertEqual(sim_tanimoto(QGrams(''), QGrams('neilsen')), 0)
        self.assertAlmostEqual(sim_tanimoto(QGrams('nelson'),
                                            QGrams('neilsen')), 4/11)

        # non-q-gram tests
        self.assertEqual(sim_tanimoto('', '', None), 1)
        self.assertEqual(sim_tanimoto('the quick', '', None), 0)
        self.assertEqual(sim_tanimoto('', 'the quick', None), 0)
        self.assertAlmostEqual(sim_tanimoto(NONQ_FROM, NONQ_TO, None), 1/3)
        self.assertAlmostEqual(sim_tanimoto(NONQ_TO, NONQ_FROM, None), 1/3)

    def test_tanimoto(self):
        """test abydos.distance.tanimoto
        """
        self.assertEqual(tanimoto('', ''), 0)
        self.assertEqual(tanimoto('nelson', ''), float('-inf'))
        self.assertEqual(tanimoto('', 'neilsen'), float('-inf'))
        self.assertAlmostEqual(tanimoto('nelson', 'neilsen'),
                               math.log(4/11, 2))

        self.assertEqual(tanimoto('', '', 2), 0)
        self.assertEqual(tanimoto('nelson', '', 2), float('-inf'))
        self.assertEqual(tanimoto('', 'neilsen', 2), float('-inf'))
        self.assertAlmostEqual(tanimoto('nelson', 'neilsen', 2),
                               math.log(4/11, 2))

        # supplied q-gram tests
        self.assertEqual(tanimoto(QGrams(''), QGrams('')), 0)
        self.assertEqual(tanimoto(QGrams('nelson'), QGrams('')), float('-inf'))
        self.assertEqual(tanimoto(QGrams(''), QGrams('neilsen')), float('-inf'))
        self.assertAlmostEqual(tanimoto(QGrams('nelson'), QGrams('neilsen')),
                               math.log(4/11, 2))

        # non-q-gram tests
        self.assertEqual(tanimoto('', '', None), 0)
        self.assertEqual(tanimoto('the quick', '', None), float('-inf'))
        self.assertEqual(tanimoto('', 'the quick', None), float('-inf'))
        self.assertAlmostEqual(tanimoto(NONQ_FROM, NONQ_TO, None),
                               math.log(1/3, 2))
        self.assertAlmostEqual(tanimoto(NONQ_TO, NONQ_FROM, None),
                               math.log(1/3, 2))


class CosineSimilarityTestCases(unittest.TestCase):
    """test cases for abydos.distance.sim_cosine & abydos.distance.dist_cosine
    """
    def test_sim_cosine(self):
        """test abydos.distance.sim_cosine
        """
        self.assertEqual(sim_cosine('', ''), 1)
        self.assertEqual(sim_cosine('nelson', ''), 0)
        self.assertEqual(sim_cosine('', 'neilsen'), 0)
        self.assertAlmostEqual(sim_cosine('nelson', 'neilsen'),
                               4/math.sqrt(7*8))

        self.assertEqual(sim_cosine('', '', 2), 1)
        self.assertEqual(sim_cosine('nelson', '', 2), 0)
        self.assertEqual(sim_cosine('', 'neilsen', 2), 0)
        self.assertAlmostEqual(sim_cosine('nelson', 'neilsen', 2),
                               4/math.sqrt(7*8))

        # supplied q-gram tests
        self.assertEqual(sim_cosine(QGrams(''), QGrams('')), 1)
        self.assertEqual(sim_cosine(QGrams('nelson'), QGrams('')), 0)
        self.assertEqual(sim_cosine(QGrams(''), QGrams('neilsen')), 0)
        self.assertAlmostEqual(sim_cosine(QGrams('nelson'), QGrams('neilsen')),
                               4/math.sqrt(7*8))

        # non-q-gram tests
        self.assertEqual(sim_cosine('', '', None), 1)
        self.assertEqual(sim_cosine('the quick', '', None), 0)
        self.assertEqual(sim_cosine('', 'the quick', None), 0)
        self.assertAlmostEqual(sim_cosine(NONQ_FROM, NONQ_TO, None),
                               4/math.sqrt(9*7))
        self.assertAlmostEqual(sim_cosine(NONQ_TO, NONQ_FROM, None),
                               4/math.sqrt(9*7))

    def test_dist_cosine(self):
        """test abydos.distance.dist_cosine
        """
        self.assertEqual(dist_cosine('', ''), 0)
        self.assertEqual(dist_cosine('nelson', ''), 1)
        self.assertEqual(dist_cosine('', 'neilsen'), 1)
        self.assertAlmostEqual(dist_cosine('nelson', 'neilsen'),
                               1-(4/math.sqrt(7*8)))

        self.assertEqual(dist_cosine('', '', 2), 0)
        self.assertEqual(dist_cosine('nelson', '', 2), 1)
        self.assertEqual(dist_cosine('', 'neilsen', 2), 1)
        self.assertAlmostEqual(dist_cosine('nelson', 'neilsen', 2),
                               1-(4/math.sqrt(7*8)))

        # supplied q-gram tests
        self.assertEqual(dist_cosine(QGrams(''), QGrams('')), 0)
        self.assertEqual(dist_cosine(QGrams('nelson'), QGrams('')), 1)
        self.assertEqual(dist_cosine(QGrams(''), QGrams('neilsen')), 1)
        self.assertAlmostEqual(dist_cosine(QGrams('nelson'), QGrams('neilsen')),
                               1-(4/math.sqrt(7*8)))

        # non-q-gram tests
        self.assertEqual(dist_cosine('', '', None), 0)
        self.assertEqual(dist_cosine('the quick', '', None), 1)
        self.assertEqual(dist_cosine('', 'the quick', None), 1)
        self.assertAlmostEqual(dist_cosine(NONQ_FROM, NONQ_TO, None),
                               1-4/math.sqrt(9*7))
        self.assertAlmostEqual(dist_cosine(NONQ_TO, NONQ_FROM, None),
                               1-4/math.sqrt(9*7))


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

        self.assertAlmostEqual(sim_strcmp95('MARTHA', 'MARHTA'), 0.96111111)
        self.assertAlmostEqual(sim_strcmp95('DWAYNE', 'DUANE'), 0.873)
        self.assertAlmostEqual(sim_strcmp95('DIXON', 'DICKSONX'), 0.839333333)

        self.assertAlmostEqual(sim_strcmp95('ABCD', 'EFGH'), 0.0)

        # long_strings = True
        self.assertAlmostEqual(sim_strcmp95('DIXON', 'DICKSONX', True),
                               0.85393939)
        self.assertAlmostEqual(sim_strcmp95('DWAYNE', 'DUANE', True),
                               0.89609090)
        self.assertAlmostEqual(sim_strcmp95('MARTHA', 'MARHTA', True),
                               0.97083333)

    def test_dist_strcmp95(self):
        """test abydos.distance.dist_strcmp95
        """
        self.assertEqual(dist_strcmp95('', ''), 0)
        self.assertEqual(dist_strcmp95('MARTHA', ''), 1)
        self.assertEqual(dist_strcmp95('', 'MARTHA'), 1)
        self.assertEqual(dist_strcmp95('MARTHA', 'MARTHA'), 0)

        self.assertAlmostEqual(dist_strcmp95('MARTHA', 'MARHTA'), 0.03888888)
        self.assertAlmostEqual(dist_strcmp95('DWAYNE', 'DUANE'), 0.127)
        self.assertAlmostEqual(dist_strcmp95('DIXON', 'DICKSONX'), 0.160666666)

        self.assertAlmostEqual(dist_strcmp95('ABCD', 'EFGH'), 1.0)

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

        self.assertRaises(ValueError, sim_jaro_winkler, 'abcd', 'dcba',
                          boost_threshold=2)
        self.assertRaises(ValueError, sim_jaro_winkler, 'abcd', 'dcba',
                          boost_threshold=-1)
        self.assertRaises(ValueError, sim_jaro_winkler, 'abcd', 'dcba',
                          scaling_factor=0.3)
        self.assertRaises(ValueError, sim_jaro_winkler, 'abcd', 'dcba',
                          scaling_factor=-1)

        self.assertAlmostEqual(sim_jaro_winkler('ABCD', 'EFGH'), 0.0)

        # long_strings = True (applies only to Jaro-Winkler, not Jaro)
        self.assertEqual(sim_jaro_winkler('ABCD', 'EFGH', long_strings=True),
                         sim_jaro_winkler('ABCD', 'EFGH'))
        self.assertEqual(sim_jaro_winkler('DIXON', 'DICKSONX',
                                                mode='jaro',
                                                long_strings=True),
                               sim_jaro_winkler('DIXON', 'DICKSONX',
                                                mode='jaro'))
        self.assertAlmostEqual(sim_jaro_winkler('DIXON', 'DICKSONX',
                                                mode='winkler',
                                                long_strings=True), 0.83030303)
        self.assertAlmostEqual(sim_jaro_winkler('MARTHA', 'MARHTA',
                                                mode='winkler',
                                                long_strings=True), 0.97083333)

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

        self.assertRaises(ValueError, dist_jaro_winkler, 'abcd', 'dcba',
                          boost_threshold=2)
        self.assertRaises(ValueError, dist_jaro_winkler, 'abcd', 'dcba',
                          boost_threshold=-1)
        self.assertRaises(ValueError, dist_jaro_winkler, 'abcd', 'dcba',
                          scaling_factor=0.3)
        self.assertRaises(ValueError, dist_jaro_winkler, 'abcd', 'dcba',
                          scaling_factor=-1)

        self.assertAlmostEqual(dist_jaro_winkler('ABCD', 'EFGH'), 1.0)

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
    """test cases for abydos.distance.sim_ratcliff_obershelp, &
    abydos.distance.dist_ratcliff_obershelp
    """
    def test_sim_ratcliff_obershelp(self):
        """test abydos.distance.sim_ratcliff_obershelp
        """
        # https://github.com/rockymadden/stringmetric/blob/master/core/src/test/scala/com/rockymadden/stringmetric/similarity/RatcliffObershelpMetricSpec.scala
        self.assertEqual(sim_ratcliff_obershelp('', ''), 1)
        self.assertEqual(sim_ratcliff_obershelp('abc', ''), 0)
        self.assertEqual(sim_ratcliff_obershelp('', 'xyz'), 0)
        self.assertEqual(sim_ratcliff_obershelp('abc', 'abc'), 1)
        self.assertEqual(sim_ratcliff_obershelp('123', '123'), 1)
        self.assertEqual(sim_ratcliff_obershelp('abc', 'xyz'), 0)
        self.assertEqual(sim_ratcliff_obershelp('123', '456'), 0)
        self.assertAlmostEqual(sim_ratcliff_obershelp('aleksander',
                                                      'alexandre'),
                               0.7368421052631579)
        self.assertAlmostEqual(sim_ratcliff_obershelp('alexandre',
                                                      'aleksander'),
                               0.7368421052631579)
        self.assertAlmostEqual(sim_ratcliff_obershelp('pennsylvania',
                                                     'pencilvaneya'),
                               0.6666666666666666)
        self.assertAlmostEqual(sim_ratcliff_obershelp('pencilvaneya',
                                                     'pennsylvania'),
                               0.6666666666666666)
        self.assertAlmostEqual(sim_ratcliff_obershelp('abcefglmn', 'abefglmo'),
                               0.8235294117647058)
        self.assertAlmostEqual(sim_ratcliff_obershelp('abefglmo', 'abcefglmn'),
                               0.8235294117647058)

        with open(TESTDIR+'/variantNames.csv') as cav_testset:
            next(cav_testset)
            for line in cav_testset:
                line = line.split(',')
                word1, word2 = line[0], line[4]
                self.assertAlmostEqual(sim_ratcliff_obershelp(word1, word2),
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
                self.assertAlmostEqual(sim_ratcliff_obershelp(word1, word2),
                                       SequenceMatcher(None, word1,
                                                       word2).ratio())

    def test_dist_ratcliff_obershelp(self):
        """test abydos.distance.dist_ratcliff_obershelp
        """
        # https://github.com/rockymadden/stringmetric/blob/master/core/src/test/scala/com/rockymadden/stringmetric/similarity/RatcliffObershelpMetricSpec.scala
        self.assertEqual(dist_ratcliff_obershelp('', ''), 0)
        self.assertEqual(dist_ratcliff_obershelp('abc', ''), 1)
        self.assertEqual(dist_ratcliff_obershelp('', 'xyz'), 1)
        self.assertEqual(dist_ratcliff_obershelp('abc', 'abc'), 0)
        self.assertEqual(dist_ratcliff_obershelp('123', '123'), 0)
        self.assertEqual(dist_ratcliff_obershelp('abc', 'xyz'), 1)
        self.assertEqual(dist_ratcliff_obershelp('123', '456'), 1)
        self.assertAlmostEqual(dist_ratcliff_obershelp('aleksander',
                                                      'alexandre'),
                               0.2631578947368421)
        self.assertAlmostEqual(dist_ratcliff_obershelp('alexandre',
                                                      'aleksander'),
                               0.2631578947368421)
        self.assertAlmostEqual(dist_ratcliff_obershelp('pennsylvania',
                                                     'pencilvaneya'),
                               0.3333333333333333)
        self.assertAlmostEqual(dist_ratcliff_obershelp('pencilvaneya',
                                                     'pennsylvania'),
                               0.3333333333333333)
        self.assertAlmostEqual(dist_ratcliff_obershelp('abcefglmn', 'abefglmo'),
                               0.1764705882352941)
        self.assertAlmostEqual(dist_ratcliff_obershelp('abefglmo', 'abcefglmn'),
                               0.1764705882352941)


class MraTestCases(unittest.TestCase):
    """test cases for abydos.distance.mra_compare, abydos.distance.sim_mra &
    abydos.distance.dist_mra
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

        self.assertEqual(mra_compare('ab', 'abcdefgh'), 0)
        self.assertEqual(mra_compare('ab', 'ac'), 5)
        self.assertEqual(mra_compare('abcdefik', 'abcdefgh'), 3)
        self.assertEqual(mra_compare('xyz', 'abc'), 0)

    def test_sim_mra(self):
        """test abydos.distance.sim_mra
        """
        self.assertEqual(sim_mra('', ''), 1)
        self.assertEqual(sim_mra('a', 'a'), 1)
        self.assertEqual(sim_mra('abcdefg', 'abcdefg'), 1)
        self.assertEqual(sim_mra('abcdefg', ''), 0)
        self.assertEqual(sim_mra('', 'abcdefg'), 0)

        # https://en.wikipedia.org/wiki/Match_rating_approach
        self.assertEqual(sim_mra('Byrne', 'Boern'), 5/6)
        self.assertEqual(sim_mra('Smith', 'Smyth'), 5/6)
        self.assertEqual(sim_mra('Catherine', 'Kathryn'), 4/6)

        self.assertEqual(sim_mra('ab', 'abcdefgh'), 0)
        self.assertEqual(sim_mra('ab', 'ac'), 5/6)
        self.assertEqual(sim_mra('abcdefik', 'abcdefgh'), 3/6)
        self.assertEqual(sim_mra('xyz', 'abc'), 0)

    def test_dist_mra(self):
        """test abydos.distance.dist_mra
        """
        self.assertEqual(dist_mra('', ''), 0)
        self.assertEqual(dist_mra('a', 'a'), 0)
        self.assertEqual(dist_mra('abcdefg', 'abcdefg'), 0)
        self.assertEqual(dist_mra('abcdefg', ''), 1)
        self.assertEqual(dist_mra('', 'abcdefg'), 1)

        # https://en.wikipedia.org/wiki/Match_rating_approach
        self.assertAlmostEqual(dist_mra('Byrne', 'Boern'), 1/6)
        self.assertAlmostEqual(dist_mra('Smith', 'Smyth'), 1/6)
        self.assertAlmostEqual(dist_mra('Catherine', 'Kathryn'), 2/6)

        self.assertEqual(dist_mra('ab', 'abcdefgh'), 1)
        self.assertAlmostEqual(dist_mra('ab', 'ac'), 1/6)
        self.assertAlmostEqual(dist_mra('abcdefik', 'abcdefgh'), 3/6)
        self.assertEqual(dist_mra('xyz', 'abc'), 1)


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
        self.assertEqual(sim_monge_elkan('a', 'a'), 1)

        self.assertEqual(sim_monge_elkan('Niall', 'Neal'), 3/4)
        self.assertEqual(sim_monge_elkan('Niall', 'Njall'), 5/6)
        self.assertEqual(sim_monge_elkan('Niall', 'Niel'), 3/4)
        self.assertEqual(sim_monge_elkan('Niall', 'Nigel'), 3/4)

        self.assertEqual(sim_monge_elkan('Niall', 'Neal', sym=True), 31/40)
        self.assertEqual(sim_monge_elkan('Niall', 'Njall', sym=True), 5/6)
        self.assertEqual(sim_monge_elkan('Niall', 'Niel', sym=True), 31/40)
        self.assertAlmostEqual(sim_monge_elkan('Niall', 'Nigel', sym=True),
                               17/24)

    def test_dist_monge_elkan(self):
        """test abydos.distance.dist_monge_elkan
        """
        self.assertEqual(dist_monge_elkan('', ''), 0)
        self.assertEqual(dist_monge_elkan('', 'a'), 1)

        self.assertEqual(dist_monge_elkan('Niall', 'Neal'), 1/4)
        self.assertAlmostEqual(dist_monge_elkan('Niall', 'Njall'), 1/6)
        self.assertEqual(dist_monge_elkan('Niall', 'Niel'), 1/4)
        self.assertEqual(dist_monge_elkan('Niall', 'Nigel'), 1/4)

        self.assertAlmostEqual(dist_monge_elkan('Niall', 'Neal', sym=True),
                               9/40)
        self.assertAlmostEqual(dist_monge_elkan('Niall', 'Njall', sym=True),
                               1/6)
        self.assertAlmostEqual(dist_monge_elkan('Niall', 'Niel', sym=True),
                               9/40)
        self.assertAlmostEqual(dist_monge_elkan('Niall', 'Nigel', sym=True),
                               7/24)


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
    """Returns a similarity score for two DNA base pairs

    Values copied from:
    https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm
    """
    nw_matrix = {('A', 'A'):10, ('G', 'G'):7,
                 ('C', 'C'):9, ('T', 'T'):8,
                 ('A', 'G'):-1, ('A', 'C'):-3, ('A', 'T'):-4,
                 ('G', 'C'):-5, ('G', 'T'):-3,
                 ('C', 'T'):0}
    return sim_matrix(src, tar, nw_matrix, symmetric=True, alphabet='CGAT')


def _sim_nw(src, tar):
    """Returns 1 if src is tar, otherwise -1
    """
    return 2*float(src is tar)-1


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

        # https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm
        self.assertEqual(_sim_wikipedia('A', 'C'), -3)
        self.assertEqual(_sim_wikipedia('G', 'G'), 7)
        self.assertEqual(_sim_wikipedia('A', 'A'), 10)
        self.assertEqual(_sim_wikipedia('T', 'A'), -4)
        self.assertEqual(_sim_wikipedia('T', 'C'), 0)
        self.assertEqual(_sim_wikipedia('A', 'G'), -1)
        self.assertEqual(_sim_wikipedia('C', 'T'), 0)

        self.assertRaises(ValueError, sim_matrix, 'abc', 'cba', alphabet='ab')
        self.assertRaises(ValueError, sim_matrix, 'abc', 'ba', alphabet='ab')
        self.assertRaises(ValueError, sim_matrix, 'ab', 'cba', alphabet='ab')


class NeedlemanWunschTestCases(unittest.TestCase):
    """test cases for abydos.distance.needleman_wunsch
    """
    def test_needleman_wunsch(self):
        """test abydos.distance.needleman_wunsch
        """
        self.assertEqual(needleman_wunsch('', ''), 0)

        # https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm
        self.assertEqual(needleman_wunsch('GATTACA', 'GCATGCU',
                                          1, _sim_nw), 0)
        self.assertEqual(needleman_wunsch('AGACTAGTTAC', 'CGAGACGT',
                                          5, _sim_wikipedia), 16)

        # checked against http://ds9a.nl/nwunsch/ (mismatch=1, gap=5, skew=5)
        self.assertEqual(needleman_wunsch('CGATATCAG', 'TGACGSTGC',
                                          5, _sim_nw), -5)
        self.assertEqual(needleman_wunsch('AGACTAGTTAC', 'TGACGSTGC',
                                          5, _sim_nw), -7)
        self.assertEqual(needleman_wunsch('AGACTAGTTAC', 'CGAGACGT',
                                          5, _sim_nw), -15)

    def test_needleman_wunsch_nialls(self):
        """test abydos.distance.needleman_wunsch (Nialls set)
        """
        # checked against http://ds9a.nl/nwunsch/ (mismatch=1, gap=2, skew=2)
        nw_vals = (5, 0, -2, 3, 1, 1, -2, -2, -1, -3, -3, -5, -3, -7, -7, -19)
        for i in _range(len(NIALL)):
            self.assertEqual(needleman_wunsch(NIALL[0], NIALL[i], 2,
                                              _sim_nw), nw_vals[i])


class SmithWatermanTestCases(unittest.TestCase):
    """test cases for abydos.distance.smith_waterman
    """
    def test_smith_waterman(self):
        """test abydos.distance.smith_waterman
        """
        self.assertEqual(smith_waterman('', ''), 0)

        # https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm
        self.assertEqual(smith_waterman('GATTACA', 'GCATGCU',
                                          1, _sim_nw), 0)
        self.assertEqual(smith_waterman('AGACTAGTTAC', 'CGAGACGT',
                                          5, _sim_wikipedia), 26)

        self.assertEqual(smith_waterman('CGATATCAG', 'TGACGSTGC',
                                          5, _sim_nw), 0)
        self.assertEqual(smith_waterman('AGACTAGTTAC', 'TGACGSTGC',
                                          5, _sim_nw), 1)
        self.assertEqual(smith_waterman('AGACTAGTTAC', 'CGAGACGT',
                                          5, _sim_nw), 0)

    def test_smith_waterman_nialls(self):
        """test abydos.distance.smith_waterman (Nialls set)
        """
        sw_vals = (5, 1, 1, 3, 2, 1, 1, 0, 0, 1, 1, 2, 2, 1, 0, 0)
        for i in _range(len(NIALL)):
            self.assertEqual(smith_waterman(NIALL[0], NIALL[i], 2,
                                            _sim_nw), sw_vals[i])


class GotohTestCases(unittest.TestCase):
    """test cases for abydos.distance.gotoh
    """
    def test_gotoh(self):
        """test abydos.distance.needleman_wunsch_affine
        """
        self.assertEqual(gotoh('', ''), 0)

        # https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm
        self.assertEqual(gotoh('GATTACA', 'GCATGCU', 1, 1, _sim_nw), 0)
        self.assertGreaterEqual(gotoh('GATTACA', 'GCATGCU', 1, 0.5, _sim_nw),
                                needleman_wunsch('GATTACA', 'GCATGCU', 1,
                                                 _sim_nw))
        self.assertEqual(gotoh('AGACTAGTTAC', 'CGAGACGT', 5, 5, _sim_wikipedia),
                         16)
        self.assertGreaterEqual(gotoh('AGACTAGTTAC', 'CGAGACGT', 5, 2,
                                      _sim_wikipedia),
                                needleman_wunsch('AGACTAGTTAC', 'CGAGACGT', 5,
                                                 _sim_wikipedia))

        # checked against http://ds9a.nl/nwunsch/ (mismatch=1, gap=5, skew=5)
        self.assertEqual(gotoh('CGATATCAG', 'TGACGSTGC', 5, 5, _sim_nw), -5)
        self.assertGreaterEqual(gotoh('CGATATCAG', 'TGACGSTGC', 5, 2, _sim_nw),
                                needleman_wunsch('CGATATCAG', 'TGACGSTGC', 5,
                                                 _sim_nw))
        self.assertEqual(gotoh('AGACTAGTTAC', 'TGACGSTGC', 5, 5, _sim_nw), -7)
        self.assertGreaterEqual(gotoh('AGACTAGTTAC', 'TGACGSTGC', 5, 2,
                                      _sim_nw),
                                needleman_wunsch('AGACTAGTTAC', 'TGACGSTGC', 5,
                                                 _sim_nw))
        self.assertEqual(gotoh('AGACTAGTTAC', 'CGAGACGT', 5, 5, _sim_nw), -15)
        self.assertGreaterEqual(gotoh('AGACTAGTTAC', 'CGAGACGT', 5, 2, _sim_nw),
                                needleman_wunsch('AGACTAGTTAC', 'CGAGACGT', 5,
                                                 _sim_nw))

    def test_gotoh_nialls(self):
        """test abydos.distance.gotoh (Nialls set)
        """
        # checked against http://ds9a.nl/nwunsch/ (mismatch=1, gap=2, skew=2)
        nw_vals = (5, 0, -2, 3, 1, 1, -2, -2, -1, -3, -3, -5, -3, -7, -7, -19)
        for i in _range(len(NIALL)):
            self.assertEqual(gotoh(NIALL[0], NIALL[i], 2, 2, _sim_nw),
                             nw_vals[i])
        nw_vals2 = (5, 0, -2, 3, 1, 1, -2, -2, -1, -2, -3, -3, -2, -6, -6, -8)
        for i in _range(len(NIALL)):
            self.assertEqual(gotoh(NIALL[0], NIALL[i], 2, 1, _sim_nw),
                             nw_vals2[i])
            self.assertGreaterEqual(gotoh(NIALL[0], NIALL[i], 2, 0.5, _sim_nw),
                                    needleman_wunsch(NIALL[0], NIALL[i], 2,
                                                     _sim_nw))


class LengthTestCases(unittest.TestCase):
    """test cases for abydos.distance.sim_length &
    abydos.distance.dist_length
    """
    def test_sim_ident(self):
        """test abydos.distance.sim_length
        """
        self.assertEqual(sim_length('', ''), 1)
        self.assertEqual(sim_length('', 'a'), 0)
        self.assertEqual(sim_length('a', ''), 0)
        self.assertEqual(sim_length('a', 'a'), 1)
        self.assertEqual(sim_length('abcd', 'abcd'), 1)
        self.assertEqual(sim_length('abcd', 'dcba'), 1)
        self.assertEqual(sim_length('abc', 'cba'), 1)
        self.assertEqual(sim_length('abc', 'dcba'), 0.75)
        self.assertEqual(sim_length('abcd', 'cba'), 0.75)
        self.assertEqual(sim_length('ab', 'dcba'), 0.5)
        self.assertEqual(sim_length('abcd', 'ba'), 0.5)

    def test_dist_ident(self):
        """test abydos.distance.dist_length
        """
        self.assertEqual(dist_length('', ''), 0)
        self.assertEqual(dist_length('', 'a'), 1)
        self.assertEqual(dist_length('a', ''), 1)
        self.assertEqual(dist_length('a', 'a'), 0)
        self.assertEqual(dist_length('abcd', 'abcd'), 0)
        self.assertEqual(dist_length('abcd', 'dcba'), 0)
        self.assertEqual(dist_length('abc', 'cba'), 0)
        self.assertEqual(dist_length('abc', 'dcba'), 0.25)
        self.assertEqual(dist_length('abcd', 'cba'), 0.25)
        self.assertEqual(dist_length('ab', 'dcba'), 0.5)
        self.assertEqual(dist_length('abcd', 'ba'), 0.5)


class PrefixTestCases(unittest.TestCase):
    """test cases for abydos.distance.sim_prefix &
    abydos.distance.dist_prefix
    """
    def test_sim_prefix(self):
        """test abydos.distance.sim_prefix
        """
        self.assertEqual(sim_prefix('', ''), 1)
        self.assertEqual(sim_prefix('a', ''), 0)
        self.assertEqual(sim_prefix('', 'a'), 0)
        self.assertEqual(sim_prefix('a', 'a'), 1)
        self.assertEqual(sim_prefix('ax', 'a'), 1)
        self.assertEqual(sim_prefix('axx', 'a'), 1)
        self.assertEqual(sim_prefix('ax', 'ay'), 1/2)
        self.assertEqual(sim_prefix('a', 'ay'), 1)
        self.assertEqual(sim_prefix('a', 'ayy'), 1)
        self.assertEqual(sim_prefix('ax', 'ay'), 1/2)
        self.assertEqual(sim_prefix('a', 'y'), 0)
        self.assertEqual(sim_prefix('y', 'a'), 0)
        self.assertEqual(sim_prefix('aaax', 'aaa'), 1)
        self.assertAlmostEqual(sim_prefix('axxx', 'aaa'), 1/3)
        self.assertEqual(sim_prefix('aaxx', 'aayy'), 1/2)
        self.assertEqual(sim_prefix('xxaa', 'yyaa'), 0)
        self.assertAlmostEqual(sim_prefix('aaxxx', 'aay'), 2/3)
        self.assertEqual(sim_prefix('aaxxxx', 'aayyy'), 2/5)
        self.assertEqual(sim_prefix('xa', 'a'), 0)
        self.assertEqual(sim_prefix('xxa', 'a'), 0)
        self.assertEqual(sim_prefix('xa', 'ya'), 0)
        self.assertEqual(sim_prefix('a', 'ya'), 0)
        self.assertEqual(sim_prefix('a', 'yya'), 0)
        self.assertEqual(sim_prefix('xa', 'ya'), 0)
        self.assertEqual(sim_prefix('xaaa', 'aaa'), 0)
        self.assertEqual(sim_prefix('xxxa', 'aaa'), 0)
        self.assertEqual(sim_prefix('xxxaa', 'yaa'), 0)
        self.assertEqual(sim_prefix('xxxxaa', 'yyyaa'), 0)

    def test_dist_prefix(self):
        """test abydos.distance.dist_prefix
        """
        self.assertEqual(dist_prefix('', ''), 0)
        self.assertEqual(dist_prefix('a', ''), 1)
        self.assertEqual(dist_prefix('', 'a'), 1)
        self.assertEqual(dist_prefix('a', 'a'), 0)
        self.assertEqual(dist_prefix('ax', 'a'), 0)
        self.assertEqual(dist_prefix('axx', 'a'), 0)
        self.assertEqual(dist_prefix('ax', 'ay'), 1/2)
        self.assertEqual(dist_prefix('a', 'ay'), 0)
        self.assertEqual(dist_prefix('a', 'ayy'), 0)
        self.assertEqual(dist_prefix('ax', 'ay'), 1/2)
        self.assertEqual(dist_prefix('a', 'y'), 1)
        self.assertEqual(dist_prefix('y', 'a'), 1)
        self.assertEqual(dist_prefix('aaax', 'aaa'), 0)
        self.assertAlmostEqual(dist_prefix('axxx', 'aaa'), 2/3)
        self.assertEqual(dist_prefix('aaxx', 'aayy'), 1/2)
        self.assertEqual(dist_prefix('xxaa', 'yyaa'), 1)
        self.assertAlmostEqual(dist_prefix('aaxxx', 'aay'), 1/3)
        self.assertEqual(dist_prefix('aaxxxx', 'aayyy'), 3/5)
        self.assertEqual(dist_prefix('xa', 'a'), 1)
        self.assertEqual(dist_prefix('xxa', 'a'), 1)
        self.assertEqual(dist_prefix('xa', 'ya'), 1)
        self.assertEqual(dist_prefix('a', 'ya'), 1)
        self.assertEqual(dist_prefix('a', 'yya'), 1)
        self.assertEqual(dist_prefix('xa', 'ya'), 1)
        self.assertEqual(dist_prefix('xaaa', 'aaa'), 1)
        self.assertEqual(dist_prefix('xxxa', 'aaa'), 1)
        self.assertEqual(dist_prefix('xxxaa', 'yaa'), 1)
        self.assertEqual(dist_prefix('xxxxaa', 'yyyaa'), 1)


class SuffixTestCases(unittest.TestCase):
    """test cases for abydos.distance.sim_suffix &
    abydos.distance.dist_suffix
    """
    def test_sim_suffix(self):
        """test abydos.distance.sim_suffix
        """
        self.assertEqual(sim_suffix('', ''), 1)
        self.assertEqual(sim_suffix('a', ''), 0)
        self.assertEqual(sim_suffix('', 'a'), 0)
        self.assertEqual(sim_suffix('a', 'a'), 1)
        self.assertEqual(sim_suffix('ax', 'a'), 0)
        self.assertEqual(sim_suffix('axx', 'a'), 0)
        self.assertEqual(sim_suffix('ax', 'ay'), 0)
        self.assertEqual(sim_suffix('a', 'ay'), 0)
        self.assertEqual(sim_suffix('a', 'ayy'), 0)
        self.assertEqual(sim_suffix('ax', 'ay'), 0)
        self.assertEqual(sim_suffix('a', 'y'), 0)
        self.assertEqual(sim_suffix('y', 'a'), 0)
        self.assertEqual(sim_suffix('aaax', 'aaa'), 0)
        self.assertEqual(sim_suffix('axxx', 'aaa'), 0)
        self.assertEqual(sim_suffix('aaxx', 'aayy'), 0)
        self.assertEqual(sim_suffix('xxaa', 'yyaa'), 1/2)
        self.assertEqual(sim_suffix('aaxxx', 'aay'), 0)
        self.assertEqual(sim_suffix('aaxxxx', 'aayyy'), 0)
        self.assertEqual(sim_suffix('xa', 'a'), 1)
        self.assertEqual(sim_suffix('xxa', 'a'), 1)
        self.assertEqual(sim_suffix('xa', 'ya'), 1/2)
        self.assertEqual(sim_suffix('a', 'ya'), 1)
        self.assertEqual(sim_suffix('a', 'yya'), 1)
        self.assertEqual(sim_suffix('xa', 'ya'), 1/2)
        self.assertEqual(sim_suffix('xaaa', 'aaa'), 1)
        self.assertAlmostEqual(sim_suffix('xxxa', 'aaa'), 1/3)
        self.assertAlmostEqual(sim_suffix('xxxaa', 'yaa'), 2/3)
        self.assertEqual(sim_suffix('xxxxaa', 'yyyaa'), 2/5)

    def test_dist_suffix(self):
        """test abydos.distance.dist_suffix
        """
        self.assertEqual(dist_suffix('', ''), 0)
        self.assertEqual(dist_suffix('a', ''), 1)
        self.assertEqual(dist_suffix('', 'a'), 1)
        self.assertEqual(dist_suffix('a', 'a'), 0)
        self.assertEqual(dist_suffix('ax', 'a'), 1)
        self.assertEqual(dist_suffix('axx', 'a'), 1)
        self.assertEqual(dist_suffix('ax', 'ay'), 1)
        self.assertEqual(dist_suffix('a', 'ay'), 1)
        self.assertEqual(dist_suffix('a', 'ayy'), 1)
        self.assertEqual(dist_suffix('ax', 'ay'), 1)
        self.assertEqual(dist_suffix('a', 'y'), 1)
        self.assertEqual(dist_suffix('y', 'a'), 1)
        self.assertEqual(dist_suffix('aaax', 'aaa'), 1)
        self.assertEqual(dist_suffix('axxx', 'aaa'), 1)
        self.assertEqual(dist_suffix('aaxx', 'aayy'), 1)
        self.assertEqual(dist_suffix('xxaa', 'yyaa'), 1/2)
        self.assertEqual(dist_suffix('aaxxx', 'aay'), 1)
        self.assertEqual(dist_suffix('aaxxxx', 'aayyy'), 1)
        self.assertEqual(dist_suffix('xa', 'a'), 0)
        self.assertEqual(dist_suffix('xxa', 'a'), 0)
        self.assertEqual(dist_suffix('xa', 'ya'), 1/2)
        self.assertEqual(dist_suffix('a', 'ya'), 0)
        self.assertEqual(dist_suffix('a', 'yya'), 0)
        self.assertEqual(dist_suffix('xa', 'ya'), 1/2)
        self.assertEqual(dist_suffix('xaaa', 'aaa'), 0)
        self.assertAlmostEqual(dist_suffix('xxxa', 'aaa'), 2/3)
        self.assertAlmostEqual(dist_suffix('xxxaa', 'yaa'), 1/3)
        self.assertEqual(dist_suffix('xxxxaa', 'yyyaa'), 3/5)


class MLIPNSTestCases(unittest.TestCase):
    """test cases for abydos.distance.sim_mlipns &
    abydos.distance.dist_mlipns
    """
    def test_sim_mlipns(self):
        """test abydos.distance.sim_mlipns
        """
        self.assertEqual(sim_mlipns('', ''), 1)
        self.assertEqual(sim_mlipns('a', ''), 0)
        self.assertEqual(sim_mlipns('', 'a'), 0)
        self.assertEqual(sim_mlipns('a', 'a'), 1)
        self.assertEqual(sim_mlipns('ab', 'a'), 1)
        self.assertEqual(sim_mlipns('abc', 'abc'), 1)
        self.assertEqual(sim_mlipns('abc', 'abcde'), 1)
        self.assertEqual(sim_mlipns('abcg', 'abcdeg'), 1)
        self.assertEqual(sim_mlipns('abcg', 'abcdefg'), 0)
        self.assertEqual(sim_mlipns('Tomato', 'Tamato'), 1)

    def test_dist_mlipns(self):
        """test abydos.distance.dist_mlipns
        """
        self.assertEqual(dist_mlipns('', ''), 0)
        self.assertEqual(dist_mlipns('a', ''), 1)
        self.assertEqual(dist_mlipns('', 'a'), 1)
        self.assertEqual(dist_mlipns('a', 'a'), 0)
        self.assertEqual(dist_mlipns('ab', 'a'), 0)
        self.assertEqual(dist_mlipns('abc', 'abc'), 0)
        self.assertEqual(dist_mlipns('abc', 'abcde'), 0)
        self.assertEqual(dist_mlipns('abcg', 'abcdeg'), 0)
        self.assertEqual(dist_mlipns('abcg', 'abcdefg'), 1)
        self.assertEqual(dist_mlipns('Tomato', 'Tamato'), 0)


class BagTestCases(unittest.TestCase):
    """test cases for abydos.distance.bag, abydos.distance.sim_bag &
    abydos.distance.dist_bag
    """
    def test_bag(self):
        """test abydos.distance.sim_bag
        """
        self.assertEqual(bag('', ''), 0)
        self.assertEqual(bag('nelson', ''), 6)
        self.assertEqual(bag('', 'neilsen'), 7)
        self.assertEqual(bag('ab', 'a'), 1)
        self.assertEqual(bag('ab', 'c'), 2)
        self.assertAlmostEqual(bag('nelson', 'neilsen'), 2)
        self.assertAlmostEqual(bag('neilsen', 'nelson'), 2)
        self.assertAlmostEqual(bag('niall', 'neal'), 2)

    def test_sim_bag(self):
        """test abydos.distance.sim_bag
        """
        self.assertEqual(sim_bag('', ''), 1)
        self.assertEqual(sim_bag('nelson', ''), 0)
        self.assertEqual(sim_bag('', 'neilsen'), 0)
        self.assertEqual(sim_bag('ab', 'a'), 0.5)
        self.assertEqual(sim_bag('ab', 'c'), 0)
        self.assertAlmostEqual(sim_bag('nelson', 'neilsen'), 5/7)
        self.assertAlmostEqual(sim_bag('neilsen', 'nelson'), 5/7)
        self.assertAlmostEqual(sim_bag('niall', 'neal'), 3/5)

    def test_dist_bag(self):
        """test abydos.distance.dist_bag
        """
        self.assertEqual(dist_bag('', ''), 0)
        self.assertEqual(dist_bag('nelson', ''), 1)
        self.assertEqual(dist_bag('', 'neilsen'), 1)
        self.assertEqual(dist_bag('ab', 'a'), 0.5)
        self.assertEqual(dist_bag('ab', 'c'), 1)
        self.assertAlmostEqual(dist_bag('nelson', 'neilsen'), 2/7)
        self.assertAlmostEqual(dist_bag('neilsen', 'nelson'), 2/7)
        self.assertAlmostEqual(dist_bag('niall', 'neal'), 2/5)


class SimDistTestCases(unittest.TestCase):
    """test cases for abydos.distance.sim &
    abydos.distance.dist
    """
    def test_sim(self):
        """test abydos.distance.sim
        """
        self.assertEqual(sim('Niall', 'Nigel'),
                         sim_levenshtein('Niall', 'Nigel'))
        self.assertRaises(AttributeError, sim, 'abc', 'abc', 0)

    def test_dist(self):
        """test abydos.distance.dist
        """
        self.assertEqual(dist('Niall', 'Nigel'),
                         dist_levenshtein('Niall', 'Nigel'))
        self.assertRaises(AttributeError, dist, 'abc', 'abc', 0)


if __name__ == '__main__':
    unittest.main()
