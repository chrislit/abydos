# -*- coding: utf-8 -*-

# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_lcsseq.

This module contains unit tests for abydos.distance.LCSseq
"""

import unittest

from abydos.distance import LCSseq, dist_lcsseq, lcsseq, sim_lcsseq


class LCSseqTestCases(unittest.TestCase):
    """Test LCSseq functions.

    abydos.distance.LCSseq
    """

    cmp = LCSseq()

    def test_lcsseq(self):
        """Test abydos.distance.LCSseq.lcsseq."""
        self.assertEqual(self.cmp.lcsseq('', ''), '')
        self.assertEqual(self.cmp.lcsseq('A', ''), '')
        self.assertEqual(self.cmp.lcsseq('', 'A'), '')
        self.assertEqual(self.cmp.lcsseq('A', 'A'), 'A')
        self.assertEqual(self.cmp.lcsseq('ABCD', ''), '')
        self.assertEqual(self.cmp.lcsseq('', 'ABCD'), '')
        self.assertEqual(self.cmp.lcsseq('ABCD', 'ABCD'), 'ABCD')
        self.assertEqual(self.cmp.lcsseq('ABCD', 'BC'), 'BC')
        self.assertEqual(self.cmp.lcsseq('ABCD', 'AD'), 'AD')
        self.assertEqual(self.cmp.lcsseq('ABCD', 'AC'), 'AC')
        self.assertEqual(self.cmp.lcsseq('AB', 'CD'), '')
        self.assertEqual(self.cmp.lcsseq('ABC', 'BCD'), 'BC')

        self.assertEqual(self.cmp.lcsseq('DIXON', 'DICKSONX'), 'DION')

        # https://en.wikipedia.org/wiki/Longest_common_subsequence_problem
        self.assertEqual(self.cmp.lcsseq('AGCAT', 'GAC'), 'AC')
        self.assertEqual(self.cmp.lcsseq('XMJYAUZ', 'MZJAWXU'), 'MJAU')

        # https://github.com/jwmerrill/factor/blob/master/basis/lcs/lcs-tests.factor
        self.assertEqual(self.cmp.lcsseq('hell', 'hello'), 'hell')
        self.assertEqual(self.cmp.lcsseq('hello', 'hell'), 'hell')
        self.assertEqual(self.cmp.lcsseq('ell', 'hell'), 'ell')
        self.assertEqual(self.cmp.lcsseq('hell', 'ell'), 'ell')
        self.assertEqual(self.cmp.lcsseq('faxbcd', 'abdef'), 'abd')

        # http://www.unesco.org/culture/languages-atlas/assets/_core/php/qcubed_unit_tests.php
        self.assertEqual(
            self.cmp.lcsseq('hello world', 'world war 2'), 'world'
        )
        self.assertEqual(self.cmp.lcsseq('foo bar', 'bar foo'), 'foo')
        self.assertEqual(self.cmp.lcsseq('aaa', 'aa'), 'aa')
        self.assertEqual(self.cmp.lcsseq('cc', 'bbbbcccccc'), 'cc')
        self.assertEqual(self.cmp.lcsseq('ccc', 'bcbb'), 'c')

        # Test wrapper
        self.assertEqual(lcsseq('ABC', 'BCD'), 'BC')

    def test_lcsseq_sim(self):
        """Test abydos.distance.LCSseq.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('A', ''), 0)
        self.assertEqual(self.cmp.sim('', 'A'), 0)
        self.assertEqual(self.cmp.sim('A', 'A'), 1)
        self.assertEqual(self.cmp.sim('ABCD', ''), 0)
        self.assertEqual(self.cmp.sim('', 'ABCD'), 0)
        self.assertEqual(self.cmp.sim('ABCD', 'ABCD'), 1)
        self.assertAlmostEqual(self.cmp.sim('ABCD', 'BC'), 2 / 4)
        self.assertAlmostEqual(self.cmp.sim('ABCD', 'AD'), 2 / 4)
        self.assertAlmostEqual(self.cmp.sim('ABCD', 'AC'), 2 / 4)
        self.assertAlmostEqual(self.cmp.sim('AB', 'CD'), 0)
        self.assertAlmostEqual(self.cmp.sim('ABC', 'BCD'), 2 / 3)

        self.assertAlmostEqual(self.cmp.sim('DIXON', 'DICKSONX'), 4 / 8)

        # https://en.wikipedia.org/wiki/Longest_common_subsequence_problem
        self.assertAlmostEqual(self.cmp.sim('AGCAT', 'GAC'), 2 / 5)
        self.assertAlmostEqual(self.cmp.sim('XMJYAUZ', 'MZJAWXU'), 4 / 7)

        # https://github.com/jwmerrill/factor/blob/master/basis/lcs/lcs-tests.factor
        self.assertAlmostEqual(self.cmp.sim('hell', 'hello'), 4 / 5)
        self.assertAlmostEqual(self.cmp.sim('hello', 'hell'), 4 / 5)
        self.assertAlmostEqual(self.cmp.sim('ell', 'hell'), 3 / 4)
        self.assertAlmostEqual(self.cmp.sim('hell', 'ell'), 3 / 4)
        self.assertAlmostEqual(self.cmp.sim('faxbcd', 'abdef'), 3 / 6)

        # http://www.unesco.org/culture/languages-atlas/assets/_core/php/qcubed_unit_tests.php
        self.assertAlmostEqual(
            self.cmp.sim('hello world', 'world war 2'), 5 / 11
        )
        self.assertAlmostEqual(self.cmp.sim('foo bar', 'bar foo'), 3 / 7)
        self.assertAlmostEqual(self.cmp.sim('aaa', 'aa'), 2 / 3)
        self.assertAlmostEqual(self.cmp.sim('cc', 'bbbbcccccc'), 2 / 10)
        self.assertAlmostEqual(self.cmp.sim('ccc', 'bcbb'), 1 / 4)

        # Test wrapper
        self.assertAlmostEqual(sim_lcsseq('ABC', 'BCD'), 2 / 3)

    def test_lcsseq_dist(self):
        """Test abydos.distance.LCSseq.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('A', ''), 1)
        self.assertEqual(self.cmp.dist('', 'A'), 1)
        self.assertEqual(self.cmp.dist('A', 'A'), 0)
        self.assertEqual(self.cmp.dist('ABCD', ''), 1)
        self.assertEqual(self.cmp.dist('', 'ABCD'), 1)
        self.assertEqual(self.cmp.dist('ABCD', 'ABCD'), 0)
        self.assertAlmostEqual(self.cmp.dist('ABCD', 'BC'), 2 / 4)
        self.assertAlmostEqual(self.cmp.dist('ABCD', 'AD'), 2 / 4)
        self.assertAlmostEqual(self.cmp.dist('ABCD', 'AC'), 2 / 4)
        self.assertAlmostEqual(self.cmp.dist('AB', 'CD'), 1)
        self.assertAlmostEqual(self.cmp.dist('ABC', 'BCD'), 1 / 3)

        self.assertAlmostEqual(self.cmp.dist('DIXON', 'DICKSONX'), 4 / 8)

        # https://en.wikipedia.org/wiki/Longest_common_subsequence_problem
        self.assertAlmostEqual(self.cmp.dist('AGCAT', 'GAC'), 3 / 5)
        self.assertAlmostEqual(self.cmp.dist('XMJYAUZ', 'MZJAWXU'), 3 / 7)

        # https://github.com/jwmerrill/factor/blob/master/basis/lcs/lcs-tests.factor
        self.assertAlmostEqual(self.cmp.dist('hell', 'hello'), 1 / 5)
        self.assertAlmostEqual(self.cmp.dist('hello', 'hell'), 1 / 5)
        self.assertAlmostEqual(self.cmp.dist('ell', 'hell'), 1 / 4)
        self.assertAlmostEqual(self.cmp.dist('hell', 'ell'), 1 / 4)
        self.assertAlmostEqual(self.cmp.dist('faxbcd', 'abdef'), 3 / 6)

        # http://www.unesco.org/culture/languages-atlas/assets/_core/php/qcubed_unit_tests.php
        self.assertAlmostEqual(
            self.cmp.dist('hello world', 'world war 2'), 6 / 11
        )
        self.assertAlmostEqual(self.cmp.dist('foo bar', 'bar foo'), 4 / 7)
        self.assertAlmostEqual(self.cmp.dist('aaa', 'aa'), 1 / 3)
        self.assertAlmostEqual(self.cmp.dist('cc', 'bbbbcccccc'), 8 / 10)
        self.assertAlmostEqual(self.cmp.dist('ccc', 'bcbb'), 3 / 4)

        # Test wrapper
        self.assertAlmostEqual(dist_lcsseq('ABC', 'BCD'), 1 / 3)


if __name__ == '__main__':
    unittest.main()
