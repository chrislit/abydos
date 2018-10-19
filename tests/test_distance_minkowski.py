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

"""abydos.tests.test_distance.minkowski.

This module contains unit tests for abydos.distance.minkowski
"""

from __future__ import division, unicode_literals

import unittest

from abydos.distance.minkowski import chebyshev, dist_euclidean, \
    dist_manhattan, dist_minkowski, euclidean, manhattan, minkowski, \
    sim_euclidean, sim_manhattan, sim_minkowski
from abydos.tokenizer.qgram import QGrams

from test_distance import NONQ_FROM, NONQ_TO


class MinkowskiTestCases(unittest.TestCase):
    """Test Minkowski functions.

    abydos.distance.minkowski, sim_minkowski & .dist_minkowski
    """

    def test_minkowski(self):
        """Test abydos.distance.minkowski."""
        self.assertEqual(minkowski('', ''), 0)
        self.assertEqual(minkowski('nelson', ''), 7)
        self.assertEqual(minkowski('', 'neilsen'), 8)
        self.assertAlmostEqual(minkowski('nelson', 'neilsen'), 7)

        self.assertEqual(minkowski('', '', 2), 0)
        self.assertEqual(minkowski('nelson', '', 2), 7)
        self.assertEqual(minkowski('', 'neilsen', 2), 8)
        self.assertAlmostEqual(minkowski('nelson', 'neilsen', 2), 7)

        # supplied q-gram tests
        self.assertEqual(minkowski(QGrams(''), QGrams('')), 0)
        self.assertEqual(minkowski(QGrams('nelson'), QGrams('')), 7)
        self.assertEqual(minkowski(QGrams(''), QGrams('neilsen')), 8)
        self.assertAlmostEqual(minkowski(QGrams('nelson'),
                                         QGrams('neilsen')), 7)

        # non-q-gram tests
        self.assertEqual(minkowski('', '', 0), 0)
        self.assertEqual(minkowski('the quick', '', 0), 2)
        self.assertEqual(minkowski('', 'the quick', 0), 2)
        self.assertAlmostEqual(minkowski(NONQ_FROM, NONQ_TO, 0), 8)
        self.assertAlmostEqual(minkowski(NONQ_TO, NONQ_FROM, 0), 8)

        # test l_0 "norm"
        self.assertEqual(minkowski('', '', 1, 0), 0)
        self.assertEqual(minkowski('a', '', 1, 0), 1)
        self.assertEqual(minkowski('a', 'b', 1, 0), 2)
        self.assertEqual(minkowski('ab', 'b', 1, 0), 1)
        self.assertEqual(minkowski('aab', 'b', 1, 0), 1)
        self.assertEqual(minkowski('', '', 1, 0, True), 0)
        self.assertEqual(minkowski('a', '', 1, 0, True), 1)
        self.assertEqual(minkowski('a', 'b', 1, 0, True), 1)
        self.assertEqual(minkowski('ab', 'b', 1, 0, True), 1/2)
        self.assertEqual(minkowski('aab', 'b', 1, 0, True), 1/2)
        self.assertEqual(minkowski('aaab', 'b', 1, 0, True), 1/2)
        self.assertEqual(minkowski('aaab', 'ab', 1, 0, True), 1/2)

        # test with alphabet
        self.assertEqual(minkowski('ab', 'b', 1, alphabet=26), 1)
        self.assertEqual(minkowski('ab', 'b', 1, normalized=True, alphabet=26),
                         1/26)
        self.assertEqual(minkowski('ab', 'b', 1, normalized=True,
                                   alphabet='abcdefghijklmnopqrstuvwxyz'),
                         1/26)

    def test_sim_minkowski(self):
        """Test abydos.distance.sim_minkowski."""
        self.assertEqual(sim_minkowski('', ''), 1)
        self.assertEqual(sim_minkowski('nelson', ''), 0)
        self.assertEqual(sim_minkowski('', 'neilsen'), 0)
        self.assertAlmostEqual(sim_minkowski('nelson', 'neilsen'), 8/15)

        self.assertEqual(sim_minkowski('', '', 2), 1)
        self.assertEqual(sim_minkowski('nelson', '', 2), 0)
        self.assertEqual(sim_minkowski('', 'neilsen', 2), 0)
        self.assertAlmostEqual(sim_minkowski('nelson', 'neilsen', 2), 8/15)

        # supplied q-gram tests
        self.assertEqual(sim_minkowski(QGrams(''), QGrams('')), 1)
        self.assertEqual(sim_minkowski(QGrams('nelson'), QGrams('')), 0)
        self.assertEqual(sim_minkowski(QGrams(''), QGrams('neilsen')), 0)
        self.assertAlmostEqual(sim_minkowski(QGrams('nelson'),
                                             QGrams('neilsen')), 8/15)

        # non-q-gram tests
        self.assertEqual(sim_minkowski('', '', 0), 1)
        self.assertEqual(sim_minkowski('the quick', '', 0), 0)
        self.assertEqual(sim_minkowski('', 'the quick', 0), 0)
        self.assertAlmostEqual(sim_minkowski(NONQ_FROM, NONQ_TO, 0), 1/2)
        self.assertAlmostEqual(sim_minkowski(NONQ_TO, NONQ_FROM, 0), 1/2)

    def test_dist_minkowski(self):
        """Test abydos.distance.dist_minkowski."""
        self.assertEqual(dist_minkowski('', ''), 0)
        self.assertEqual(dist_minkowski('nelson', ''), 1)
        self.assertEqual(dist_minkowski('', 'neilsen'), 1)
        self.assertAlmostEqual(dist_minkowski('nelson', 'neilsen'), 7/15)

        self.assertEqual(dist_minkowski('', '', 2), 0)
        self.assertEqual(dist_minkowski('nelson', '', 2), 1)
        self.assertEqual(dist_minkowski('', 'neilsen', 2), 1)
        self.assertAlmostEqual(dist_minkowski('nelson', 'neilsen', 2), 7/15)

        # supplied q-gram tests
        self.assertEqual(dist_minkowski(QGrams(''), QGrams('')), 0)
        self.assertEqual(dist_minkowski(QGrams('nelson'), QGrams('')), 1)
        self.assertEqual(dist_minkowski(QGrams(''), QGrams('neilsen')), 1)
        self.assertAlmostEqual(dist_minkowski(QGrams('nelson'),
                                              QGrams('neilsen')), 7/15)

        # non-q-gram tests
        self.assertEqual(dist_minkowski('', '', 0), 0)
        self.assertEqual(dist_minkowski('the quick', '', 0), 1)
        self.assertEqual(dist_minkowski('', 'the quick', 0), 1)
        self.assertAlmostEqual(dist_minkowski(NONQ_FROM, NONQ_TO, 0), 1/2)
        self.assertAlmostEqual(dist_minkowski(NONQ_TO, NONQ_FROM, 0), 1/2)


class ManhattanTestCases(unittest.TestCase):
    """Test Manhattan functions.

    abydos.distance.manhattan, sim_manhattan & .dist_manhattan
    """

    def test_manhattan(self):
        """Test abydos.distance.manhattan."""
        self.assertEqual(manhattan('', ''), 0)
        self.assertEqual(manhattan('nelson', ''), 7)
        self.assertEqual(manhattan('', 'neilsen'), 8)
        self.assertAlmostEqual(manhattan('nelson', 'neilsen'), 7)

        self.assertEqual(manhattan('', '', 2), 0)
        self.assertEqual(manhattan('nelson', '', 2), 7)
        self.assertEqual(manhattan('', 'neilsen', 2), 8)
        self.assertAlmostEqual(manhattan('nelson', 'neilsen', 2), 7)

        # supplied q-gram tests
        self.assertEqual(manhattan(QGrams(''), QGrams('')), 0)
        self.assertEqual(manhattan(QGrams('nelson'), QGrams('')), 7)
        self.assertEqual(manhattan(QGrams(''), QGrams('neilsen')), 8)
        self.assertAlmostEqual(manhattan(QGrams('nelson'),
                                         QGrams('neilsen')), 7)

        # non-q-gram tests
        self.assertEqual(manhattan('', '', 0), 0)
        self.assertEqual(manhattan('the quick', '', 0), 2)
        self.assertEqual(manhattan('', 'the quick', 0), 2)
        self.assertAlmostEqual(manhattan(NONQ_FROM, NONQ_TO, 0), 8)
        self.assertAlmostEqual(manhattan(NONQ_TO, NONQ_FROM, 0), 8)

    def test_sim_manhattan(self):
        """Test abydos.distance.sim_manhattan."""
        self.assertEqual(sim_manhattan('', ''), 1)
        self.assertEqual(sim_manhattan('nelson', ''), 0)
        self.assertEqual(sim_manhattan('', 'neilsen'), 0)
        self.assertAlmostEqual(sim_manhattan('nelson', 'neilsen'), 8/15)

        self.assertEqual(sim_manhattan('', '', 2), 1)
        self.assertEqual(sim_manhattan('nelson', '', 2), 0)
        self.assertEqual(sim_manhattan('', 'neilsen', 2), 0)
        self.assertAlmostEqual(sim_manhattan('nelson', 'neilsen', 2), 8/15)

        # supplied q-gram tests
        self.assertEqual(sim_manhattan(QGrams(''), QGrams('')), 1)
        self.assertEqual(sim_manhattan(QGrams('nelson'), QGrams('')), 0)
        self.assertEqual(sim_manhattan(QGrams(''), QGrams('neilsen')), 0)
        self.assertAlmostEqual(sim_manhattan(QGrams('nelson'),
                                             QGrams('neilsen')), 8/15)

        # non-q-gram tests
        self.assertEqual(sim_manhattan('', '', 0), 1)
        self.assertEqual(sim_manhattan('the quick', '', 0), 0)
        self.assertEqual(sim_manhattan('', 'the quick', 0), 0)
        self.assertAlmostEqual(sim_manhattan(NONQ_FROM, NONQ_TO, 0), 1/2)
        self.assertAlmostEqual(sim_manhattan(NONQ_TO, NONQ_FROM, 0), 1/2)

    def test_dist_manhattan(self):
        """Test abydos.distance.dist_manhattan."""
        self.assertEqual(dist_manhattan('', ''), 0)
        self.assertEqual(dist_manhattan('nelson', ''), 1)
        self.assertEqual(dist_manhattan('', 'neilsen'), 1)
        self.assertAlmostEqual(dist_manhattan('nelson', 'neilsen'), 7/15)

        self.assertEqual(dist_manhattan('', '', 2), 0)
        self.assertEqual(dist_manhattan('nelson', '', 2), 1)
        self.assertEqual(dist_manhattan('', 'neilsen', 2), 1)
        self.assertAlmostEqual(dist_manhattan('nelson', 'neilsen', 2), 7/15)

        # supplied q-gram tests
        self.assertEqual(dist_manhattan(QGrams(''), QGrams('')), 0)
        self.assertEqual(dist_manhattan(QGrams('nelson'), QGrams('')), 1)
        self.assertEqual(dist_manhattan(QGrams(''), QGrams('neilsen')), 1)
        self.assertAlmostEqual(dist_manhattan(QGrams('nelson'),
                                              QGrams('neilsen')), 7/15)

        # non-q-gram tests
        self.assertEqual(dist_manhattan('', '', 0), 0)
        self.assertEqual(dist_manhattan('the quick', '', 0), 1)
        self.assertEqual(dist_manhattan('', 'the quick', 0), 1)
        self.assertAlmostEqual(dist_manhattan(NONQ_FROM, NONQ_TO, 0), 1/2)
        self.assertAlmostEqual(dist_manhattan(NONQ_TO, NONQ_FROM, 0), 1/2)


class EuclideanTestCases(unittest.TestCase):
    """Test Euclidean functions.

    abydos.distance.euclidean, sim_euclidean & .dist_euclidean
    """

    def test_euclidean(self):
        """Test abydos.distance.euclidean."""
        self.assertEqual(euclidean('', ''), 0)
        self.assertEqual(euclidean('nelson', ''), 7**0.5)
        self.assertEqual(euclidean('', 'neilsen'), 8**0.5)
        self.assertAlmostEqual(euclidean('nelson', 'neilsen'), 7**0.5)

        self.assertEqual(euclidean('', '', 2), 0)
        self.assertEqual(euclidean('nelson', '', 2), 7**0.5)
        self.assertEqual(euclidean('', 'neilsen', 2), 8**0.5)
        self.assertAlmostEqual(euclidean('nelson', 'neilsen', 2), 7**0.5)

        # supplied q-gram tests
        self.assertEqual(euclidean(QGrams(''), QGrams('')), 0)
        self.assertEqual(euclidean(QGrams('nelson'), QGrams('')), 7**0.5)
        self.assertEqual(euclidean(QGrams(''), QGrams('neilsen')), 8**0.5)
        self.assertAlmostEqual(euclidean(QGrams('nelson'),
                                         QGrams('neilsen')), 7**0.5)

        # non-q-gram tests
        self.assertEqual(euclidean('', '', 0), 0)
        self.assertEqual(euclidean('the quick', '', 0), 2**0.5)
        self.assertEqual(euclidean('', 'the quick', 0), 2**0.5)
        self.assertAlmostEqual(euclidean(NONQ_FROM, NONQ_TO, 0), 8**0.5)
        self.assertAlmostEqual(euclidean(NONQ_TO, NONQ_FROM, 0), 8**0.5)

    def test_sim_euclidean(self):
        """Test abydos.distance.sim_euclidean."""
        self.assertEqual(sim_euclidean('', ''), 1)
        self.assertEqual(sim_euclidean('nelson', ''), 0)
        self.assertEqual(sim_euclidean('', 'neilsen'), 0)
        self.assertAlmostEqual(sim_euclidean('nelson', 'neilsen'),
                               1-7**0.5/23**0.5)

        self.assertEqual(sim_euclidean('', '', 2), 1)
        self.assertEqual(sim_euclidean('nelson', '', 2), 0)
        self.assertEqual(sim_euclidean('', 'neilsen', 2), 0)
        self.assertAlmostEqual(sim_euclidean('nelson', 'neilsen', 2),
                               1-7**0.5/23**0.5)

        # supplied q-gram tests
        self.assertEqual(sim_euclidean(QGrams(''), QGrams('')), 1)
        self.assertEqual(sim_euclidean(QGrams('nelson'), QGrams('')), 0)
        self.assertEqual(sim_euclidean(QGrams(''), QGrams('neilsen')), 0)
        self.assertAlmostEqual(sim_euclidean(QGrams('nelson'),
                                             QGrams('neilsen')),
                               1-7**0.5/23**0.5)

        # non-q-gram tests
        self.assertEqual(sim_euclidean('', '', 0), 1)
        self.assertEqual(sim_euclidean('the quick', '', 0), 0)
        self.assertEqual(sim_euclidean('', 'the quick', 0), 0)
        self.assertAlmostEqual(sim_euclidean(NONQ_FROM, NONQ_TO, 0),
                               1-8**0.5/24**0.5)
        self.assertAlmostEqual(sim_euclidean(NONQ_TO, NONQ_FROM, 0),
                               1-8**0.5/24**0.5)

    def test_dist_euclidean(self):
        """Test abydos.distance.dist_euclidean."""
        self.assertEqual(dist_euclidean('', ''), 0)
        self.assertEqual(dist_euclidean('nelson', ''), 1)
        self.assertEqual(dist_euclidean('', 'neilsen'), 1)
        self.assertAlmostEqual(dist_euclidean('nelson', 'neilsen'),
                               7**0.5 / 23**0.5)

        self.assertEqual(dist_euclidean('', '', 2), 0)
        self.assertEqual(dist_euclidean('nelson', '', 2), 1)
        self.assertEqual(dist_euclidean('', 'neilsen', 2), 1)
        self.assertAlmostEqual(dist_euclidean('nelson', 'neilsen', 2),
                               7**0.5 / 23**0.5)

        # supplied q-gram tests
        self.assertEqual(dist_euclidean(QGrams(''), QGrams('')), 0)
        self.assertEqual(dist_euclidean(QGrams('nelson'), QGrams('')), 1)
        self.assertEqual(dist_euclidean(QGrams(''), QGrams('neilsen')), 1)
        self.assertAlmostEqual(dist_euclidean(QGrams('nelson'),
                                              QGrams('neilsen')),
                               7**0.5 / 23**0.5)

        # non-q-gram tests
        self.assertEqual(dist_euclidean('', '', 0), 0)
        self.assertEqual(dist_euclidean('the quick', '', 0), 1)
        self.assertEqual(dist_euclidean('', 'the quick', 0), 1)
        self.assertAlmostEqual(dist_euclidean(NONQ_FROM, NONQ_TO, 0),
                               8**0.5/24**0.5)
        self.assertAlmostEqual(dist_euclidean(NONQ_TO, NONQ_FROM, 0),
                               8**0.5/24**0.5)


class ChebyshevTestCases(unittest.TestCase):
    """Test Chebyshev functions.

    abydos.distance.chebyshev, sim_chebyshev & .dist_chebyshev
    """

    def test_chebyshev(self):
        """Test abydos.distance.chebyshev."""
        self.assertEqual(chebyshev('', ''), 0)
        self.assertEqual(chebyshev('nelson', ''), 1)
        self.assertEqual(chebyshev('', 'neilsen'), 1)
        self.assertEqual(chebyshev('nelson', 'neilsen'), 1)

        self.assertEqual(chebyshev('', '', 2), 0)
        self.assertEqual(chebyshev('nelson', '', 2), 1)
        self.assertEqual(chebyshev('', 'neilsen', 2), 1)
        self.assertAlmostEqual(chebyshev('nelson', 'neilsen', 2), 1)

        # supplied q-gram tests
        self.assertEqual(chebyshev(QGrams(''), QGrams('')), 0)
        self.assertEqual(chebyshev(QGrams('nelson'), QGrams('')), 1)
        self.assertEqual(chebyshev(QGrams(''), QGrams('neilsen')), 1)
        self.assertAlmostEqual(chebyshev(QGrams('nelson'),
                                         QGrams('neilsen')), 1)

        # non-q-gram tests
        self.assertEqual(chebyshev('', '', 0), 0)
        self.assertEqual(chebyshev('the quick', '', 0), 1)
        self.assertEqual(chebyshev('', 'the quick', 0), 1)
        self.assertAlmostEqual(chebyshev(NONQ_FROM, NONQ_TO, 0), 1)
        self.assertAlmostEqual(chebyshev(NONQ_TO, NONQ_FROM, 0), 1)


if __name__ == '__main__':
    unittest.main()
