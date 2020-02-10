# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_monge_elkan.

This module contains unit tests for abydos.distance.MongeElkan
"""

import unittest

from abydos.distance import Jaccard, MongeElkan


class MongeElkanTestCases(unittest.TestCase):
    """Test Monge-Elkan functions.

    abydos.distance.MongeElkan
    """

    cmp = MongeElkan()
    cmp_sym = MongeElkan(symmetric=True)
    cmp_jac = MongeElkan(sim_func=Jaccard())
    cmp_jac_sim = MongeElkan(sim_func=Jaccard().sim)

    def test_monge_elkan_sim(self):
        """Test abydos.distance.MongeElkan.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('', 'a'), 0)
        self.assertEqual(self.cmp.sim('a', 'a'), 1)

        self.assertEqual(self.cmp.sim('Niall', 'Neal'), 3 / 4)
        self.assertEqual(self.cmp.sim('Niall', 'Njall'), 5 / 6)
        self.assertEqual(self.cmp.sim('Niall', 'Niel'), 3 / 4)
        self.assertEqual(self.cmp.sim('Niall', 'Nigel'), 3 / 4)

        self.assertEqual(self.cmp_sym.sim('Niall', 'Neal'), 31 / 40)
        self.assertEqual(self.cmp_sym.sim('Niall', 'Njall'), 5 / 6)
        self.assertEqual(self.cmp_sym.sim('Niall', 'Niel'), 31 / 40)
        self.assertAlmostEqual(self.cmp_sym.sim('Niall', 'Nigel'), 17 / 24)

        self.assertEqual(self.cmp_jac.sim('Njall', 'Neil'), 29 / 60)
        self.assertEqual(self.cmp_jac_sim.sim('Njall', 'Neil'), 29 / 60)

    def test_monge_elkan_dist(self):
        """Test abydos.distance.MongeElkan.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('', 'a'), 1)

        self.assertEqual(self.cmp.dist('Niall', 'Neal'), 1 / 4)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Njall'), 1 / 6)
        self.assertEqual(self.cmp.dist('Niall', 'Niel'), 1 / 4)
        self.assertEqual(self.cmp.dist('Niall', 'Nigel'), 1 / 4)

        self.assertAlmostEqual(self.cmp_sym.dist('Niall', 'Neal'), 9 / 40)
        self.assertAlmostEqual(self.cmp_sym.dist('Niall', 'Njall'), 1 / 6)
        self.assertAlmostEqual(self.cmp_sym.dist('Niall', 'Niel'), 9 / 40)
        self.assertAlmostEqual(self.cmp_sym.dist('Niall', 'Nigel'), 7 / 24)


if __name__ == '__main__':
    unittest.main()
