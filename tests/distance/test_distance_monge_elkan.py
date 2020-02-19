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
from abydos.tokenizer import QGrams


class MongeElkanTestCases(unittest.TestCase):
    """Test Monge-Elkan functions.

    abydos.distance.MongeElkan
    """

    q2 = QGrams()
    cmp = MongeElkan()
    cmp_q2 = MongeElkan(tokenizer=q2)
    cmp_sym = MongeElkan(symmetric=True, tokenizer=q2)
    cmp_jac = MongeElkan(sim_func=Jaccard(), tokenizer=q2)
    cmp_jac_sim = MongeElkan(sim_func=Jaccard().sim, tokenizer=q2)

    def test_monge_elkan_sim(self):
        """Test abydos.distance.MongeElkan.sim."""
        self.assertEqual(self.cmp_q2.sim('', ''), 1)
        self.assertEqual(self.cmp_q2.sim('', 'a'), 0)
        self.assertEqual(self.cmp_q2.sim('a', 'a'), 1)

        self.assertEqual(self.cmp_q2.sim('Niall', 'Neal'), 3 / 4)
        self.assertEqual(self.cmp_q2.sim('Niall', 'Njall'), 5 / 6)
        self.assertEqual(self.cmp_q2.sim('Niall', 'Niel'), 3 / 4)
        self.assertEqual(self.cmp_q2.sim('Niall', 'Nigel'), 3 / 4)

        self.assertEqual(self.cmp_sym.sim('Niall', 'Neal'), 31 / 40)
        self.assertEqual(self.cmp_sym.sim('Niall', 'Njall'), 5 / 6)
        self.assertEqual(self.cmp_sym.sim('Niall', 'Niel'), 31 / 40)
        self.assertAlmostEqual(self.cmp_sym.sim('Niall', 'Nigel'), 17 / 24)

        self.assertEqual(self.cmp_jac.sim('Njall', 'Neil'), 29 / 60)
        self.assertEqual(self.cmp_jac_sim.sim('Njall', 'Neil'), 29 / 60)

        self.assertAlmostEqual(
            MongeElkan().sim(
                'Comput. Sci. & Eng. Dept., University of California, San Diego',  # noqa: E501
                'Department of Computer Science, Univ. Calif., San Diego',
            ),
            1297 / 2200,
        )

    def test_monge_elkan_dist(self):
        """Test abydos.distance.MongeElkan.dist."""
        self.assertEqual(self.cmp_q2.dist('', ''), 0)
        self.assertEqual(self.cmp_q2.dist('', 'a'), 1)

        self.assertEqual(self.cmp_q2.dist('Niall', 'Neal'), 1 / 4)
        self.assertAlmostEqual(self.cmp_q2.dist('Niall', 'Njall'), 1 / 6)
        self.assertEqual(self.cmp_q2.dist('Niall', 'Niel'), 1 / 4)
        self.assertEqual(self.cmp_q2.dist('Niall', 'Nigel'), 1 / 4)

        self.assertAlmostEqual(self.cmp_sym.dist('Niall', 'Neal'), 9 / 40)
        self.assertAlmostEqual(self.cmp_sym.dist('Niall', 'Njall'), 1 / 6)
        self.assertAlmostEqual(self.cmp_sym.dist('Niall', 'Niel'), 9 / 40)
        self.assertAlmostEqual(self.cmp_sym.dist('Niall', 'Nigel'), 7 / 24)


if __name__ == '__main__':
    unittest.main()
