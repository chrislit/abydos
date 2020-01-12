# Copyright 2018-2020 by Christopher C. Little.
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

"""abydos.tests.phonetic.test_phonetic_soundex_br.

This module contains unit tests for abydos.phonetic.SoundexBR
"""

import unittest

from abydos.phonetic import SoundexBR


class SoundexBRTestCases(unittest.TestCase):
    """Test SoundexBR functions.

    test cases for abydos.phonetic.SoundexBR
    """

    pa = SoundexBR()

    def test_soundex_br(self):
        """Test abydos.phonetic.SoundexBR."""
        # Base case
        self.assertEqual(self.pa.encode(''), '0000')

        # Examples given at https://github.com/danielmarcelino/SoundexBR
        self.assertEqual(self.pa.encode('Ana Karolina Kuhnen'), 'A526')
        self.assertEqual(self.pa.encode('Ana Carolina Kuhnen'), 'A526')
        self.assertEqual(self.pa.encode('Ana Karolina'), 'A526')
        self.assertEqual(self.pa.encode('João Souza'), 'J220')
        self.assertEqual(self.pa.encode('Dilma Vana Rousseff'), 'D451')
        self.assertEqual(self.pa.encode('Dilma Rousef'), 'D456')
        self.assertEqual(self.pa.encode('Aécio Neves'), 'A251')
        self.assertEqual(self.pa.encode('Aecio Neves'), 'A251')
        self.assertEqual(self.pa.encode('HILBERT'), 'I416')
        self.assertEqual(self.pa.encode('Heilbronn'), 'E416')
        self.assertEqual(self.pa.encode('Gauss'), 'G200')
        self.assertEqual(self.pa.encode('Kant'), 'C530')

        # Tests to complete coverage
        self.assertEqual(self.pa.encode('Wasser'), 'V260')
        self.assertEqual(self.pa.encode('Cici'), 'S200')
        self.assertEqual(self.pa.encode('Gerard'), 'J663')
        self.assertEqual(self.pa.encode('Yglesias'), 'I242')
        self.assertEqual(SoundexBR(zero_pad=False).encode('Cici'), 'S2')

        # encode_alpha
        self.assertEqual(self.pa.encode_alpha('Aecio Neves'), 'AKNP')
        self.assertEqual(self.pa.encode_alpha('HILBERT'), 'ILPR')
        self.assertEqual(self.pa.encode_alpha('Heilbronn'), 'ELPR')
        self.assertEqual(self.pa.encode_alpha('Gauss'), 'GK')


if __name__ == '__main__':
    unittest.main()
