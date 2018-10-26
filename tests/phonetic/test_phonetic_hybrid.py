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

"""abydos.tests.phonetic.test_phonetic_hybrid.

This module contains unit tests for abydos.phonetic.hybrid
"""

from __future__ import unicode_literals

import unittest

from abydos.phonetic.hybrid import metasoundex, onca


class ONCATestCases(unittest.TestCase):
    """Test ONCA functions.

    test cases for abydos.phonetic.hybrid.onca
    """

    def test_onca(self):
        """Test abydos.phonetic.hybrid.onca."""
        # https://nces.ed.gov/FCSM/pdf/RLT97.pdf
        self.assertEqual(onca('HALL'), 'H400')
        self.assertEqual(onca('SMITH'), 'S530')

        # http://nchod.uhce.ox.ac.uk/NCHOD%20Oxford%20E5%20Report%201st%20Feb_VerAM2.pdf
        self.assertEqual(onca('HAWTON'), 'H350')
        self.assertEqual(onca('HORTON'), 'H635')
        self.assertEqual(onca('HOUGHTON'), 'H235')


class MetaSoundexTestCases(unittest.TestCase):
    """Test MetaSoundex functions.

    test cases for abydos.phonetic.hybrid.metasoundex
    """

    def test_metasoundex(self):
        """Test abydos.phonetic.hybrid.metasoundex."""
        # Base cases
        self.assertEqual(metasoundex(''), '0000')
        self.assertEqual(metasoundex('', lang='en'), '0000')
        self.assertEqual(metasoundex('', lang='es'), '')

        # Top 10 Anglo surnames in US
        self.assertEqual(metasoundex('Smith', lang='en'), '4500')
        self.assertEqual(metasoundex('Johnson', lang='en'), '1525')
        self.assertEqual(metasoundex('Williams', lang='en'), '7452')
        self.assertEqual(metasoundex('Brown', lang='en'), '7650')
        self.assertEqual(metasoundex('Jones', lang='en'), '1520')
        self.assertEqual(metasoundex('Miller', lang='en'), '6460')
        self.assertEqual(metasoundex('Davis', lang='en'), '3120')
        self.assertEqual(metasoundex('Wilson', lang='en'), '7425')
        self.assertEqual(metasoundex('Anderson', lang='en'), '0536')
        self.assertEqual(metasoundex('Thomas', lang='en'), '6200')

        self.assertEqual(metasoundex('Smith', lang='es'), '4632')
        self.assertEqual(metasoundex('Johnson', lang='es'), '82646')
        self.assertEqual(metasoundex('Williams', lang='es'), '564')
        self.assertEqual(metasoundex('Brown', lang='es'), '196')
        self.assertEqual(metasoundex('Jones', lang='es'), '864')
        self.assertEqual(metasoundex('Miller', lang='es'), '659')
        self.assertEqual(metasoundex('Davis', lang='es'), '314')
        self.assertEqual(metasoundex('Wilson', lang='es'), '546')
        self.assertEqual(metasoundex('Anderson', lang='es'), '63946')
        self.assertEqual(metasoundex('Thomas', lang='es'), '364')

        # Top 10 Mexican surnames
        self.assertEqual(metasoundex('Hernández', lang='en'), '5653')
        self.assertEqual(metasoundex('García', lang='en'), '5620')
        self.assertEqual(metasoundex('Lòpez', lang='en'), '8120')
        self.assertEqual(metasoundex('Martìnez', lang='en'), '6635')
        self.assertEqual(metasoundex('Rodrìguez', lang='en'), '9362')
        self.assertEqual(metasoundex('González', lang='en'), '5524')
        self.assertEqual(metasoundex('Pérez', lang='en'), '7620')
        self.assertEqual(metasoundex('Sánchez', lang='en'), '4520')
        self.assertEqual(metasoundex('Gómez', lang='en'), '5520')
        self.assertEqual(metasoundex('Flores', lang='en'), '7462')

        self.assertEqual(metasoundex('Hernández', lang='es'), '96634')
        self.assertEqual(metasoundex('García', lang='es'), '894')
        self.assertEqual(metasoundex('Lòpez', lang='es'), '504')
        self.assertEqual(metasoundex('Martìnez', lang='es'), '69364')
        self.assertEqual(metasoundex('Rodrìguez', lang='es'), '93984')
        self.assertEqual(metasoundex('González', lang='es'), '86454')
        self.assertEqual(metasoundex('Pérez', lang='es'), '094')
        self.assertEqual(metasoundex('Sánchez', lang='es'), '4644')
        self.assertEqual(metasoundex('Gómez', lang='es'), '864')
        self.assertEqual(metasoundex('Flores', lang='es'), '2594')


if __name__ == '__main__':
    unittest.main()
