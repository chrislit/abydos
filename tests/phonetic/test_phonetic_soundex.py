# Copyright 2014-2020 by Christopher C. Little.
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

import unittest

from abydos.phonetic import Soundex


class SoundexTestCases(unittest.TestCase):
    """Test Soundex functions.

    test cases for abydos.phonetic.Soundex
    """

    pa = Soundex()

    def test_soundex(self):
        """Test abydos.phonetic.Soundex."""
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
        self.assertEqual(Soundex(10).encode('Lincoln'), 'L524500000')
        self.assertEqual(Soundex(5).encode('Lincoln'), 'L5245')
        self.assertEqual(Soundex(6).encode('Christopher'), 'C62316')

        # max_length bounds tests
        self.assertEqual(
            Soundex(max_length=-1).encode('Niall'),
            'N4000000000000000000000000000000000000000000000000'
            + '00000000000000',
        )
        self.assertEqual(Soundex(max_length=0).encode('Niall'), 'N400')

        # reverse tests
        self.assertEqual(Soundex(reverse=True).encode('Rubin'), 'N160')
        self.assertEqual(Soundex(reverse=True).encode('Llyod'), 'D400')
        self.assertEqual(Soundex(reverse=True).encode('Lincoln'), 'N425')
        self.assertEqual(Soundex(reverse=True).encode('Knuth'), 'H352')

        # zero_pad tests
        self.assertEqual(
            Soundex(max_length=-1, zero_pad=False).encode('Niall'), 'N4'
        )
        self.assertEqual(
            Soundex(max_length=0, zero_pad=False).encode('Niall'), 'N4'
        )
        self.assertEqual(
            Soundex(max_length=0, zero_pad=True).encode('Niall'), 'N400'
        )
        self.assertEqual(Soundex(max_length=4, zero_pad=False).encode(''), '0')
        self.assertEqual(
            Soundex(max_length=4, zero_pad=True).encode(''), '0000'
        )

        # encode_alpha
        self.assertEqual(self.pa.encode_alpha('Euler'), 'ELR')
        self.assertEqual(self.pa.encode_alpha('Gauss'), 'GK')
        self.assertEqual(self.pa.encode_alpha('Hilbert'), 'HLPR')
        self.assertEqual(self.pa.encode_alpha('Knuth'), 'KNT')

    def test_soundex_special(self):
        """Test abydos.phonetic.Soundex (special 1880-1910 variant method)."""
        pa_special = Soundex(var='special')
        self.assertEqual(pa_special.encode('Ashcroft'), 'A226')
        self.assertEqual(pa_special.encode('Asicroft'), 'A226')
        self.assertEqual(pa_special.encode('AsWcroft'), 'A226')
        self.assertEqual(pa_special.encode('Rupert'), 'R163')
        self.assertEqual(pa_special.encode('Rubin'), 'R150')

    def test_soundex_census(self):
        """Test abydos.phonetic.Soundex(Census variant method)."""
        pa_census = Soundex(var='Census')
        self.assertEqual(pa_census.encode('Vandeusen'), ('V532', 'D250'))
        self.assertEqual(pa_census.encode('van Deusen'), ('V532', 'D250'))
        self.assertEqual(pa_census.encode('McDonald'), 'M235')
        self.assertEqual(pa_census.encode('la Cruz'), ('L262', 'C620'))
        self.assertEqual(pa_census.encode('vanDamme'), ('V535', 'D500'))


if __name__ == '__main__':
    unittest.main()
