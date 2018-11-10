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

"""abydos.tests.phonetic.test_phonetic_dm.

This module contains unit tests for abydos.phonetic._dm
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.phonetic import dm_soundex


class DMSoundexTestCases(unittest.TestCase):
    """Test Daitch-Mokotoff Soundex functions.

    test cases for abydos.phonetic._dm.dm_soundex
    """

    def test_dm_soundex(self):
        """Test abydos.phonetic._dm.dm_soundex (Daitch-Mokotoff Soundex)."""
        # D-M tests
        self.assertEqual(dm_soundex(''), {'000000'})

        # http://www.avotaynu.com/soundex.htm
        self.assertEqual(dm_soundex('Augsburg'), {'054795'})
        self.assertEqual(dm_soundex('Breuer'), {'791900'})
        self.assertEqual(dm_soundex('Halberstadt'), {'587943', '587433'})
        self.assertEqual(dm_soundex('Mannheim'), {'665600'})
        self.assertEqual(dm_soundex('Chernowitz'), {'496740', '596740'})
        self.assertEqual(dm_soundex('Cherkassy'), {'495400', '595400'})
        self.assertEqual(dm_soundex('Kleinman'), {'586660'})
        self.assertEqual(dm_soundex('Berlin'), {'798600'})

        self.assertEqual(dm_soundex('Ceniow'), {'467000', '567000'})
        self.assertEqual(dm_soundex('Tsenyuv'), {'467000'})
        self.assertEqual(dm_soundex('Holubica'), {'587400', '587500'})
        self.assertEqual(dm_soundex('Golubitsa'), {'587400'})
        self.assertEqual(dm_soundex('Przemysl'), {'746480', '794648'})
        self.assertEqual(dm_soundex('Pshemeshil'), {'746480'})
        self.assertEqual(
            dm_soundex('Rosochowaciec'),
            {
                '944744',
                '945744',
                '944755',
                '944754',
                '944745',
                '945745',
                '945754',
                '945755',
            },
        )
        self.assertEqual(dm_soundex('Rosokhovatsets'), {'945744'})

        # https://en.wikipedia.org/wiki/Daitch%E2%80%93Mokotoff_Soundex
        self.assertEqual(dm_soundex('Peters'), {'739400', '734000'})
        self.assertEqual(dm_soundex('Peterson'), {'739460', '734600'})
        self.assertEqual(dm_soundex('Moskowitz'), {'645740'})
        self.assertEqual(dm_soundex('Moskovitz'), {'645740'})
        self.assertEqual(dm_soundex('Auerbach'), {'097500', '097400'})
        self.assertEqual(dm_soundex('Uhrbach'), {'097500', '097400'})
        self.assertEqual(
            dm_soundex('Jackson'), {'154600', '454600', '145460', '445460'}
        )
        self.assertEqual(
            dm_soundex('Jackson-Jackson'),
            {
                '154654',
                '454654',
                '145465',
                '445465',
                '154645',
                '454645',
                '145464',
                '445464',
                '154644',
                '454644',
            },
        )

        # http://www.jewishgen.org/infofiles/soundex.html
        self.assertEqual(dm_soundex('OHRBACH'), {'097500', '097400'})
        self.assertEqual(dm_soundex('LIPSHITZ'), {'874400'})
        self.assertEqual(dm_soundex('LIPPSZYC'), {'874400', '874500'})
        self.assertEqual(dm_soundex('LEWINSKY'), {'876450'})
        self.assertEqual(dm_soundex('LEVINSKI'), {'876450'})
        self.assertEqual(dm_soundex('SZLAMAWICZ'), {'486740'})
        self.assertEqual(dm_soundex('SHLAMOVITZ'), {'486740'})

        # http://community.actian.com/wiki/OME_soundex_dm()
        self.assertEqual(dm_soundex('Schwarzenegger'), {'479465', '474659'})
        self.assertEqual(dm_soundex('Shwarzenegger'), {'479465', '474659'})
        self.assertEqual(dm_soundex('Schwartsenegger'), {'479465'})

        # max_length bounds tests
        self.assertEqual(dm_soundex('Niall', max_length=-1), {'68' + '0' * 62})
        self.assertEqual(dm_soundex('Niall', max_length=0), {'680000'})

        # zero_pad tests
        self.assertEqual(
            dm_soundex('Niall', max_length=-1, zero_pad=False), {'68'}
        )
        self.assertEqual(
            dm_soundex('Niall', max_length=0, zero_pad=False), {'68'}
        )
        self.assertEqual(
            dm_soundex('Niall', max_length=0, zero_pad=True), {'680000'}
        )
        self.assertEqual(dm_soundex('', max_length=6, zero_pad=False), {'0'})
        self.assertEqual(
            dm_soundex('', max_length=6, zero_pad=True), {'000000'}
        )


if __name__ == '__main__':
    unittest.main()
