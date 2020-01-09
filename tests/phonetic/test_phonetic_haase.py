# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

"""abydos.tests.phonetic.test_phonetic_haase.

This module contains unit tests for abydos.phonetic.Haase
"""

import unittest

from abydos.phonetic import Haase, haase_phonetik


class HaaseTestCases(unittest.TestCase):
    """Test Haase Phonetik functions.

    test cases for abydos.phonetic.Haase
    """

    pa = Haase()

    def test_haase_phonetik(self):
        """Test abydos.phonetic.Haase."""
        # Base cases
        self.assertEqual(self.pa.encode(''), ('',))

        # equivalents
        self.assertEqual(self.pa.encode('Häschen'), self.pa.encode('Haeschen'))
        self.assertEqual(self.pa.encode('Schloß'), self.pa.encode('Schloss'))
        self.assertEqual(self.pa.encode('üben'), self.pa.encode('ueben'))
        self.assertEqual(
            self.pa.encode('Eichörnchen'), self.pa.encode('Eichoernchen')
        )

        # coverage completion
        self.assertEqual(self.pa.encode('Häschen'), ('9896', '9496'))
        self.assertEqual(Haase(primary_only=True).encode('Häschen'), ('9896',))
        self.assertEqual(self.pa.encode('Eichörnchen'), ('94976496',))
        self.assertEqual(self.pa.encode('Hexe'), ('9489',))
        self.assertEqual(self.pa.encode('Chemie'), ('4969', '8969'))

        self.assertEqual(self.pa.encode('Brille'), ('17959', '179'))
        self.assertEqual(
            self.pa.encode('Brilleille'), ('1795959', '17959', '179')
        )
        self.assertEqual(self.pa.encode('Niveau'), ('6939',))
        self.assertEqual(self.pa.encode('Korb'), ('4971', '4973'))
        self.assertEqual(self.pa.encode('Heino'), ('969', '9693'))
        self.assertEqual(self.pa.encode('Nekka'), ('6949', '69497'))
        self.assertEqual(self.pa.encode('Aleph'), ('9593',))
        self.assertEqual(self.pa.encode('Aleppo'), ('95919', '959193'))
        self.assertEqual(self.pa.encode('Endzipfel'), ('96891395',))
        self.assertEqual(self.pa.encode('verbrandt'), ('39717962', '39737962'))
        self.assertEqual(self.pa.encode('Cent'), ('8962',))
        self.assertEqual(self.pa.encode('addiscendae'), ('92989629',))
        self.assertEqual(self.pa.encode('kickx'), ('4948',))
        self.assertEqual(self.pa.encode('sanctionen'), ('896829696',))

        # encode_alpha
        self.assertEqual(self.pa.encode_alpha('Niveau'), ('NAFA',))
        self.assertEqual(self.pa.encode_alpha('Korb'), ('KARP', 'KARF'))
        self.assertEqual(self.pa.encode_alpha('Heino'), ('ANA', 'ANAF'))
        self.assertEqual(self.pa.encode_alpha('Nekka'), ('NAKA', 'NAKAR'))

        # Test wrapper
        self.assertEqual(haase_phonetik('Häschen'), ('9896', '9496'))


if __name__ == '__main__':
    unittest.main()
