# -*- coding: utf-8 -*-

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

"""abydos.tests.phonetic.test_phonetic_reth_schek.

This module contains unit tests for abydos.phonetic.RethSchek
"""

import unittest

from abydos.phonetic import RethSchek, reth_schek_phonetik


class RethSchekTestCases(unittest.TestCase):
    """Test Reth-Schek Phonetik functions.

    test cases for abydos.phonetic.RethSchek
    """

    pa = RethSchek()

    def test_reth_schek_phonetik(self):
        """Test abydos.phonetic.RethSchek."""
        # Base cases
        self.assertEqual(self.pa.encode(''), '')

        # equivalents
        self.assertEqual(self.pa.encode('Häschen'), self.pa.encode('Haeschen'))
        self.assertEqual(self.pa.encode('Schloß'), self.pa.encode('Schloss'))
        self.assertEqual(self.pa.encode('üben'), self.pa.encode('ueben'))
        self.assertEqual(
            self.pa.encode('Eichörnchen'), self.pa.encode('Eichoernchen')
        )

        self.assertEqual(self.pa.encode('Häschen'), 'HESCHEN')
        self.assertEqual(self.pa.encode('Eichörnchen'), 'AIGHOERNGHEN')
        self.assertEqual(self.pa.encode('Hexe'), 'HEXE')
        self.assertEqual(self.pa.encode('Chemie'), 'GHEMI')
        self.assertEqual(self.pa.encode('Brille'), 'BRILE')
        self.assertEqual(self.pa.encode('Brilleille'), 'BRILAILE')
        self.assertEqual(self.pa.encode('Niveau'), 'NIFEAU')
        self.assertEqual(self.pa.encode('Korb'), 'GORB')
        self.assertEqual(self.pa.encode('Heino'), 'HAINO')
        self.assertEqual(self.pa.encode('Nekka'), 'NEKA')
        self.assertEqual(self.pa.encode('Aleph'), 'ALEF')
        self.assertEqual(self.pa.encode('Aleppo'), 'ALEBO')
        self.assertEqual(self.pa.encode('Endzipfel'), 'ENDZIBFL')
        self.assertEqual(self.pa.encode('verbrandt'), 'FERBRAND')
        self.assertEqual(self.pa.encode('Cent'), 'GEND')
        self.assertEqual(self.pa.encode('addiscendae'), 'ADISGENDE')
        self.assertEqual(self.pa.encode('kickx'), 'GIGX')
        self.assertEqual(self.pa.encode('sanctionen'), 'SANGDIONEN')
        self.assertEqual(self.pa.encode('Kuh'), 'GU')
        self.assertEqual(self.pa.encode('lecker'), 'LEGR')
        self.assertEqual(self.pa.encode('rödlich'), 'ROEDLIG')

        # Test wrapper
        self.assertEqual(reth_schek_phonetik('Häschen'), 'HESCHEN')


if __name__ == '__main__':
    unittest.main()
