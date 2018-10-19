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

"""abydos.tests.test_phonetic_spfc.

This module contains unit tests for abydos.phonetic.spfc
"""

from __future__ import unicode_literals

import unittest

from abydos.phonetic.spfc import spfc


class SPFCTestCases(unittest.TestCase):
    """Test SPFC functions.

    test cases for abydos.phonetic.spfc
    """

    def test_spfc(self):
        """Test abydos.phonetic.spfc."""
        self.assertEqual(spfc(''), '')

        # https://archive.org/stream/accessingindivid00moor#page/19/mode/1up
        self.assertEqual(spfc(('J', 'KUHNS')), '16760')
        self.assertEqual(spfc(('G', 'ALTSHULER')), '35797')
        self.assertEqual(spfc('J KUHNS'), '16760')
        self.assertEqual(spfc('G ALTSHULER'), '35797')
        self.assertEqual(spfc('J. KUHNS'), '16760')
        self.assertEqual(spfc('G. ALTSHULER'), '35797')
        self.assertEqual(spfc('J. Kuhns'), '16760')
        self.assertEqual(spfc('G. Altshuler'), '35797')
        self.assertEqual(spfc('T. Vines'), '16760')
        self.assertEqual(spfc('J. Butler'), '35779')
        self.assertNotEqual(spfc('J. Kuhns'), spfc('J. Kuntz'))
        self.assertEqual(spfc('Jon Kuhns'), '16760')
        self.assertEqual(spfc('James Kuhns'), '16760')

        self.assertRaises(AttributeError, spfc, ('J', 'A', 'Kuhns'))
        self.assertRaises(AttributeError, spfc, 'JKuhns')
        self.assertRaises(AttributeError, spfc, 5)

        # etc. (for code coverage)
        self.assertEqual(spfc('James Goldstein'), '78795')
        self.assertEqual(spfc('James Hansen'), '58760')
        self.assertEqual(spfc('James Hester'), '59700')
        self.assertEqual(spfc('James Bardot'), '31745')
        self.assertEqual(spfc('James Windsor'), '29765')
        self.assertEqual(spfc('James Wenders'), '27760')
        self.assertEqual(spfc('James Ventor'), '17760')
        self.assertEqual(spfc('þ þ'), '00')


if __name__ == '__main__':
    unittest.main()
