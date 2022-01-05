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

"""abydos.tests.distance.test_distance_morisita.

This module contains unit tests for abydos.distance.Morisita
"""

import unittest

from abydos.distance import Morisita


class MorisitaTestCases(unittest.TestCase):
    """Test Morisita functions.

    abydos.distance.Morisita
    """

    cmp = Morisita()

    def test_morisita_sim_score(self):
        """Test abydos.distance.Morisita.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('a', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim_score('a', 'a'), 1.0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim_score('abc', 'abc'), 0.5)
        self.assertEqual(self.cmp.sim_score('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), 0.1666666666
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), 0.1666666666
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Colin', 'Coiln'), 0.1666666666
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Coiln', 'Colin'), 0.1666666666
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 0.12727272727
        )

        self.assertAlmostEqual(
            self.cmp.sim_score('sadklsalkdhsa', 'slksajdlkasj'), 1.44
        )

    def test_morisita_dist(self):
        """Test abydos.distance.Morisita.dist."""
        self.assertRaises(NotImplementedError, self.cmp.dist)

    def test_morisita_sim(self):
        """Test abydos.distance.Morisita.sim."""
        self.assertRaises(NotImplementedError, self.cmp.sim)


if __name__ == '__main__':
    unittest.main()
