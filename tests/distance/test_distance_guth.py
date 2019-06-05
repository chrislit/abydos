# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_guth.

This module contains unit tests for abydos.distance.Guth
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Guth


class GuthTestCases(unittest.TestCase):
    """Test Guth functions.

    abydos.distance.Guth
    """

    cmp = Guth()

    def test_guth_sim_score(self):
        """Test abydos.distance.Guth.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_score('a', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_score('abcd', 'efgh'), 0.0)

        # Tescases from paper
        self.assertEqual(self.cmp.sim_score('Glawyn', 'Glavin'), 1.0)
        self.assertEqual(self.cmp.sim_score('Smears', 'Smares'), 1.0)
        self.assertEqual(self.cmp.sim_score('Giddings', 'Gittins'), 1.0)
        self.assertEqual(self.cmp.sim_score('Bokenham', 'Buckingham'), 0.0)

    def test_guth_sim(self):
        """Test abydos.distance.Guth.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('a', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        # Tescases from paper
        self.assertEqual(self.cmp.sim('Glawyn', 'Glavin'), 0.0)
        self.assertEqual(self.cmp.sim('Smears', 'Smares'), 0.0)
        self.assertEqual(self.cmp.sim('Giddings', 'Gittins'), 0.0)
        self.assertEqual(self.cmp.sim('Bokenham', 'Buckingham'), 0.0)


if __name__ == '__main__':
    unittest.main()
