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

"""abydos.tests.distance.test_distance_isg.

This module contains unit tests for abydos.distance.ISG
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import ISG


class ISGTestCases(unittest.TestCase):
    """Test ISG functions.

    abydos.distance.ISG
    """

    cmp = ISG()
    cmp_full = ISG(full_guth=True)

    def test_inclusion_sim(self):
        """Test abydos.distance.ISG.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('a', 'a'), 1.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.0)

        # Testcases from paper
        self.assertEqual(self.cmp.sim('alaire', 'alard'), 0.5714285714285714)
        self.assertEqual(self.cmp.sim('georges', 'george'), 0.8571428571428571)
        self.assertEqual(self.cmp.sim('emile', 'emilien'), 0.7142857142857143)
        self.assertEqual(self.cmp.sim('blanchet', 'blanchette'), 0.8)
        self.assertEqual(self.cmp.sim('marie', 'maria'), 0.6666666666666666)
        self.assertEqual(self.cmp.sim('filion', 'filguion'), 0.75)
        self.assertEqual(self.cmp.sim('daneau', 'dagneau'), 0.8571428571428571)
        self.assertEqual(self.cmp.sim('larouche', 'laroche'), 0.875)
        self.assertEqual(self.cmp.sim('alaire', 'dalaire'), 0.8571428571428571)
        self.assertEqual(self.cmp.sim('donne', 'dionne'), 0.8333333333333334)
        self.assertEqual(self.cmp.sim('audet', 'gaudet'), 0.8333333333333334)
        self.assertEqual(self.cmp.sim('couet', 'caouet'), 0.8333333333333334)
        self.assertEqual(self.cmp.sim('exulie', 'axilia'), 0.5)
        self.assertEqual(self.cmp.sim('leon', 'noel'), 0.3333333333333333)
        self.assertEqual(
            self.cmp.sim('norbert', 'bertran'), 0.16666666666666666
        )

        # Full Guth ruleset tests
        self.assertEqual(
            self.cmp_full.sim('alaire', 'alard'), 0.8333333333333334
        )
        self.assertEqual(
            self.cmp_full.sim('georges', 'george'), 0.8571428571428571
        )
        self.assertEqual(
            self.cmp_full.sim('emile', 'emilien'), 0.7142857142857143
        )
        self.assertEqual(self.cmp_full.sim('blanchet', 'blanchette'), 0.8)
        self.assertEqual(
            self.cmp_full.sim('marie', 'maria'), 0.6666666666666666
        )
        self.assertEqual(self.cmp_full.sim('filion', 'filguion'), 0.75)
        self.assertEqual(
            self.cmp_full.sim('daneau', 'dagneau'), 0.8571428571428571
        )
        self.assertEqual(self.cmp_full.sim('larouche', 'laroche'), 0.875)
        self.assertEqual(
            self.cmp_full.sim('alaire', 'dalaire'), 0.8571428571428571
        )
        self.assertEqual(
            self.cmp_full.sim('donne', 'dionne'), 0.8333333333333334
        )
        self.assertEqual(
            self.cmp_full.sim('audet', 'gaudet'), 0.8333333333333334
        )
        self.assertEqual(
            self.cmp_full.sim('couet', 'caouet'), 0.8333333333333334
        )
        self.assertEqual(
            self.cmp_full.sim('exulie', 'axilia'), 0.7142857142857143
        )
        self.assertEqual(self.cmp_full.sim('leon', 'noel'), 0.3333333333333333)
        self.assertEqual(
            self.cmp_full.sim('norbert', 'bertran'), 0.5555555555555556
        )


if __name__ == '__main__':
    unittest.main()
