# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

"""abydos.tests.phonetic.test_phonetic_pt.

This module contains unit tests for abydos.phonetic.pt
"""

from __future__ import unicode_literals

import unittest

from abydos.phonetic.pt import soundex_br


class SoundexBRTestCases(unittest.TestCase):
    """Test SoundexBR functions.

    test cases for abydos.phonetic.pt.soundex_br
    """

    def test_soundex_br(self):
        """Test abydos.phonetic.pt.soundex_br."""
        # Base case
        self.assertEqual(soundex_br(''), '0000')

        # Examples given at https://github.com/danielmarcelino/SoundexBR
        self.assertEqual(soundex_br('Ana Karolina Kuhnen'), 'A526')
        self.assertEqual(soundex_br('Ana Carolina Kuhnen'), 'A526')
        self.assertEqual(soundex_br('Ana Karolina'), 'A526')
        self.assertEqual(soundex_br('João Souza'), 'J220')
        self.assertEqual(soundex_br('Dilma Vana Rousseff'), 'D451')
        self.assertEqual(soundex_br('Dilma Rousef'), 'D456')
        self.assertEqual(soundex_br('Aécio Neves'), 'A251')
        self.assertEqual(soundex_br('Aecio Neves'), 'A251')
        self.assertEqual(soundex_br('HILBERT'), 'I416')
        self.assertEqual(soundex_br('Heilbronn'), 'E416')
        self.assertEqual(soundex_br('Gauss'), 'G200')
        self.assertEqual(soundex_br('Kant'), 'C530')

        # Tests to complete coverage
        self.assertEqual(soundex_br('Wasser'), 'V260')
        self.assertEqual(soundex_br('Cici'), 'S200')
        self.assertEqual(soundex_br('Gerard'), 'J663')
        self.assertEqual(soundex_br('Yglesias'), 'I242')
        self.assertEqual(soundex_br('Cici', zero_pad=False), 'S2')


if __name__ == '__main__':
    unittest.main()
