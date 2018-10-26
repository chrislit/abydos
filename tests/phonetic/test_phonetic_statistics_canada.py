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

"""abydos.tests.phonetic.test_phonetic_statistics_canada.

This module contains unit tests for abydos.phonetic.statistics_canada
"""

from __future__ import unicode_literals

import unittest

from abydos.phonetic.statistics_canada import statistics_canada


class StatisticsCanadaTestCases(unittest.TestCase):
    """Test Statistics Canada functions.

    test cases for abydos.phonetic.statistics_canada.statistics_canada
    """

    def test_statistics_canada(self):
        """Test abydos.phonetic.statistics_canada.statistics_canada."""
        self.assertEqual(statistics_canada(''), '')

        # https://naldc.nal.usda.gov/download/27833/PDF
        self.assertEqual(statistics_canada('Daves'), 'DVS')
        self.assertEqual(statistics_canada('Davies'), 'DVS')
        self.assertEqual(statistics_canada('Devese'), 'DVS')
        self.assertEqual(statistics_canada('Devies'), 'DVS')
        self.assertEqual(statistics_canada('Devos'), 'DVS')

        self.assertEqual(statistics_canada('Smathers'), 'SMTH')
        self.assertEqual(statistics_canada('Smithart'), 'SMTH')
        self.assertEqual(statistics_canada('Smithbower'), 'SMTH')
        self.assertEqual(statistics_canada('Smitherman'), 'SMTH')
        self.assertEqual(statistics_canada('Smithey'), 'SMTH')
        self.assertEqual(statistics_canada('Smithgall'), 'SMTH')
        self.assertEqual(statistics_canada('Smithingall'), 'SMTH')
        self.assertEqual(statistics_canada('Smithmyer'), 'SMTH')
        self.assertEqual(statistics_canada('Smithpeter'), 'SMTH')
        self.assertEqual(statistics_canada('Smithson'), 'SMTH')
        self.assertEqual(statistics_canada('Smithy'), 'SMTH')
        self.assertEqual(statistics_canada('Smotherman'), 'SMTH')
        self.assertEqual(statistics_canada('Smothers'), 'SMTH')
        self.assertEqual(statistics_canada('Smyth'), 'SMTH')

        # Additional tests from @Yomguithereal's talisman
        # https://github.com/Yomguithereal/talisman/blob/master/test/phonetics/statcan.js
        self.assertEqual(statistics_canada('Guillaume'), 'GLM')
        self.assertEqual(statistics_canada('Arlène'), 'ARLN')
        self.assertEqual(statistics_canada('Lüdenscheidt'), 'LDNS')


if __name__ == '__main__':
    unittest.main()
