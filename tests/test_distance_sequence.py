# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
# This file is part of Abydos.
#
# Abydos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Abydos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Abydos. If not, see <http://www.gnu.org/licenses/>.

"""abydos.tests.test_distance.sequence.

This module contains unit tests for abydos.distance.sequence
"""

from __future__ import division, unicode_literals

import unittest
from difflib import SequenceMatcher

from abydos.distance.sequence import dist_lcsseq, dist_lcsstr, \
    dist_ratcliff_obershelp, lcsseq, lcsstr, sim_lcsseq, sim_lcsstr, \
    sim_ratcliff_obershelp

from . import TESTDIR


class LcsseqTestCases(unittest.TestCase):
    """Test LCSseq functions.

    abydos.distance.lcsseq, .sim_lcsseq, & .dist_lcsseq
    """

    def test_lcsseq(self):
        """Test abydos.distance.lcsseq."""
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
        """Test abydos.distance.sim_lcsseq."""
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
        """Test abydos.distance.dist_lcsseq."""
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
    """Test LCSstr functions.

    abydos.distance.lcsstr, .sim_lcsstr, & .dist_lcsstr
    """

    def test_lcsstr(self):
        """Test abydos.distance.lcsstr."""
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
        self.assertEqual(lcsstr('tsaxbaxyz', 'axcaxy'), 'axy')
        self.assertEqual(lcsstr('abcde', 'uvabxycde'), 'cde')
        self.assertEqual(lcsstr('abc', 'xyz'), '')
        self.assertEqual(lcsstr('TAAGGTCGGCGCGCACGCTGGCGAGTATGGTGCGGAGGCCCTGGA\
GAGGTGAGGCTCCCTCCCCTGCTCCGACCCGGGCTCCTCGCCCGCCCGGACCCAC', 'AAGCGCCGCGCAGTCTGGG\
CTCCGCACACTTCTGGTCCAGTCCGACTGAGAAGGAACCACCATGGTGCTGTCTCCCGCTGACAAGACCAACATCAAG\
ACTGCCTGGGAAAAGATCGGCAGCCACGGTGGCGAGTATGGCGCCGAGGCCGT'), 'TGGCGAGTATGG')

    def test_sim_lcsstr(self):
        """Test abydos.distance.sim_lcsstr."""
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
        """Test abydos.distance.dist_lcsstr."""
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
    """Test Ratcliff-Obserhelp functions.

    abydos.distance.sim_ratcliff_obershelp, &
    abydos.distance.dist_ratcliff_obershelp
    """

    def test_sim_ratcliff_obershelp(self):
        """Test abydos.distance.sim_ratcliff_obershelp."""
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

        with open(TESTDIR+'/corpora/variantNames.csv') as cav_testset:
            next(cav_testset)
            for line in cav_testset:
                line = line.strip().split(',')
                word1, word2 = line[0], line[4]
                self.assertAlmostEqual(sim_ratcliff_obershelp(word1, word2),
                                       SequenceMatcher(None, word1,
                                                       word2).ratio())

        with open(TESTDIR+'/corpora/wikipediaCommonMisspellings.csv') as missp:
            next(missp)
            for line in missp:
                line = line.strip().upper()
                line = ''.join([_ for _ in line.strip() if _ in
                                tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ,')])
                word1, word2 = line.split(',')
                # print(word1, word2e)
                self.assertAlmostEqual(sim_ratcliff_obershelp(word1, word2),
                                       SequenceMatcher(None, word1,
                                                       word2).ratio())

    def test_dist_ratcliff_obershelp(self):
        """Test abydos.distance.dist_ratcliff_obershelp."""
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
        self.assertAlmostEqual(dist_ratcliff_obershelp('abcefglmn',
                                                       'abefglmo'),
                               0.1764705882352941)
        self.assertAlmostEqual(dist_ratcliff_obershelp('abefglmo',
                                                       'abcefglmn'),
                               0.1764705882352941)


if __name__ == '__main__':
    unittest.main()
