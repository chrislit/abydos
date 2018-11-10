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

"""abydos.tests.phonetic.test_phonetic_russell.

This module contains unit tests for abydos.phonetic._russell
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import math
import unittest

from abydos.phonetic import (
    russell_index,
    russell_index_alpha,
    russell_index_num_to_alpha,
)


class RussellIndexTestCases(unittest.TestCase):
    """Test Russel Index functions.

    test cases for abydos.phonetic._russell.russell_index,
    .russell_index_num_to_alpha, & .russell_index_alpha
    """

    def test_russel_index(self):
        """Test abydos.phonetic._russell.russell_index."""
        self.assertTrue(math.isnan(russell_index('')))
        self.assertTrue(math.isnan(russell_index('H')))
        self.assertEqual(russell_index('Hoppa'), 12)
        self.assertEqual(russell_index('Hopley'), 125)
        self.assertEqual(russell_index('Highfield'), 1254)
        self.assertEqual(russell_index('Wright'), 814)
        self.assertEqual(russell_index('Carter'), 31848)
        self.assertEqual(russell_index('Hopf'), 12)
        self.assertEqual(russell_index('Hay'), 1)
        self.assertEqual(russell_index('Haas'), 1)
        self.assertEqual(russell_index('Meyers'), 618)
        self.assertEqual(russell_index('Myers'), 618)
        self.assertEqual(russell_index('Meyer'), 618)
        self.assertEqual(russell_index('Myer'), 618)
        self.assertEqual(russell_index('Mack'), 613)
        self.assertEqual(russell_index('Knack'), 3713)

    def test_russel_index_n2a(self):
        """Test abydos.phonetic._russell.russell_index_num_to_alpha."""
        self.assertEqual(russell_index_num_to_alpha(0), '')
        self.assertEqual(russell_index_num_to_alpha(''), '')
        self.assertEqual(russell_index_num_to_alpha(float('NaN')), '')
        self.assertEqual(russell_index_num_to_alpha(123456789), 'ABCDLMNR')
        self.assertEqual(russell_index_num_to_alpha('0123456789'), 'ABCDLMNR')

    def test_russel_index_alpha(self):
        """Test abydos.phonetic._russell.russell_index_alpha."""
        self.assertEqual(russell_index_alpha(''), '')
        self.assertEqual(russell_index_alpha('H'), '')
        self.assertEqual(russell_index_alpha('Hoppa'), 'AB')
        self.assertEqual(russell_index_alpha('Hopley'), 'ABL')
        self.assertEqual(russell_index_alpha('Highfield'), 'ABLD')
        self.assertEqual(russell_index_alpha('Wright'), 'RAD')
        self.assertEqual(russell_index_alpha('Carter'), 'CARDR')
        self.assertEqual(russell_index_alpha('Hopf'), 'AB')
        self.assertEqual(russell_index_alpha('Hay'), 'A')
        self.assertEqual(russell_index_alpha('Haas'), 'A')
        self.assertEqual(russell_index_alpha('Meyers'), 'MAR')
        self.assertEqual(russell_index_alpha('Myers'), 'MAR')
        self.assertEqual(russell_index_alpha('Meyer'), 'MAR')
        self.assertEqual(russell_index_alpha('Myer'), 'MAR')
        self.assertEqual(russell_index_alpha('Mack'), 'MAC')
        self.assertEqual(russell_index_alpha('Knack'), 'CNAC')


if __name__ == '__main__':
    unittest.main()
