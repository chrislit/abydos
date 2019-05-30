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

"""abydos.tests.phonetic.test_phonetic_henry_early.

This module contains unit tests for abydos.phonetic.HenryEarly
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.phonetic import HenryEarly, henry_early


class HenryEarlyTestCases(unittest.TestCase):
    """Test early Henry Code functions.

    test cases for abydos.phonetic.HenryEarly
    """

    pa = HenryEarly()

    def test_henry_early(self):
        """Test abydos.phonetic.HenryEarly."""
        # Base case
        self.assertEqual(self.pa.encode(''), '')

        # Examples from Legare 1972 paper
        self.assertEqual(self.pa.encode('Descarry'), 'DKR')
        self.assertEqual(self.pa.encode('Descaries'), 'DKR')
        self.assertEqual(self.pa.encode('Campo'), 'KP')
        self.assertEqual(self.pa.encode('Campot'), 'KP')
        self.assertEqual(self.pa.encode('Gausselin'), 'GSL')
        self.assertEqual(self.pa.encode('Gosselin'), 'GSL')
        self.assertEqual(self.pa.encode('Bergeron'), 'BRJ')
        self.assertEqual(self.pa.encode('Bergereau'), 'BRJ')
        self.assertEqual(self.pa.encode('Bosseron'), 'BSR')
        self.assertEqual(self.pa.encode('Cicire'), 'SSR')
        self.assertEqual(self.pa.encode('Lechevalier'), 'LCV')
        self.assertEqual(self.pa.encode('Chevalier'), 'CVL')
        self.assertEqual(self.pa.encode('Peloy'), 'PL')
        self.assertEqual(self.pa.encode('Beloy'), 'BL')
        self.assertEqual(self.pa.encode('Beret'), 'BR')
        self.assertEqual(self.pa.encode('Benet'), 'BN')
        self.assertEqual(self.pa.encode('Turcot'), 'TRK')
        self.assertEqual(self.pa.encode('Turgot'), 'TRG')
        self.assertEqual(self.pa.encode('Vigier'), 'VJ')
        self.assertEqual(self.pa.encode('Vigiere'), 'VJR')
        self.assertEqual(self.pa.encode('Dodin'), 'DD')
        self.assertEqual(self.pa.encode('Dodelin'), 'DDL')

        # Tests to complete coverage
        self.assertEqual(self.pa.encode('Anil'), 'ANL')
        self.assertEqual(self.pa.encode('Emmanuel'), 'AMN')
        self.assertEqual(self.pa.encode('Ainu'), 'EN')
        self.assertEqual(self.pa.encode('Oeuf'), 'OF')
        self.assertEqual(self.pa.encode('Yves'), 'IV')
        self.assertEqual(self.pa.encode('Yo'), 'I')
        self.assertEqual(self.pa.encode('Umman'), 'EM')
        self.assertEqual(self.pa.encode('Omman'), 'OM')
        self.assertEqual(self.pa.encode('Zoe'), 'S')
        self.assertEqual(self.pa.encode('Beauchamp'), 'BCP')
        self.assertEqual(self.pa.encode('Chloe'), 'KL')
        self.assertEqual(self.pa.encode('Gerard'), 'JRR')
        self.assertEqual(self.pa.encode('Agnes'), 'ANN')
        self.assertEqual(self.pa.encode('Pinot'), 'PN')
        self.assertEqual(self.pa.encode('Philo'), 'FL')
        self.assertEqual(self.pa.encode('Quisling'), 'GL')
        self.assertEqual(self.pa.encode('Qualite'), 'KLT')
        self.assertEqual(self.pa.encode('Sainte-Marie'), 'XMR')
        self.assertEqual(self.pa.encode('Saint-Jean'), 'XJ')
        self.assertEqual(self.pa.encode('Ste-Marie'), 'XMR')
        self.assertEqual(self.pa.encode('St-Jean'), 'XJ')
        self.assertEqual(self.pa.encode('Cloe'), 'KL')
        self.assertEqual(self.pa.encode('Ahch-To'), 'AKT')
        self.assertEqual(self.pa.encode('Zdavros'), 'SDV')
        self.assertEqual(self.pa.encode('Sdavros'), 'DVR')
        self.assertEqual(self.pa.encode('Coulomb'), 'KLB')
        self.assertEqual(self.pa.encode('Calm'), 'K')
        self.assertEqual(self.pa.encode('Omnia'), 'ON')
        self.assertEqual(self.pa.encode('Ramps'), 'RPS')
        self.assertEqual(self.pa.encode('Renault'), 'RN')
        self.assertEqual(self.pa.encode('Czech'), 'CSK')
        self.assertEqual(self.pa.encode('Imran'), 'ER')
        self.assertEqual(
            HenryEarly(max_length=-1).encode('Christopher'), 'KRXF'
        )

        # Test wrapper
        self.assertEqual(henry_early('Gausselin'), 'GSL')


if __name__ == '__main__':
    unittest.main()
