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

"""abydos.tests.phonetic.test_phonetic_statistics_canada.

This module contains unit tests for abydos.phonetic.StatisticsCanada
"""

import unittest

from abydos.phonetic import StatisticsCanada, statistics_canada


class StatisticsCanadaTestCases(unittest.TestCase):
    """Test Statistics Canada functions.

    test cases for abydos.phonetic.StatisticsCanada
    """

    pa = StatisticsCanada()

    def test_statistics_canada(self):
        """Test abydos.phonetic.StatisticsCanada."""
        self.assertEqual(self.pa.encode(''), '')

        # https://naldc.nal.usda.gov/download/27833/PDF
        self.assertEqual(self.pa.encode('Daves'), 'DVS')
        self.assertEqual(self.pa.encode('Davies'), 'DVS')
        self.assertEqual(self.pa.encode('Devese'), 'DVS')
        self.assertEqual(self.pa.encode('Devies'), 'DVS')
        self.assertEqual(self.pa.encode('Devos'), 'DVS')

        self.assertEqual(self.pa.encode('Smathers'), 'SMTH')
        self.assertEqual(self.pa.encode('Smithart'), 'SMTH')
        self.assertEqual(self.pa.encode('Smithbower'), 'SMTH')
        self.assertEqual(self.pa.encode('Smitherman'), 'SMTH')
        self.assertEqual(self.pa.encode('Smithey'), 'SMTH')
        self.assertEqual(self.pa.encode('Smithgall'), 'SMTH')
        self.assertEqual(self.pa.encode('Smithingall'), 'SMTH')
        self.assertEqual(self.pa.encode('Smithmyer'), 'SMTH')
        self.assertEqual(self.pa.encode('Smithpeter'), 'SMTH')
        self.assertEqual(self.pa.encode('Smithson'), 'SMTH')
        self.assertEqual(self.pa.encode('Smithy'), 'SMTH')
        self.assertEqual(self.pa.encode('Smotherman'), 'SMTH')
        self.assertEqual(self.pa.encode('Smothers'), 'SMTH')
        self.assertEqual(self.pa.encode('Smyth'), 'SMTH')

        # Additional tests from @Yomguithereal's talisman
        # https://github.com/Yomguithereal/talisman/blob/master/test/phonetics/statcan.js
        self.assertEqual(self.pa.encode('Guillaume'), 'GLM')
        self.assertEqual(self.pa.encode('Arlène'), 'ARLN')
        self.assertEqual(self.pa.encode('Lüdenscheidt'), 'LDNS')

        # Test wrapper
        self.assertEqual(statistics_canada('Daves'), 'DVS')


if __name__ == '__main__':
    unittest.main()
