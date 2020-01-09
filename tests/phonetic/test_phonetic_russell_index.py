# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

"""abydos.tests.phonetic.test_phonetic_russell_index.

This module contains unit tests for abydos.phonetic.RussellIndex
"""

import math
import unittest

from abydos.phonetic import (
    RussellIndex,
    russell_index,
    russell_index_alpha,
    russell_index_num_to_alpha,
)


class RussellIndexTestCases(unittest.TestCase):
    """Test Russel Index functions.

    test cases for abydos.RussellIndex
    """

    pa = RussellIndex()

    def test_russel_index(self):
        """Test abydos.phonetic.RussellIndex."""
        self.assertTrue(math.isnan(self.pa.encode('')))
        self.assertTrue(math.isnan(self.pa.encode('H')))
        self.assertEqual(self.pa.encode('Hoppa'), 12)
        self.assertEqual(self.pa.encode('Hopley'), 125)
        self.assertEqual(self.pa.encode('Highfield'), 1254)
        self.assertEqual(self.pa.encode('Wright'), 814)
        self.assertEqual(self.pa.encode('Carter'), 31848)
        self.assertEqual(self.pa.encode('Hopf'), 12)
        self.assertEqual(self.pa.encode('Hay'), 1)
        self.assertEqual(self.pa.encode('Haas'), 1)
        self.assertEqual(self.pa.encode('Meyers'), 618)
        self.assertEqual(self.pa.encode('Myers'), 618)
        self.assertEqual(self.pa.encode('Meyer'), 618)
        self.assertEqual(self.pa.encode('Myer'), 618)
        self.assertEqual(self.pa.encode('Mack'), 613)
        self.assertEqual(self.pa.encode('Knack'), 3713)

        # Test wrapper
        self.assertEqual(russell_index('Highfield'), 1254)

    def test_russel_index_n2a(self):
        """Test abydos.phonetic.RussellIndex._to_alpha."""
        self.assertEqual(self.pa._to_alpha(0), '')  # noqa: SF01
        self.assertEqual(self.pa._to_alpha(''), '')  # noqa: SF01
        self.assertEqual(self.pa._to_alpha(float('NaN')), '')  # noqa: SF01
        self.assertEqual(
            self.pa._to_alpha(123456789), 'ABCDLMNR'  # noqa: SF01
        )
        self.assertEqual(
            self.pa._to_alpha('0123456789'), 'ABCDLMNR'  # noqa: SF01
        )

        # Test wrapper
        self.assertEqual(russell_index_num_to_alpha(123456789), 'ABCDLMNR')

    def test_russel_index_alpha(self):
        """Test abydos.phonetic.RussellIndex.encode_alpha."""
        self.assertEqual(self.pa.encode_alpha(''), '')
        self.assertEqual(self.pa.encode_alpha('H'), '')
        self.assertEqual(self.pa.encode_alpha('Hoppa'), 'AB')
        self.assertEqual(self.pa.encode_alpha('Hopley'), 'ABL')
        self.assertEqual(self.pa.encode_alpha('Highfield'), 'ABLD')
        self.assertEqual(self.pa.encode_alpha('Wright'), 'RAD')
        self.assertEqual(self.pa.encode_alpha('Carter'), 'CARDR')
        self.assertEqual(self.pa.encode_alpha('Hopf'), 'AB')
        self.assertEqual(self.pa.encode_alpha('Hay'), 'A')
        self.assertEqual(self.pa.encode_alpha('Haas'), 'A')
        self.assertEqual(self.pa.encode_alpha('Meyers'), 'MAR')
        self.assertEqual(self.pa.encode_alpha('Myers'), 'MAR')
        self.assertEqual(self.pa.encode_alpha('Meyer'), 'MAR')
        self.assertEqual(self.pa.encode_alpha('Myer'), 'MAR')
        self.assertEqual(self.pa.encode_alpha('Mack'), 'MAC')
        self.assertEqual(self.pa.encode_alpha('Knack'), 'CNAC')

        # Test wrapper
        self.assertEqual(russell_index_alpha('Highfield'), 'ABLD')


if __name__ == '__main__':
    unittest.main()
