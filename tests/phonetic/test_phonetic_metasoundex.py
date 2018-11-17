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

"""abydos.tests.phonetic.test_phonetic_metasoundex.

This module contains unit tests for abydos.phonetic.MetaSoundex
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.phonetic import MetaSoundex, metasoundex


class MetaSoundexTestCases(unittest.TestCase):
    """Test MetaSoundex functions.

    test cases for abydos.phonetic.MetaSoundex
    """

    pa = MetaSoundex()

    def test_metasoundex(self):
        """Test abydos.phonetic.MetaSoundex."""
        # Base cases
        self.assertEqual(self.pa.encode(''), '0000')
        self.assertEqual(self.pa.encode('', lang='en'), '0000')
        self.assertEqual(self.pa.encode('', lang='es'), '')

        # Top 10 Anglo surnames in US
        self.assertEqual(self.pa.encode('Smith', lang='en'), '4500')
        self.assertEqual(self.pa.encode('Johnson', lang='en'), '1525')
        self.assertEqual(self.pa.encode('Williams', lang='en'), '7452')
        self.assertEqual(self.pa.encode('Brown', lang='en'), '7650')
        self.assertEqual(self.pa.encode('Jones', lang='en'), '1520')
        self.assertEqual(self.pa.encode('Miller', lang='en'), '6460')
        self.assertEqual(self.pa.encode('Davis', lang='en'), '3120')
        self.assertEqual(self.pa.encode('Wilson', lang='en'), '7425')
        self.assertEqual(self.pa.encode('Anderson', lang='en'), '0536')
        self.assertEqual(self.pa.encode('Thomas', lang='en'), '6200')

        self.assertEqual(self.pa.encode('Smith', lang='es'), '4632')
        self.assertEqual(self.pa.encode('Johnson', lang='es'), '82646')
        self.assertEqual(self.pa.encode('Williams', lang='es'), '564')
        self.assertEqual(self.pa.encode('Brown', lang='es'), '196')
        self.assertEqual(self.pa.encode('Jones', lang='es'), '864')
        self.assertEqual(self.pa.encode('Miller', lang='es'), '659')
        self.assertEqual(self.pa.encode('Davis', lang='es'), '314')
        self.assertEqual(self.pa.encode('Wilson', lang='es'), '546')
        self.assertEqual(self.pa.encode('Anderson', lang='es'), '63946')
        self.assertEqual(self.pa.encode('Thomas', lang='es'), '364')

        # Top 10 Mexican surnames
        self.assertEqual(self.pa.encode('Hernández', lang='en'), '5653')
        self.assertEqual(self.pa.encode('García', lang='en'), '5620')
        self.assertEqual(self.pa.encode('Lòpez', lang='en'), '8120')
        self.assertEqual(self.pa.encode('Martìnez', lang='en'), '6635')
        self.assertEqual(self.pa.encode('Rodrìguez', lang='en'), '9362')
        self.assertEqual(self.pa.encode('González', lang='en'), '5524')
        self.assertEqual(self.pa.encode('Pérez', lang='en'), '7620')
        self.assertEqual(self.pa.encode('Sánchez', lang='en'), '4520')
        self.assertEqual(self.pa.encode('Gómez', lang='en'), '5520')
        self.assertEqual(self.pa.encode('Flores', lang='en'), '7462')

        self.assertEqual(self.pa.encode('Hernández', lang='es'), '96634')
        self.assertEqual(self.pa.encode('García', lang='es'), '894')
        self.assertEqual(self.pa.encode('Lòpez', lang='es'), '504')
        self.assertEqual(self.pa.encode('Martìnez', lang='es'), '69364')
        self.assertEqual(self.pa.encode('Rodrìguez', lang='es'), '93984')
        self.assertEqual(self.pa.encode('González', lang='es'), '86454')
        self.assertEqual(self.pa.encode('Pérez', lang='es'), '094')
        self.assertEqual(self.pa.encode('Sánchez', lang='es'), '4644')
        self.assertEqual(self.pa.encode('Gómez', lang='es'), '864')
        self.assertEqual(self.pa.encode('Flores', lang='es'), '2594')

        # Test wrapper
        self.assertEqual(metasoundex('Smith', lang='en'), '4500')
        self.assertEqual(metasoundex('Hernández', lang='es'), '96634')


if __name__ == '__main__':
    unittest.main()
