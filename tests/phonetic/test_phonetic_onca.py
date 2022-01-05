# Copyright 2018-2022 by Christopher C. Little.
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

"""abydos.tests.phonetic.test_phonetic_ONCA.

This module contains unit tests for abydos.phonetic.ONCA
"""

import unittest

from abydos.phonetic import ONCA


class ONCATestCases(unittest.TestCase):
    """Test ONCA functions.

    test cases for abydos.phonetic.ONCA
    """

    pa = ONCA()

    def test_onca(self):
        """Test abydos.phonetic.ONCA."""
        # https://nces.ed.gov/FCSM/pdf/RLT97.pdf
        self.assertEqual(self.pa.encode('HALL'), 'H400')
        self.assertEqual(self.pa.encode('SMITH'), 'S530')

        # http://nchod.uhce.ox.ac.uk/NCHOD%20Oxford%20E5%20Report%201st%20Feb_VerAM2.pdf
        self.assertEqual(self.pa.encode('HAWTON'), 'H350')
        self.assertEqual(self.pa.encode('HORTON'), 'H635')
        self.assertEqual(self.pa.encode('HOUGHTON'), 'H235')

        # encode_alpha
        self.assertEqual(self.pa.encode_alpha('HALL'), 'HL')
        self.assertEqual(self.pa.encode_alpha('SMITH'), 'SNT')
        self.assertEqual(self.pa.encode_alpha('HOUGHTON'), 'HKTN')


if __name__ == '__main__':
    unittest.main()
