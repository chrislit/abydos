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

"""abydos.tests.distance.test_distance_ssk.

This module contains unit tests for abydos.distance.SSK
"""

import unittest

from abydos.distance import SSK

import numpy as np


class SSKTestCases(unittest.TestCase):
    """Test SSK functions.

    abydos.distance.SSK
    """

    cmp = SSK()
    cmp_05 = SSK(ssk_lambda=0.05)

    def test_ssk_sim(self):
        """Test abydos.distance.SSK.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.341958748279)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.341958748279)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.875737900641)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.875737900641)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.932931869
        )

        # Examples from paper
        self.assertAlmostEqual(self.cmp.sim('cat', 'car'), 0.3558718861209964)
        self.assertAlmostEqual(
            self.cmp_05.sim('cat', 'car'), 0.4993757802746567
        )

    def test_ssk_sim_score(self):
        """Test abydos.distance.SSK.sim_score."""
        # Base cases
        self.assertEqual(self.cmp.sim_score('', ''), 0)
        self.assertEqual(self.cmp.sim_score('a', ''), 0)
        self.assertEqual(self.cmp.sim_score('', 'a'), 0)
        self.assertEqual(self.cmp.sim_score('abc', ''), 0)
        self.assertEqual(self.cmp.sim_score('', 'abc'), 0)
        self.assertAlmostEqual(self.cmp.sim_score('abc', 'abc'), 1.843641)
        self.assertEqual(self.cmp.sim_score('abcd', 'efgh'), 0)

        self.assertAlmostEqual(
            self.cmp.sim_score('Nigel', 'Niall'), 2.3009630391
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Niall', 'Nigel'), 2.3009630391
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Colin', 'Coiln'), 4.7537994501
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('Coiln', 'Colin'), 4.7537994501
        )
        self.assertAlmostEqual(
            self.cmp.sim_score('ATCAACGAGT', 'AACGATTAG'), 59.67083050606762
        )

        # Examples from paper
        self.assertEqual(self.cmp.sim_score('cat', 'car'), 0.6561000000000001)
        self.assertEqual(
            self.cmp_05.sim_score('cat', 'car'), 6.250000000000003e-06
        )

        # multiple lambdas
        self.assertAlmostEqual(
            SSK(ssk_lambda=0.05).sim_score('Nigel', 'Niall'),
            6.250822363281253e-06,
        )
        self.assertAlmostEqual(
            SSK(ssk_lambda=0.5).sim_score('Nigel', 'Niall'), 0.0771484375
        )
        self.assertAlmostEqual(
            SSK(ssk_lambda=np.arange(0.05, 0.5, 0.05)).sim_score(
                'Nigel', 'Niall'
            ),
            0.5461411944067384,
        )
        self.assertAlmostEqual(
            SSK(ssk_lambda=(0.05, 0.5)).sim_score('Nigel', 'Niall'),
            0.07841429769736327,
        )


if __name__ == '__main__':
    unittest.main()
