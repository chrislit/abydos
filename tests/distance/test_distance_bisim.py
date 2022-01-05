# Copyright 2019-2022 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_bisim.

This module contains unit tests for abydos.distance.BISIM
"""

import unittest

from abydos.distance import BISIM


class BISIMTestCases(unittest.TestCase):
    """Test BISIM functions.

    abydos.distance.BISIM
    """

    cmp = BISIM()
    cmp3 = BISIM(qval=3)

    def test_bi_sim_sim(self):
        """Test abydos.distance.BISIM.sim."""
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
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.6)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.6)
        self.assertAlmostEqual(self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.6)

        # test cases from Kondrak and Dorr (2003)
        self.assertAlmostEqual(self.cmp.sim('ara', 'ala'), 0.6666666667)
        self.assertAlmostEqual(self.cmp.sim('atara', 'arata'), 0.6)
        self.assertAlmostEqual(self.cmp.sim('amaryl', 'amikin'), 0.4166666667)
        self.assertAlmostEqual(self.cmp.sim('amaryl', 'altoce'), 0.250)

        # other examples from Kondrak and Dorr (2004)
        self.assertAlmostEqual(self.cmp.sim('Zantac', 'Xanax'), 0.4166666667)
        self.assertAlmostEqual(self.cmp.sim('Zantac', 'Contac'), 0.5833333333)
        self.assertAlmostEqual(self.cmp.sim('Xanax', 'Contac'), 0.25)
        self.assertAlmostEqual(self.cmp3.sim('Zantac', 'Xanax'), 0.333333333)
        self.assertAlmostEqual(self.cmp3.sim('Zantac', 'Contac'), 0.5)
        self.assertAlmostEqual(self.cmp3.sim('Xanax', 'Contac'), 0.166666667)

        self.assertAlmostEqual(self.cmp.sim('Toradol', 'Tramadol'), 0.6875)
        self.assertAlmostEqual(self.cmp.sim('Toradol', 'Tobradex'), 0.6250)
        self.assertAlmostEqual(self.cmp.sim('Toradol', 'Torecan'), 0.57142857)
        self.assertAlmostEqual(self.cmp.sim('Toradol', 'Stadol'), 0.5)
        self.assertAlmostEqual(self.cmp.sim('Toradol', 'Torsemide'), 0.5)
        self.assertAlmostEqual(self.cmp.sim('Toradol', 'Theraflu'), 0.5)
        self.assertAlmostEqual(self.cmp.sim('Toradol', 'Tegretol'), 0.5)
        self.assertAlmostEqual(self.cmp.sim('Toradol', 'Taxol'), 0.5)


if __name__ == '__main__':
    unittest.main()
