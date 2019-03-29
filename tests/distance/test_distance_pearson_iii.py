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

"""abydos.tests.distance.test_distance_pearson_iii.

This module contains unit tests for abydos.distance.PearsonIII
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import PearsonIII


class PearsonIIITestCases(unittest.TestCase):
    """Test PearsonIII functions.

    abydos.distance.PearsonIII
    """

    cmp = PearsonIII()
    cmp_no_d = PearsonIII(alphabet=0)

    def test_pearson_iii_corr(self):
        """Test abydos.distance.PearsonIII.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), float('nan'))
        self.assertEqual(self.cmp.corr('a', ''), float('nan'))
        self.assertEqual(self.cmp.corr('', 'a'), float('nan'))
        self.assertEqual(self.cmp.corr('abc', ''), float('nan'))
        self.assertEqual(self.cmp.corr('', 'abc'), float('nan'))
        self.assertEqual(self.cmp.corr('abc', 'abc'), 0.03569153051241248)
        self.assertEqual(
            self.cmp.corr('abcd', 'efgh'),
            (1.7520273272936104e-19 + 0.0028612777635371113j),
        )

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.0251482893)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.0251482893)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.0251482893)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.0251482893)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.0290663533
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.corr('a', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.corr('', 'a'), float('nan'))
        self.assertEqual(self.cmp_no_d.corr('abc', ''), float('nan'))
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), float('nan'))
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), float('nan'))
        self.assertEqual(
            self.cmp_no_d.corr('abcd', 'efgh'),
            (2.041077998578922e-17 + 0.3333333333333333j),
        )

        self.assertAlmostEqual(
            self.cmp_no_d.corr('Nigel', 'Niall'), float('nan')
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Niall', 'Nigel'), float('nan')
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Colin', 'Coiln'), float('nan')
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Coiln', 'Colin'), float('nan')
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), float('nan')
        )


if __name__ == '__main__':
    unittest.main()
