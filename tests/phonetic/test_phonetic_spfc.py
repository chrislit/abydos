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

"""abydos.tests.phonetic.test_phonetic_spfc.

This module contains unit tests for abydos.phonetic.SPFC
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.phonetic import SPFC, spfc


class SPFCTestCases(unittest.TestCase):
    """Test SPFC functions.

    test cases for abydos.phonetic.SPFC
    """

    pa = SPFC()

    def test_spfc(self):
        """Test abydos.phonetic.SPFC."""
        self.assertEqual(self.pa.encode(''), '')

        # https://archive.org/stream/accessingindivid00moor#page/19/mode/1up
        self.assertEqual(self.pa.encode(('J', 'KUHNS')), '16760')
        self.assertEqual(self.pa.encode(('G', 'ALTSHULER')), '35797')
        self.assertEqual(self.pa.encode('J KUHNS'), '16760')
        self.assertEqual(self.pa.encode('G ALTSHULER'), '35797')
        self.assertEqual(self.pa.encode('J. KUHNS'), '16760')
        self.assertEqual(self.pa.encode('G. ALTSHULER'), '35797')
        self.assertEqual(self.pa.encode('J. Kuhns'), '16760')
        self.assertEqual(self.pa.encode('G. Altshuler'), '35797')
        self.assertEqual(self.pa.encode('T. Vines'), '16760')
        self.assertEqual(self.pa.encode('J. Butler'), '35779')
        self.assertNotEqual(
            self.pa.encode('J. Kuhns'), self.pa.encode('J. Kuntz')
        )
        self.assertEqual(self.pa.encode('Jon Kuhns'), '16760')
        self.assertEqual(self.pa.encode('James Kuhns'), '16760')

        self.assertRaises(AttributeError, self.pa.encode, ('J', 'A', 'Kuhns'))
        self.assertRaises(AttributeError, self.pa.encode, 'JKuhns')
        self.assertRaises(AttributeError, self.pa.encode, 5)

        # etc. (for code coverage)
        self.assertEqual(self.pa.encode('James Goldstein'), '77795')
        self.assertEqual(self.pa.encode('James Hansen'), '57760')
        self.assertEqual(self.pa.encode('James Hester'), '57700')
        self.assertEqual(self.pa.encode('James Bardot'), '31745')
        self.assertEqual(self.pa.encode('James Windsor'), '27765')
        self.assertEqual(self.pa.encode('James Wenders'), '27760')
        self.assertEqual(self.pa.encode('James Ventor'), '17760')
        self.assertEqual(self.pa.encode('þ þ'), '00')

        # encode_alpha
        self.assertEqual(self.pa.encode_alpha('J. Kuhns'), 'CSGMS')
        self.assertEqual(self.pa.encode_alpha('G. Altshuler'), 'ARGEG')
        self.assertEqual(self.pa.encode_alpha('T. Vines'), 'CSGMS')
        self.assertEqual(self.pa.encode_alpha('James Ventor'), 'CZGMS')

        # Test wrapper
        self.assertEqual(spfc('G ALTSHULER'), '35797')


if __name__ == '__main__':
    unittest.main()
