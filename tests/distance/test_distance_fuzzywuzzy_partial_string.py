# -*- coding: utf-8 -*-

# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_fuzzywuzzy_partial_string.

This module contains unit tests for abydos.distance.FuzzyWuzzyPartialString
"""

import unittest

from abydos.distance import FuzzyWuzzyPartialString


class FuzzyWuzzyPartialStringTestCases(unittest.TestCase):
    """Test FuzzyWuzzyPartialString functions.

    abydos.distance.FuzzyWuzzyPartialString
    """

    cmp = FuzzyWuzzyPartialString()

    def test_fuzzywuzzy_partial_string_sim(self):
        """Test abydos.distance.FuzzyWuzzyPartialString.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 1.0)
        self.assertEqual(self.cmp.sim('', 'a'), 1.0)
        self.assertEqual(self.cmp.sim('abc', ''), 1.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.6)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.6)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.8)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.8)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.6666666667
        )

        # tests from blog
        self.assertAlmostEqual(
            self.cmp.sim('YANKEES', 'NEW YORK YANKEES'), 1.0
        )
        self.assertAlmostEqual(
            self.cmp.sim('NEW YORK METS', 'NEW YORK YANKEES'),
            0.6923076923076923,
        )
        self.assertAlmostEqual(
            self.cmp.sim(
                'New York Mets vs Atlanta Braves',
                'Atlanta Braves vs New York Mets',
            ),
            0.45161290322580644,
        )

    def test_fuzzywuzzy_partial_string_dist(self):
        """Test abydos.distance.FuzzyWuzzyPartialString.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.0)
        self.assertEqual(self.cmp.dist('', 'a'), 0.0)
        self.assertEqual(self.cmp.dist('abc', ''), 0.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.4)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.4)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.2)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.2)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.3333333333
        )


if __name__ == '__main__':
    unittest.main()
