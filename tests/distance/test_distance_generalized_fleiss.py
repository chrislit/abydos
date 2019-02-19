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

"""abydos.tests.distance.test_distance_generalized_fleiss.

This module contains unit tests for abydos.distance.GeneralizedFleiss
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import GeneralizedFleiss


class GeneralizedFleissTestCases(unittest.TestCase):
    """Test GeneralizedFleiss functions.

    abydos.distance.GeneralizedFleiss
    """

    cmp = GeneralizedFleiss()
    cmp_no_d = GeneralizedFleiss(alphabet=1)

    def test_generalized_fleiss_sim(self):
        """Test abydos.distance.GeneralizedFleiss.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), float('nan'))
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), -0.006418485237483954)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.4961439589)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.4961439589)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.4961439589)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.4961439589)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.6626008748
        )

        # Tests with alphabet=1 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('a', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), -1.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), -0.5)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), -0.5)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), -0.5)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), -0.5)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), -0.380952381
        )


if __name__ == '__main__':
    unittest.main()
