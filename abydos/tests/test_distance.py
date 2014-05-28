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
from abydos.distance import levenshtein, levenshtein_normalized, hamming, \
    hamming_normalized, tversky_index, sorensen_coeff, sorensen, \
    jaccard_coeff, jaccard, tanimoto_coeff, tanimoto, cosine_similarity, \
    strcmp95, jaro_winkler, lcs, lcsr, lcsd, mra_compare, compression
import math


# pylint: disable=R0904
# pylint: disable=R0915
class LevenshteinTestCases(unittest.TestCase):
    """test cases for abydos.distance.levenshtein &
    abydos.distance.levenshtein_normalized
    """
    def test_levenshtein(self):
        """test abydos.distance.levenshtein
        """
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
        self.assertEquals(levenshtein('', 'b', 'lev', cost=(5, 7, 10, 10)), 5)
        self.assertEquals(levenshtein('', 'b', 'osa', cost=(5, 7, 10, 10)), 5)
        self.assertEquals(levenshtein('', 'b', 'dam', cost=(5, 7, 10, 10)), 5)
        self.assertEquals(levenshtein('a', 'ab', 'lev', cost=(5, 7, 10, 10)), 5)
        self.assertEquals(levenshtein('a', 'ab', 'osa', cost=(5, 7, 10, 10)), 5)
        self.assertEquals(levenshtein('a', 'ab', 'dam', cost=(5, 7, 10, 10)), 5)

        # test cost of delete
        self.assertEquals(levenshtein('b', '', 'lev', cost=(5, 7, 10, 10)), 7)
        self.assertEquals(levenshtein('b', '', 'osa', cost=(5, 7, 10, 10)), 7)
        self.assertEquals(levenshtein('b', '', 'dam', cost=(5, 7, 10, 10)), 7)
        self.assertEquals(levenshtein('ab', 'a', 'lev', cost=(5, 7, 10, 10)), 7)
        self.assertEquals(levenshtein('ab', 'a', 'osa', cost=(5, 7, 10, 10)), 7)
        self.assertEquals(levenshtein('ab', 'a', 'dam', cost=(5, 7, 10, 10)), 7)

        # test cost of substitute
        self.assertEquals(levenshtein('a', 'b', 'lev', cost=(10, 10, 5, 10)), 5)
        self.assertEquals(levenshtein('a', 'b', 'osa', cost=(10, 10, 5, 10)), 5)
        self.assertEquals(levenshtein('a', 'b', 'dam', cost=(10, 10, 5, 10)), 5)
        self.assertEquals(levenshtein('ac', 'bc', 'lev',
                                      cost=(10, 10, 5, 10)), 5)
        self.assertEquals(levenshtein('ac', 'bc', 'osa',
                                      cost=(10, 10, 5, 10)), 5)
        self.assertEquals(levenshtein('ac', 'bc', 'dam',
                                      cost=(10, 10, 5, 10)), 5)

        # test cost of transpose
        self.assertEquals(levenshtein('ab', 'ba', 'lev',
                                      cost=(10, 10, 10, 5)), 20)
        self.assertEquals(levenshtein('ab', 'ba', 'osa',
                                      cost=(10, 10, 10, 5)), 5)
        self.assertEquals(levenshtein('ab', 'ba', 'dam',
                                      cost=(5, 5, 10, 5)), 5)
        self.assertEquals(levenshtein('abc', 'bac', 'lev',
                                      cost=(10, 10, 10, 5)), 20)
        self.assertEquals(levenshtein('abc', 'bac', 'osa',
                                      cost=(10, 10, 10, 5)), 5)
        self.assertEquals(levenshtein('abc', 'bac', 'dam',
                                      cost=(5, 5, 10, 5)), 5)
        self.assertEquals(levenshtein('cab', 'cba', 'lev',
                                      cost=(10, 10, 10, 5)), 20)
        self.assertEquals(levenshtein('cab', 'cba', 'osa',
                                      cost=(10, 10, 10, 5)), 5)
        self.assertEquals(levenshtein('cab', 'cba', 'dam',
                                      cost=(5, 5, 10, 5)), 5)

        # test exception
        self.assertRaises(ValueError, levenshtein, 'ab', 'ba', 'dam',
                          cost=(10, 10, 10, 5))

    def test_levenshtein_normalized(self):
        """test abydos.distance.levenshtein_normalized
        """
        self.assertEquals(levenshtein_normalized('', ''), 0)

        self.assertEquals(levenshtein_normalized('a', 'a'), 0)
        self.assertEquals(levenshtein_normalized('ab', 'ab'), 0)
        self.assertEquals(levenshtein_normalized('', 'a'), 1)
        self.assertEquals(levenshtein_normalized('', 'ab'), 1)
        self.assertEquals(levenshtein_normalized('a', 'c'), 1)

        self.assertEquals(levenshtein_normalized('abc', 'ac'), 1/3)
        self.assertEquals(levenshtein_normalized('abbc', 'ac'), 1/2)
        self.assertEquals(levenshtein_normalized('abbc', 'abc'), 1/4)


class HammingTestCases(unittest.TestCase):
    """test cases for abydos.distance.hamming &
    abydos.distance.hamming_normalized
    """
    def test_hamming(self):
        """test abydos.distance.hamming
        """
        self.assertEquals(hamming('', ''), 0)
        self.assertEquals(hamming('', '', False), 0)

        self.assertEquals(hamming('a', ''), 1)
        self.assertEquals(hamming('a', 'a'), 0)
        self.assertEquals(hamming('a', 'a', False), 0)
        self.assertEquals(hamming('a', 'b'), 1)
        self.assertEquals(hamming('a', 'b', False), 1)
        self.assertEquals(hamming('abc', 'cba'), 2)
        self.assertEquals(hamming('abc', 'cba', False), 2)
        self.assertEquals(hamming('abc', ''), 3)
        self.assertEquals(hamming('bb', 'cbab'), 3)

        # test exception
        self.assertRaises(ValueError, hamming, 'ab', 'a', False)

        # https://en.wikipedia.org/wiki/Hamming_distance
        self.assertEquals(hamming('karolin', 'kathrin'), 3)
        self.assertEquals(hamming('karolin', 'kerstin'), 3)
        self.assertEquals(hamming('1011101', '1001001'), 2)
        self.assertEquals(hamming('2173896', '2233796'), 3)

    def test_hamming_normalized(self):
        """test abydos.distance.hamming_normalized
        """
        self.assertEquals(hamming_normalized('', ''), 0)
        self.assertEquals(hamming_normalized('', '', False), 0)

        self.assertEquals(hamming_normalized('a', ''), 1)
        self.assertEquals(hamming_normalized('a', 'a'), 0)
        self.assertEquals(hamming_normalized('a', 'a', False), 0)
        self.assertEquals(hamming_normalized('a', 'b'), 1)
        self.assertEquals(hamming_normalized('a', 'b', False), 1)
        self.assertEquals(hamming_normalized('abc', 'cba'), 2/3)
        self.assertEquals(hamming_normalized('abc', 'cba', False), 2/3)
        self.assertEquals(hamming_normalized('abc', ''), 1)
        self.assertEquals(hamming_normalized('bb', 'cbab'), 3/4)

        # test exception
        self.assertRaises(ValueError, hamming_normalized, 'ab', 'a', False)

        # https://en.wikipedia.org/wiki/Hamming_distance
        self.assertEquals(hamming_normalized('karolin', 'kathrin'), 3/7)
        self.assertEquals(hamming_normalized('karolin', 'kerstin'), 3/7)
        self.assertEquals(hamming_normalized('1011101', '1001001'), 2/7)
        self.assertEquals(hamming_normalized('2173896', '2233796'), 3/7)

class TverskyIndexTestCases(unittest.TestCase):
    """test cases for abydos.distance.tversky_index
    """
    def test_tversky_index(self):
        """test abydos.distance.tversky_index
        """
        self.assertEquals(tversky_index('', ''), 1)
        self.assertEquals(tversky_index('nelson', ''), 0)
        self.assertEquals(tversky_index('', 'neilsen'), 0)
        self.assertEquals(tversky_index('nelson', 'neilsen'), 4/11)
        # TODO: Add bias test(s) and unequal alpha & beta tests


class SorensenTestCases(unittest.TestCase):
    """test cases for abydos.distance.sorensen_coeff & abydos.distance.sorensen
    """
    def test_sorensen_coeff(self):
        """test abydos.distance.sorensen_coeff
        """
        self.assertEquals(sorensen_coeff('', ''), 1)
        self.assertEquals(sorensen_coeff('nelson', ''), 0)
        self.assertEquals(sorensen_coeff('', 'neilsen'), 0)
        self.assertEquals(sorensen_coeff('nelson', 'neilsen'), 4/7.5)

    def test_sorensen(self):
        """test abydos.distance.sorensen
        """
        self.assertEquals(sorensen('', ''), 0)
        self.assertEquals(sorensen('nelson', ''), 1)
        self.assertEquals(sorensen('', 'neilsen'), 1)
        self.assertEquals(sorensen('nelson', 'neilsen'), 3.5/7.5)


class JaccardTestCases(unittest.TestCase):
    """test cases for abydos.distance.jaccard_coeff & abydos.distance.jaccard
    """
    def test_jaccard_coeff(self):
        """test abydos.distance.jaccard_coeff
        """
        self.assertEquals(jaccard_coeff('', ''), 1)
        self.assertEquals(jaccard_coeff('nelson', ''), 0)
        self.assertEquals(jaccard_coeff('', 'neilsen'), 0)
        self.assertEquals(jaccard_coeff('nelson', 'neilsen'), 4/11)

    def test_jaccard(self):
        """test abydos.distance.jaccard
        """
        self.assertEquals(jaccard('', ''), 0)
        self.assertEquals(jaccard('nelson', ''), 1)
        self.assertEquals(jaccard('', 'neilsen'), 1)
        self.assertEquals(jaccard('nelson', 'neilsen'), 7/11)


class TanimotoTestCases(unittest.TestCase):
    """test cases for abydos.distance.tanimoto_coeff & abydos.distance.tanimoto
    """
    def test_tanimoto_coeff(self):
        """test abydos.distance.tanimoto_coeff
        """
        self.assertEquals(tanimoto_coeff('', ''), 1)
        self.assertEquals(tanimoto_coeff('nelson', ''), 0)
        self.assertEquals(tanimoto_coeff('', 'neilsen'), 0)
        self.assertEquals(tanimoto_coeff('nelson', 'neilsen'), 4/11)

    def test_tanimoto(self):
        """test abydos.distance.tanimoto
        """
        self.assertEquals(tanimoto('', ''), 0)
        self.assertEquals(tanimoto('nelson', ''), float('-inf'))
        self.assertEquals(tanimoto('', 'neilsen'), float('-inf'))
        self.assertEquals(tanimoto('nelson', 'neilsen'), math.log(4/11, 2))


class CosineSimilarityTestCases(unittest.TestCase):
    """test cases for abydos.distance.cosine_similarity
    """
    def test_cosine_similarity(self):
        """test abydos.distance.cosine_similarity
        """
        self.assertEquals(cosine_similarity('', ''), 1)
        self.assertEquals(cosine_similarity('nelson', ''), 0)
        self.assertEquals(cosine_similarity('', 'neilsen'), 0)
        self.assertEquals(cosine_similarity('nelson', 'neilsen'),
                          4/math.sqrt(15))


class JaroWinklerTestCases(unittest.TestCase):
    """test cases for abydos.distance.strcmp95 & abydos.distance.jaro_winkler
    """
    def test_strcmp95(self):
        """test abydos.distance.strcmp95
        """
        self.assertEquals(strcmp95('', ''), 1)
        self.assertEquals(strcmp95('MARTHA', ''), 0)
        self.assertEquals(strcmp95('', 'MARTHA'), 0)
        self.assertEquals(strcmp95('MARTHA', 'MARTHA'), 1)

        # TODO: find non-trivial strcmp95 tests or manufacture some

    def test_jaro_winkler(self):
        """test abydos.distance.jaro_winkler
        """
        self.assertEquals(jaro_winkler('', '', mode='jaro'), 1)
        self.assertEquals(jaro_winkler('', '', mode='winkler'), 1)
        self.assertEquals(jaro_winkler('MARTHA', '', mode='jaro'), 0)
        self.assertEquals(jaro_winkler('MARTHA', '', mode='winkler'), 0)
        self.assertEquals(jaro_winkler('', 'MARHTA', mode='jaro'), 0)
        self.assertEquals(jaro_winkler('', 'MARHTA', mode='winkler'), 0)
        self.assertEquals(jaro_winkler('MARTHA', 'MARTHA', mode='jaro'), 1)
        self.assertEquals(jaro_winkler('MARTHA', 'MARTHA', mode='winkler'), 1)

        # https://en.wikipedia.org/wiki/Jaro-Winkler_distance
        self.assertEquals(round(jaro_winkler('MARTHA', 'MARHTA',
                                             mode='jaro'), 3), 0.944)
        self.assertEquals(round(jaro_winkler('MARTHA', 'MARHTA',
                                             mode='winkler'), 3), 0.961)
        self.assertEquals(round(jaro_winkler('DWAYNE', 'DUANE',
                                             mode='jaro'), 3), 0.822)
        self.assertEquals(round(jaro_winkler('DWAYNE', 'DUANE',
                                             mode='winkler'), 3), 0.84)
        self.assertEquals(round(jaro_winkler('DIXON', 'DICKSONX',
                                             mode='jaro'), 3), 0.767)
        self.assertEquals(round(jaro_winkler('DIXON', 'DICKSONX',
                                             mode='winkler'), 3), 0.813)


class LcsTestCases(unittest.TestCase):
    """test cases for abydos.distance.lcs
    """
    def test_lcs(self):
        """test abydos.distance.lcs
        """
        self.assertEquals(lcs('', ''), '')
        self.assertEquals(lcs('A', ''), '')
        self.assertEquals(lcs('', 'A'), '')
        self.assertEquals(lcs('A', 'A'), 'A')
        self.assertEquals(lcs('ABCD', ''), '')
        self.assertEquals(lcs('', 'ABCD'), '')
        self.assertEquals(lcs('ABCD', 'ABCD'), 'ABCD')
        self.assertEquals(lcs('ABCD', 'BC'), 'BC')
        self.assertEquals(lcs('ABCD', 'AD'), 'AD')
        self.assertEquals(lcs('ABCD', 'AC'), 'AC')
        self.assertEquals(lcs('AB', 'CD'), '')
        self.assertEquals(lcs('ABC', 'BCD'), 'BC')

        self.assertEquals(lcs('DIXON', 'DICKSONX'), 'DION')

        # https://en.wikipedia.org/wiki/Longest_common_subsequence_problem
        self.assertEquals(lcs('AGCAT', 'GAC'), 'AC')
        self.assertEquals(lcs('XMJYAUZ', 'MZJAWXU'), 'MJAU')

        # https://github.com/jwmerrill/factor/blob/master/basis/lcs/lcs-tests.factor
        self.assertEquals(lcs('hell', 'hello'), 'hell')
        self.assertEquals(lcs('hello', 'hell'), 'hell')
        self.assertEquals(lcs('ell', 'hell'), 'ell')
        self.assertEquals(lcs('hell', 'ell'), 'ell')
        self.assertEquals(lcs('faxbcd', 'abdef'), 'abd')

        # http://www.unesco.org/culture/languages-atlas/assets/_core/php/qcubed_unit_tests.php
        self.assertEquals(lcs('hello world', 'world war 2'), 'world')
        self.assertEquals(lcs('foo bar', 'bar foo'), 'foo')
        self.assertEquals(lcs('aaa', 'aa'), 'aa')
        self.assertEquals(lcs('cc', 'bbbbcccccc'), 'cc')
        self.assertEquals(lcs('ccc', 'bcbb'), 'c')

    def test_lcsr(self):
        """test abydos.distance.lcsr
        """
        self.assertEquals(lcsr('', ''), 1)
        self.assertEquals(lcsr('A', ''), 0)
        self.assertEquals(lcsr('', 'A'), 0)
        self.assertEquals(lcsr('A', 'A'), 1)
        self.assertEquals(lcsr('ABCD', ''), 0)
        self.assertEquals(lcsr('', 'ABCD'), 0)
        self.assertEquals(lcsr('ABCD', 'ABCD'), 1)
        self.assertEquals(lcsr('ABCD', 'BC'), 2/4)
        self.assertEquals(lcsr('ABCD', 'AD'), 2/4)
        self.assertEquals(lcsr('ABCD', 'AC'), 2/4)
        self.assertEquals(lcsr('AB', 'CD'), 0)
        self.assertEquals(lcsr('ABC', 'BCD'), 2/3)

        self.assertEquals(lcsr('DIXON', 'DICKSONX'), 4/8)

        # https://en.wikipedia.org/wiki/Longest_common_subsequence_problem
        self.assertEquals(lcsr('AGCAT', 'GAC'), 2/5)
        self.assertEquals(lcsr('XMJYAUZ', 'MZJAWXU'), 4/7)

        # https://github.com/jwmerrill/factor/blob/master/basis/lcs/lcs-tests.factor
        self.assertEquals(lcsr('hell', 'hello'), 4/5)
        self.assertEquals(lcsr('hello', 'hell'), 4/5)
        self.assertEquals(lcsr('ell', 'hell'), 3/4)
        self.assertEquals(lcsr('hell', 'ell'), 3/4)
        self.assertEquals(lcsr('faxbcd', 'abdef'), 3/6)

        # http://www.unesco.org/culture/languages-atlas/assets/_core/php/qcubed_unit_tests.php
        self.assertEquals(lcsr('hello world', 'world war 2'), 5/11)
        self.assertEquals(lcsr('foo bar', 'bar foo'), 3/7)
        self.assertEquals(lcsr('aaa', 'aa'), 2/3)
        self.assertEquals(lcsr('cc', 'bbbbcccccc'), 2/10)
        self.assertEquals(lcsr('ccc', 'bcbb'), 1/4)

    def test_lcsd(self):
        """test abydos.distance.lcsd
        """
        self.assertEquals(lcsd('', ''), 0)
        self.assertEquals(lcsd('A', ''), 1)
        self.assertEquals(lcsd('', 'A'), 1)
        self.assertEquals(lcsd('A', 'A'), 0)
        self.assertEquals(lcsd('ABCD', ''), 1)
        self.assertEquals(lcsd('', 'ABCD'), 1)
        self.assertEquals(lcsd('ABCD', 'ABCD'), 0)
        self.assertEquals(lcsd('ABCD', 'BC'), 2/4)
        self.assertEquals(lcsd('ABCD', 'AD'), 2/4)
        self.assertEquals(lcsd('ABCD', 'AC'), 2/4)
        self.assertEquals(lcsd('AB', 'CD'), 1)
        self.assertEquals(lcsd('ABC', 'BCD'), 1/3)

        self.assertEquals(lcsd('DIXON', 'DICKSONX'), 4/8)

        # https://en.wikipedia.org/wiki/Longest_common_subsequence_problem
        self.assertEquals(lcsd('AGCAT', 'GAC'), 3/5)
        self.assertEquals(lcsd('XMJYAUZ', 'MZJAWXU'), 3/7)

        # https://github.com/jwmerrill/factor/blob/master/basis/lcs/lcs-tests.factor
        self.assertEquals(lcsd('hell', 'hello'), 1/5)
        self.assertEquals(lcsd('hello', 'hell'), 1/5)
        self.assertEquals(lcsd('ell', 'hell'), 1/4)
        self.assertEquals(lcsd('hell', 'ell'), 1/4)
        self.assertEquals(lcsd('faxbcd', 'abdef'), 3/6)

        # http://www.unesco.org/culture/languages-atlas/assets/_core/php/qcubed_unit_tests.php
        self.assertEquals(lcsd('hello world', 'world war 2'), 6/11)
        self.assertEquals(lcsd('foo bar', 'bar foo'), 4/7)
        self.assertEquals(lcsd('aaa', 'aa'), 1/3)
        self.assertEquals(lcsd('cc', 'bbbbcccccc'), 8/10)
        self.assertEquals(lcsd('ccc', 'bcbb'), 3/4)


class MraCompareTestCases(unittest.TestCase):
    """test cases for abydos.distance.mra_compare
    """
    def test_mra_compare(self):
        """test abydos.distance.mra_compare
        """
        self.assertEquals(mra_compare('', ''), 6)
        self.assertEquals(mra_compare('a', 'a'), 6)
        self.assertEquals(mra_compare('abcdefg', 'abcdefg'), 6)
        self.assertEquals(mra_compare('abcdefg', ''), 0)
        self.assertEquals(mra_compare('', 'abcdefg'), 0)

        # https://en.wikipedia.org/wiki/Match_rating_approach
        self.assertEquals(mra_compare('Byrne', 'Boern'), 5)
        self.assertEquals(mra_compare('Smith', 'Smyth'), 5)
        self.assertEquals(mra_compare('Catherine', 'Kathryn'), 4)

class CompressionTestCases(unittest.TestCase):
    """test cases for abydos.distance.compression
    """
    def test_compression(self):
        """test abydos.distance.comporession
        """
        self.assertEquals(compression('', ''), 0)
        self.assertEquals(compression('', '', 'bzip2'), 0)
        self.assertEquals(compression('', '', 'lzma'), 0)
        self.assertEquals(compression('', '', 'zlib'), 0)

        self.assertGreater(compression('a', ''), 0)
        self.assertGreater(compression('a', '', 'bzip2'), 0)
        self.assertGreater(compression('a', '', 'lzma'), 0)
        self.assertGreater(compression('a', '', 'zlib'), 0)

        self.assertGreater(compression('abcdefg', 'fg'), 0)
        self.assertGreater(compression('abcdefg', 'fg', 'bzip2'), 0)
        self.assertGreater(compression('abcdefg', 'fg', 'lzma'), 0)
        self.assertGreater(compression('abcdefg', 'fg', 'zlib'), 0)
