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

"""abydos.tests.phonetic.test_phonetic_phonetic_spanish.

This module contains unit tests for abydos.phonetic.PhoneticSpanish
"""

import unittest

from abydos.phonetic import PhoneticSpanish, phonetic_spanish


class PhoneticSpanishTestCases(unittest.TestCase):
    """Test PhoneticSpanish functions.

    test cases for abydos.phonetic.PhoneticSpanish
    """

    pa = PhoneticSpanish()

    def test_phonetic_spanish(self):
        """Test abydos.phonetic.PhoneticSpanish."""
        # Base case
        self.assertEqual(self.pa.encode(''), '')

        # Examples given in
        self.assertEqual(self.pa.encode('Giraldo'), '8953')
        self.assertEqual(self.pa.encode('Jiraldo'), '8953')
        self.assertEqual(self.pa.encode('Halla'), '25')
        self.assertEqual(self.pa.encode('Haya'), '25')
        self.assertEqual(self.pa.encode('Cielo'), '45')
        self.assertEqual(self.pa.encode('Sielo'), '45')

        # Test to maximize coverage
        self.assertEqual(PhoneticSpanish(max_length=2).encode('Giraldo'), '89')

        # encode_alpha
        self.assertEqual(self.pa.encode_alpha('Giraldo'), 'GRLT')
        self.assertEqual(self.pa.encode_alpha('Jiraldo'), 'GRLT')
        self.assertEqual(self.pa.encode_alpha('Halla'), 'FL')
        self.assertEqual(self.pa.encode_alpha('Haya'), 'FL')
        self.assertEqual(self.pa.encode_alpha('Cielo'), 'SL')
        self.assertEqual(self.pa.encode_alpha('Sielo'), 'SL')

        # Test wrapper
        self.assertEqual(phonetic_spanish('Giraldo'), '8953')


if __name__ == '__main__':
    unittest.main()
