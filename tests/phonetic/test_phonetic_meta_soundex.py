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

"""abydos.tests.phonetic.test_phonetic_meta_soundex.

This module contains unit tests for abydos.phonetic.MetaSoundex
"""

import unittest

from abydos.phonetic import MetaSoundex, metasoundex


class MetaSoundexTestCases(unittest.TestCase):
    """Test MetaSoundex functions.

    test cases for abydos.phonetic.MetaSoundex
    """

    pa = MetaSoundex()
    pa_en = MetaSoundex(lang='en')
    pa_es = MetaSoundex(lang='es')

    def test_meta_soundex(self):
        """Test abydos.phonetic.MetaSoundex."""
        # Base cases
        self.assertEqual(self.pa.encode(''), '0000')
        self.assertEqual(self.pa_en.encode(''), '0000')
        self.assertEqual(self.pa_es.encode(''), '')

        # Top 10 Anglo surnames in US
        self.assertEqual(self.pa_en.encode('Smith'), '4500')
        self.assertEqual(self.pa_en.encode('Johnson'), '1525')
        self.assertEqual(self.pa_en.encode('Williams'), '7452')
        self.assertEqual(self.pa_en.encode('Brown'), '7650')
        self.assertEqual(self.pa_en.encode('Jones'), '1520')
        self.assertEqual(self.pa_en.encode('Miller'), '6460')
        self.assertEqual(self.pa_en.encode('Davis'), '3120')
        self.assertEqual(self.pa_en.encode('Wilson'), '7425')
        self.assertEqual(self.pa_en.encode('Anderson'), '0536')
        self.assertEqual(self.pa_en.encode('Thomas'), '6200')

        self.assertEqual(self.pa_es.encode('Smith'), '4632')
        self.assertEqual(self.pa_es.encode('Johnson'), '82646')
        self.assertEqual(self.pa_es.encode('Williams'), '564')
        self.assertEqual(self.pa_es.encode('Brown'), '196')
        self.assertEqual(self.pa_es.encode('Jones'), '864')
        self.assertEqual(self.pa_es.encode('Miller'), '659')
        self.assertEqual(self.pa_es.encode('Davis'), '314')
        self.assertEqual(self.pa_es.encode('Wilson'), '546')
        self.assertEqual(self.pa_es.encode('Anderson'), '63946')
        self.assertEqual(self.pa_es.encode('Thomas'), '364')

        # Top 10 Mexican surnames
        self.assertEqual(self.pa_en.encode('Hernández'), '5653')
        self.assertEqual(self.pa_en.encode('García'), '5620')
        self.assertEqual(self.pa_en.encode('Lòpez'), '8120')
        self.assertEqual(self.pa_en.encode('Martìnez'), '6635')
        self.assertEqual(self.pa_en.encode('Rodrìguez'), '9362')
        self.assertEqual(self.pa_en.encode('González'), '5524')
        self.assertEqual(self.pa_en.encode('Pérez'), '7620')
        self.assertEqual(self.pa_en.encode('Sánchez'), '4520')
        self.assertEqual(self.pa_en.encode('Gómez'), '5520')
        self.assertEqual(self.pa_en.encode('Flores'), '7462')

        self.assertEqual(self.pa_es.encode('Hernández'), '96634')
        self.assertEqual(self.pa_es.encode('García'), '894')
        self.assertEqual(self.pa_es.encode('Lòpez'), '504')
        self.assertEqual(self.pa_es.encode('Martìnez'), '69364')
        self.assertEqual(self.pa_es.encode('Rodrìguez'), '93984')
        self.assertEqual(self.pa_es.encode('González'), '86454')
        self.assertEqual(self.pa_es.encode('Pérez'), '094')
        self.assertEqual(self.pa_es.encode('Sánchez'), '4644')
        self.assertEqual(self.pa_es.encode('Gómez'), '864')
        self.assertEqual(self.pa_es.encode('Flores'), '2594')

        # encode_alpha
        self.assertEqual(self.pa_en.encode_alpha('Smith'), 'SN')
        self.assertEqual(self.pa_en.encode_alpha('Johnson'), 'JNKN')
        self.assertEqual(self.pa_es.encode_alpha('Hernández'), 'RNNTS')
        self.assertEqual(self.pa_es.encode_alpha('García'), 'GRS')

        # Test wrapper
        self.assertEqual(metasoundex('Smith', lang='en'), '4500')
        self.assertEqual(metasoundex('Hernández', lang='es'), '96634')


if __name__ == '__main__':
    unittest.main()
