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

"""abydos.tests.phonetic.test_phonetic_phonex.

This module contains unit tests for abydos.phonetic.Phonex
"""

import unittest

from abydos.phonetic import Phonex, phonex


class PhonexTestCases(unittest.TestCase):
    """Test Phonex functions.

    test cases for abydos.phonetic.Phonex
    """

    pa = Phonex()

    def test_phonex(self):
        """Test abydos.phonetic.Phonex."""
        self.assertEqual(self.pa.encode(''), '0000')

        # http://homepages.cs.ncl.ac.uk/brian.randell/Genealogy/NameMatching.pdf
        self.assertEqual(self.pa.encode('Ewell'), 'A400')
        self.assertEqual(self.pa.encode('Filp'), 'F100')
        self.assertEqual(self.pa.encode('Heames'), 'A500')
        self.assertEqual(self.pa.encode('Kneves'), 'N100')
        self.assertEqual(self.pa.encode('River'), 'R160')
        self.assertEqual(self.pa.encode('Corley'), 'C400')
        self.assertEqual(self.pa.encode('Carton'), 'C350')
        self.assertEqual(self.pa.encode('Cachpole'), 'C214')

        self.assertEqual(self.pa.encode('Ewell'), self.pa.encode('Ule'))
        self.assertEqual(self.pa.encode('Filp'), self.pa.encode('Philp'))
        self.assertEqual(self.pa.encode('Yule'), self.pa.encode('Ewell'))
        self.assertEqual(self.pa.encode('Heames'), self.pa.encode('Eames'))
        self.assertEqual(self.pa.encode('Kneves'), self.pa.encode('Neves'))
        self.assertEqual(self.pa.encode('River'), self.pa.encode('Rivers'))
        self.assertEqual(self.pa.encode('Corley'), self.pa.encode('Coley'))
        self.assertEqual(self.pa.encode('Carton'), self.pa.encode('Carlton'))
        self.assertEqual(
            self.pa.encode('Cachpole'), self.pa.encode('Catchpole')
        )

        # etc. (for code coverage)
        self.assertEqual(self.pa.encode('Saxon'), 'S250')
        self.assertEqual(self.pa.encode('Wright'), 'R230')
        self.assertEqual(self.pa.encode('Ai'), 'A000')
        self.assertEqual(self.pa.encode('Barth'), 'B300')
        self.assertEqual(self.pa.encode('Perry'), 'B600')
        self.assertEqual(self.pa.encode('Garth'), 'G300')
        self.assertEqual(self.pa.encode('Jerry'), 'G600')
        self.assertEqual(self.pa.encode('Gerry'), 'G600')
        self.assertEqual(self.pa.encode('Camden'), 'C500')
        self.assertEqual(self.pa.encode('Ganges'), 'G500')
        self.assertEqual(self.pa.encode('A-1'), 'A000')

        # max_length bounds tests
        self.assertEqual(
            Phonex(max_length=-1).encode('Niall'),
            'N400000000000000000000000000000000000000000000000000000000000000',
        )
        self.assertEqual(Phonex(max_length=0).encode('Niall'), 'N400')

        # zero_pad tests
        self.assertEqual(
            Phonex(max_length=0, zero_pad=False).encode('Niall'), 'N4'
        )
        self.assertEqual(
            Phonex(max_length=0, zero_pad=True).encode('Niall'), 'N400'
        )
        self.assertEqual(Phonex(max_length=4, zero_pad=False).encode(''), '0')
        self.assertEqual(
            Phonex(max_length=4, zero_pad=True).encode(''), '0000'
        )

        # encode_alpha
        self.assertEqual(self.pa.encode_alpha('Ewell'), 'AL')
        self.assertEqual(self.pa.encode_alpha('Filp'), 'FP')
        self.assertEqual(self.pa.encode_alpha('Heames'), 'AN')
        self.assertEqual(self.pa.encode_alpha('Kneves'), 'NP')

        # Test wrapper
        self.assertEqual(phonex('Ewell'), 'A400')


if __name__ == '__main__':
    unittest.main()
