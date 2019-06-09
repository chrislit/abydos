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

    def test_inclusion_dist(self):
        """Test abydos.distance.ISG.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('a', 'a'), 0.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        # Tescases from paper
        self.assertEqual(self.cmp.dist('alaire', 'alard'), 0.5714285714285714)
        self.assertEqual(
            self.cmp.dist('georges', 'george'), 0.8571428571428571
        )
        self.assertEqual(self.cmp.dist('emile', 'emilien'), 0.7142857142857143)
        self.assertEqual(self.cmp.dist('blanchet', 'blanchette'), 0.8)
        self.assertEqual(self.cmp.dist('marie', 'maria'), 0.6666666666666666)
        self.assertEqual(self.cmp.dist('filion', 'filguion'), 0.75)
        self.assertEqual(
            self.cmp.dist('daneau', 'dagneau'), 0.8571428571428571
        )
        self.assertEqual(self.cmp.dist('larouche', 'laroche'), 0.875)
        self.assertEqual(
            self.cmp.dist('alaire', 'dalaire'), 0.8571428571428571
        )
        self.assertEqual(self.cmp.dist('donne', 'dionne'), 0.8333333333333334)
        self.assertEqual(self.cmp.dist('audet', 'gaudet'), 0.8333333333333334)
        self.assertEqual(self.cmp.dist('couet', 'caouet'), 0.8333333333333334)
        self.assertEqual(self.cmp.dist('exulie', 'axilia'), 0.5)
        self.assertEqual(self.cmp.dist('leon', 'noel'), 0.3333333333333333)
        self.assertEqual(
            self.cmp.dist('norbert', 'bertran'), 0.16666666666666666
        )


if __name__ == '__main__':
    unittest.main()
