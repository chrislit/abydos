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

"""abydos.tests.distance.test_distance_unknown_f.

This module contains unit tests for abydos.distance.UnknownF
"""

import unittest

from abydos.distance import UnknownF


class UnknownFTestCases(unittest.TestCase):
    """Test UnknownF functions.

    abydos.distance.UnknownF
    """

    cmp = UnknownF()
    cmp_no_d = UnknownF(alphabet=0)

    def test_unknown_f_sim_score(self):
        """Test abydos.distance.UnknownF.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 1.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim_score('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), 0.3068528194
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), 0.3068528194
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Colin', 'Coiln'), 0.3068528194
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Coiln', 'Colin'), 0.3068528194
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 0.5956699662
        )

        # Exceptions
        self.assertRaises(NotImplementedError, self.cmp.sim, 'a', 'a')
        self.assertRaises(NotImplementedError, self.cmp.dist, 'a', 'a')


if __name__ == '__main__':
    unittest.main()
