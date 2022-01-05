# Copyright 2014-2022 by Christopher C. Little.
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

"""abydos.tests.phonetic.test_phonetic_phonix.

This module contains unit tests for abydos.phonetic.Phonix
"""

import unittest

from abydos.phonetic import Phonix


class PhonixTestCases(unittest.TestCase):
    """Test Phonix functions.

    test cases for abydos.phonetic.Phonix
    """

    pa = Phonix()

    def test_phonix(self):
        """Test abydos.phonetic.Phonix."""
        self.assertEqual(self.pa.encode(''), '0000')

        # http://cpansearch.perl.org/src/MAROS/Text-Phonetic-2.05/t/007_phonix.t
        self.assertEqual(self.pa.encode('Müller'), 'M400')
        self.assertEqual(self.pa.encode('schneider'), 'S530')
        self.assertEqual(self.pa.encode('fischer'), 'F800')
        self.assertEqual(self.pa.encode('weber'), 'W100')
        self.assertEqual(self.pa.encode('meyer'), 'M000')
        self.assertEqual(self.pa.encode('wagner'), 'W250')
        self.assertEqual(self.pa.encode('schulz'), 'S480')
        self.assertEqual(self.pa.encode('becker'), 'B200')
        self.assertEqual(self.pa.encode('hoffmann'), 'H755')
        self.assertEqual(self.pa.encode('schäfer'), 'S700')
        self.assertEqual(self.pa.encode('schmidt'), 'S530')

        # http://cpansearch.perl.org/src/MAROS/Text-Phonetic-2.05/t/007_phonix.t:
        # testcases from Wais Module
        self.assertEqual(self.pa.encode('computer'), 'K513')
        self.assertEqual(self.pa.encode('computers'), 'K513')
        self.assertEqual(Phonix(5).encode('computers'), 'K5138')
        self.assertEqual(self.pa.encode('pfeifer'), 'F700')
        self.assertEqual(self.pa.encode('pfeiffer'), 'F700')
        self.assertEqual(self.pa.encode('knight'), 'N300')
        self.assertEqual(self.pa.encode('night'), 'N300')

        # http://cpansearch.perl.org/src/MAROS/Text-Phonetic-2.05/t/007_phonix.t:
        # testcases from
        # http://www.cl.uni-heidelberg.de/~bormann/documents/phono/
        # They use a sliglty different algorithm (first char is not included in
        # num code here)
        self.assertEqual(self.pa.encode('wait'), 'W300')
        self.assertEqual(self.pa.encode('weight'), 'W300')
        self.assertEqual(self.pa.encode('gnome'), 'N500')
        self.assertEqual(self.pa.encode('noam'), 'N500')
        self.assertEqual(self.pa.encode('rees'), 'R800')
        self.assertEqual(self.pa.encode('reece'), 'R800')
        self.assertEqual(self.pa.encode('yaeger'), 'v200')

        # http://books.google.com/books?id=xtWPI7Is9wIC&lpg=PA29&ots=DXhaL7ZkvK&dq=phonix%20gadd&pg=PA29#v=onepage&q=phonix%20gadd&f=false
        self.assertEqual(self.pa.encode('alam'), 'v450')
        self.assertEqual(self.pa.encode('berkpakaian'), 'B212')
        self.assertEqual(self.pa.encode('capaian'), 'K150')

        # http://books.google.com/books?id=LZrT6eWf9NMC&lpg=PA76&ots=Tex3FqNwGP&dq=%22phonix%20algorithm%22&pg=PA75#v=onepage&q=%22phonix%20algorithm%22&f=false
        self.assertEqual(self.pa.encode('peter'), 'P300')
        self.assertEqual(self.pa.encode('pete'), 'P300')
        self.assertEqual(self.pa.encode('pedro'), 'P360')
        self.assertEqual(self.pa.encode('stephen'), 'S375')
        self.assertEqual(self.pa.encode('steve'), 'S370')
        self.assertEqual(self.pa.encode('smith'), 'S530')
        self.assertEqual(self.pa.encode('smythe'), 'S530')
        self.assertEqual(self.pa.encode('gail'), 'G400')
        self.assertEqual(self.pa.encode('gayle'), 'G400')
        self.assertEqual(self.pa.encode('christine'), 'K683')
        self.assertEqual(self.pa.encode('christina'), 'K683')
        self.assertEqual(self.pa.encode('kristina'), 'K683')

        # max_length bounds tests
        self.assertEqual(
            Phonix(max_length=-1).encode('Niall'), f"N4{'0' * 62}"
        )
        self.assertEqual(Phonix(max_length=0).encode('Niall'), 'N400')

        # zero_pad tests
        self.assertEqual(
            Phonix(max_length=-1, zero_pad=False).encode('Niall'), 'N4'
        )
        self.assertEqual(
            Phonix(max_length=0, zero_pad=False).encode('Niall'), 'N4'
        )
        self.assertEqual(
            Phonix(max_length=0, zero_pad=True).encode('Niall'), 'N400'
        )
        self.assertEqual(Phonix(max_length=4, zero_pad=False).encode(''), '0')
        self.assertEqual(
            Phonix(max_length=4, zero_pad=True).encode(''), '0000'
        )

        # encode_alpha
        self.assertEqual(self.pa.encode_alpha('Müller'), 'ML')
        self.assertEqual(self.pa.encode_alpha('schneider'), 'SNT')
        self.assertEqual(self.pa.encode_alpha('fischer'), 'FS')
        self.assertEqual(self.pa.encode_alpha('weber'), 'WP')


if __name__ == '__main__':
    unittest.main()
