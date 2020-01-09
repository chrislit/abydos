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

"""abydos.tests.distance.test_distance_ample.

This module contains unit tests for abydos.distance.AMPLE
"""

import unittest

from abydos.distance import AMPLE


class AMPLETestCases(unittest.TestCase):
    """Test AMPLE functions.

    abydos.distance.AMPLE
    """

    cmp = AMPLE()
    cmp_no_d = AMPLE(alphabet=0)
    cmp_dna = AMPLE(qval=1, alphabet='CGAT')

    def test_ample_sim(self):
        """Test abydos.distance.AMPLE.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.002551020408163265)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.00510204081632653)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.006418485237483954)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.4961439589)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.4961439589)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.4961439589)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.4961439589)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.6324826532
        )
        self.assertAlmostEqual(self.cmp_dna.sim('CGAT', 'CGA'), 0.75)

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp_no_d.sim('Nigel', 'Niall'), 0.5)
        self.assertAlmostEqual(self.cmp_no_d.sim('Niall', 'Nigel'), 0.5)
        self.assertAlmostEqual(self.cmp_no_d.sim('Colin', 'Coiln'), 0.5)
        self.assertAlmostEqual(self.cmp_no_d.sim('Coiln', 'Colin'), 0.5)
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.3636363636
        )


if __name__ == '__main__':
    unittest.main()
