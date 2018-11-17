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

"""abydos.tests.phonetic.test_phonetic_fuzzy_soundex.

This module contains unit tests for abydos.phonetic.FuzzySoundex
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.phonetic import FuzzySoundex, fuzzy_soundex


class FuzzySoundexTestCases(unittest.TestCase):
    """Test Fuzzy Soundex functions.

    test cases for abydos.phonetic.FuzzySoundex
    """

    pa = FuzzySoundex()

    def test_fuzzy_soundex(self):
        """Test abydos.phonetic.FuzzySoundex."""
        self.assertEqual(self.pa.encode(''), '00000')
        # http://wayback.archive.org/web/20100629121128/http://www.ir.iit.edu/publications/downloads/IEEESoundexV5.pdf
        self.assertEqual(self.pa.encode('Kristen'), 'K6935')
        self.assertEqual(self.pa.encode('Krissy'), 'K6900')
        self.assertEqual(self.pa.encode('Christen'), 'K6935')

        # http://books.google.com/books?id=LZrT6eWf9NMC&lpg=PA76&ots=Tex3FqNwGP&dq=%22phonix%20algorithm%22&pg=PA75#v=onepage&q=%22phonix%20algorithm%22&f=false
        self.assertEqual(self.pa.encode('peter', 4), 'P360')
        self.assertEqual(self.pa.encode('pete', 4), 'P300')
        self.assertEqual(self.pa.encode('pedro', 4), 'P360')
        self.assertEqual(self.pa.encode('stephen', 4), 'S315')
        self.assertEqual(self.pa.encode('steve', 4), 'S310')
        self.assertEqual(self.pa.encode('smith', 4), 'S530')
        self.assertEqual(self.pa.encode('smythe', 4), 'S530')
        self.assertEqual(self.pa.encode('gail', 4), 'G400')
        self.assertEqual(self.pa.encode('gayle', 4), 'G400')
        self.assertEqual(self.pa.encode('christine', 4), 'K693')
        self.assertEqual(self.pa.encode('christina', 4), 'K693')
        self.assertEqual(self.pa.encode('kristina', 4), 'K693')

        # etc. (for code coverage)
        self.assertEqual(self.pa.encode('Wight'), 'W3000')
        self.assertEqual(self.pa.encode('Hardt'), 'H6000')
        self.assertEqual(self.pa.encode('Knight'), 'N3000')
        self.assertEqual(self.pa.encode('Czech'), 'S7000')
        self.assertEqual(self.pa.encode('Tsech'), 'S7000')
        self.assertEqual(self.pa.encode('gnomic'), 'N5900')
        self.assertEqual(self.pa.encode('Wright'), 'R3000')
        self.assertEqual(self.pa.encode('Hrothgar'), 'R3760')
        self.assertEqual(self.pa.encode('Hwaet'), 'W3000')
        self.assertEqual(self.pa.encode('Grant'), 'G6300')
        self.assertEqual(self.pa.encode('Hart'), 'H6000')
        self.assertEqual(self.pa.encode('Hardt'), 'H6000')

        # max_length bounds tests
        self.assertEqual(
            self.pa.encode('Niall', max_length=-1),
            'N4000000000000000000000000000000000000000000000000'
            + '00000000000000',
        )
        self.assertEqual(self.pa.encode('Niall', max_length=0), 'N400')

        # zero_pad tests
        self.assertEqual(
            self.pa.encode('Niall', max_length=-1, zero_pad=False), 'N4'
        )
        self.assertEqual(
            self.pa.encode('Niall', max_length=0, zero_pad=False), 'N4'
        )
        self.assertEqual(
            self.pa.encode('Niall', max_length=0, zero_pad=True), 'N400'
        )
        self.assertEqual(self.pa.encode('', max_length=4, zero_pad=False), '0')
        self.assertEqual(
            self.pa.encode('', max_length=4, zero_pad=True), '0000'
        )

        # Test wrapper
        self.assertEqual(fuzzy_soundex('Kristen'), 'K6935')


if __name__ == '__main__':
    unittest.main()
