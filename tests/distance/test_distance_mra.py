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

"""abydos.tests.test_distance.mra.

This module contains unit tests for abydos.distance.mra
"""

from __future__ import division, unicode_literals

import unittest

from abydos.distance.mra import dist_mra, mra_compare, sim_mra


class MraTestCases(unittest.TestCase):
    """Test MRA functions.

    abydos.distance.mra_compare, .sim_mra & .dist_mra
    """

    def test_mra_compare(self):
        """Test abydos.distance.mra_compare."""
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
        """Test abydos.distance.sim_mra."""
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
        """Test abydos.distance.dist_mra."""
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


if __name__ == '__main__':
    unittest.main()
