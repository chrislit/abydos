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

"""abydos.tests.distance.test_distance_fuzzywuzzy_token_sort.

This module contains unit tests for abydos.distance.FuzzyWuzzyTokenSort
"""

import unittest

from abydos.distance import FuzzyWuzzyTokenSort
from abydos.tokenizer import QGrams


class FuzzyWuzzyTokenSortTestCases(unittest.TestCase):
    """Test FuzzyWuzzyTokenSort functions.

    abydos.distance.FuzzyWuzzyTokenSort
    """

    cmp = FuzzyWuzzyTokenSort()
    cmp_q2 = FuzzyWuzzyTokenSort(tokenizer=QGrams(qval=2))

    def test_fuzzywuzzy_token_sort_sim(self):
        """Test abydos.distance.FuzzyWuzzyTokenSort.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.6)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.6)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.8)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.8)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.6315789474
        )

        # tests from blog
        self.assertEqual(
            self.cmp.sim(
                'New York Mets vs Atlanta Braves',
                'Atlanta Braves vs New York Mets',
            ),
            1.0,
        )

        # q2 tokenizer
        self.assertAlmostEqual(
            self.cmp_q2.sim('ATCAACGAGT', 'AACGATTAG'), 0.8524590163934426
        )
        self.assertAlmostEqual(
            self.cmp_q2.sim('YANKEES', 'NEW YORK YANKEES'), 0.6027397260273972
        )
        self.assertAlmostEqual(
            self.cmp_q2.sim('NEW YORK METS', 'NEW YORK YANKEES'),
            0.7692307692307693,
        )
        self.assertAlmostEqual(
            self.cmp_q2.sim(
                'New York Mets vs Atlanta Braves',
                'Atlanta Braves vs New York Mets',
            ),
            0.9578947368421052,
        )

    def test_fuzzywuzzy_token_sort_dist(self):
        """Test abydos.distance.FuzzyWuzzyTokenSort.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.4)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.4)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.2)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.2)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.3684210526
        )


if __name__ == '__main__':
    unittest.main()
