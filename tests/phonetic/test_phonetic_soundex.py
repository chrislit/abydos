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

"""abydos.tests.phonetic.test_phonetic_soundex.

This module contains unit tests for abydos.phonetic.Soundex
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.phonetic import Soundex, soundex


class SoundexTestCases(unittest.TestCase):
    """Test Soundex functions.

    test cases for abydos.phonetic.Soundex
    """

    pa = Soundex()

    def test_soundex(self):
        """Test abydos.phonetic._soundex.soundex."""
        self.assertEqual(self.pa.encode(''), '0000')

        # https://archive.org/stream/accessingindivid00moor#page/14/mode/2up
        self.assertEqual(self.pa.encode('Euler'), 'E460')
        self.assertEqual(self.pa.encode('Gauss'), 'G200')
        self.assertEqual(self.pa.encode('Hilbert'), 'H416')
        self.assertEqual(self.pa.encode('Knuth'), 'K530')
        self.assertEqual(self.pa.encode('Lloyd'), 'L300')
        self.assertEqual(self.pa.encode('Lukasieicz'), 'L222')
        self.assertEqual(self.pa.encode('Ellery'), 'E460')
        self.assertEqual(self.pa.encode('Ghosh'), 'G200')
        self.assertEqual(self.pa.encode('Heilbronn'), 'H416')
        self.assertEqual(self.pa.encode('Kant'), 'K530')
        self.assertEqual(self.pa.encode('Ladd'), 'L300')
        self.assertEqual(self.pa.encode('Lissajous'), 'L222')
        self.assertEqual(self.pa.encode('Rogers'), 'R262')
        self.assertEqual(self.pa.encode('Rodgers'), 'R326')
        self.assertNotEqual(
            self.pa.encode('Rogers'), self.pa.encode('Rodgers')
        )
        self.assertNotEqual(
            self.pa.encode('Sinclair'), self.pa.encode('St. Clair')
        )
        self.assertNotEqual(
            self.pa.encode('Tchebysheff'), self.pa.encode('Chebyshev')
        )

        # http://creativyst.com/Doc/Articles/SoundEx1/SoundEx1.htm#Related
        self.assertEqual(self.pa.encode('Htacky'), 'H320')
        self.assertEqual(self.pa.encode('Atacky'), 'A320')
        self.assertEqual(self.pa.encode('Schmit'), 'S530')
        self.assertEqual(self.pa.encode('Schneider'), 'S536')
        self.assertEqual(self.pa.encode('Pfister'), 'P236')
        self.assertEqual(self.pa.encode('Ashcroft'), 'A261')
        self.assertEqual(self.pa.encode('Asicroft'), 'A226')

        # https://en.wikipedia.org/wiki/Soundex
        self.assertEqual(self.pa.encode('Robert'), 'R163')
        self.assertEqual(self.pa.encode('Rupert'), 'R163')
        self.assertEqual(self.pa.encode('Rubin'), 'R150')
        self.assertEqual(self.pa.encode('Tymczak'), 'T522')

        # https://en.wikipedia.org/wiki/Daitch%E2%80%93Mokotoff_Soundex
        self.assertEqual(self.pa.encode('Peters'), 'P362')
        self.assertEqual(self.pa.encode('Peterson'), 'P362')
        self.assertEqual(self.pa.encode('Moskowitz'), 'M232')
        self.assertEqual(self.pa.encode('Moskovitz'), 'M213')
        self.assertEqual(self.pa.encode('Auerbach'), 'A612')
        self.assertEqual(self.pa.encode('Uhrbach'), 'U612')
        self.assertEqual(self.pa.encode('Jackson'), 'J250')
        self.assertEqual(self.pa.encode('Jackson-Jackson'), 'J252')

        # max_length tests
        self.assertEqual(self.pa.encode('Lincoln', 10), 'L524500000')
        self.assertEqual(self.pa.encode('Lincoln', 5), 'L5245')
        self.assertEqual(self.pa.encode('Christopher', 6), 'C62316')

        # max_length bounds tests
        self.assertEqual(
            self.pa.encode('Niall', max_length=-1),
            'N4000000000000000000000000000000000000000000000000'
            + '00000000000000',
        )
        self.assertEqual(self.pa.encode('Niall', max_length=0), 'N400')

        # reverse tests
        self.assertEqual(self.pa.encode('Rubin', reverse=True), 'N160')
        self.assertEqual(self.pa.encode('Llyod', reverse=True), 'D400')
        self.assertEqual(self.pa.encode('Lincoln', reverse=True), 'N425')
        self.assertEqual(self.pa.encode('Knuth', reverse=True), 'H352')

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
        self.assertEqual(soundex('Euler'), 'E460')

    def test_soundex_special(self):
        """Test abydos.phonetic._soundex.soundex (special 1880-1910 variant method)."""  # noqa: E501
        self.assertEqual(self.pa.encode('Ashcroft', var='special'), 'A226')
        self.assertEqual(self.pa.encode('Asicroft', var='special'), 'A226')
        self.assertEqual(self.pa.encode('AsWcroft', var='special'), 'A226')
        self.assertEqual(self.pa.encode('Rupert', var='special'), 'R163')
        self.assertEqual(self.pa.encode('Rubin', var='special'), 'R150')

    def test_soundex_census(self):
        """Test abydos.phonetic._soundex.soundex (Census variant method)."""
        self.assertEqual(
            self.pa.encode('Vandeusen', var='Census'), ('V532', 'D250')
        )
        self.assertEqual(
            self.pa.encode('van Deusen', var='Census'), ('V532', 'D250')
        )
        self.assertEqual(self.pa.encode('McDonald', var='Census'), 'M235')
        self.assertEqual(
            self.pa.encode('la Cruz', var='Census'), ('L262', 'C620')
        )
        self.assertEqual(
            self.pa.encode('vanDamme', var='Census'), ('V535', 'D500')
        )


if __name__ == '__main__':
    unittest.main()
