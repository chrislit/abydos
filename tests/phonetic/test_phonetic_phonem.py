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

"""abydos.tests.phonetic.test_phonetic_phonem.

This module contains unit tests for abydos.phonetic.Phonem
"""

import unittest

from abydos.phonetic import Phonem


class PhonemTestCases(unittest.TestCase):
    """Test Phonem functions.

    test cases for abydos.phonetic.Phonem
    """

    pa = Phonem()

    def test_phonem(self):
        """Test abydos.phonetic.Phonem."""
        self.assertEqual(self.pa.encode(''), '')

        # http://phonetik.phil-fak.uni-koeln.de/fileadmin/home/ritters/Allgemeine_Dateien/Martin_Wilz.pdf
        self.assertEqual(self.pa.encode('müller'), 'MYLR')
        self.assertEqual(self.pa.encode('schmidt'), 'CMYD')
        self.assertEqual(self.pa.encode('schneider'), 'CNAYDR')
        self.assertEqual(self.pa.encode('fischer'), 'VYCR')
        self.assertEqual(self.pa.encode('weber'), 'VBR')
        self.assertEqual(self.pa.encode('meyer'), 'MAYR')
        self.assertEqual(self.pa.encode('wagner'), 'VACNR')
        self.assertEqual(self.pa.encode('schulz'), 'CULC')
        self.assertEqual(self.pa.encode('becker'), 'BCR')
        self.assertEqual(self.pa.encode('hoffmann'), 'OVMAN')
        self.assertEqual(self.pa.encode('schäfer'), 'CVR')

        # http://cpansearch.perl.org/src/MAROS/Text-Phonetic-2.05/t/008_phonem.t
        self.assertEqual(self.pa.encode('mair'), 'MAYR')
        self.assertEqual(self.pa.encode('bäker'), 'BCR')
        self.assertEqual(self.pa.encode('schaeffer'), 'CVR')
        self.assertEqual(self.pa.encode('computer'), 'COMBUDR')
        self.assertEqual(self.pa.encode('pfeifer'), 'VAYVR')
        self.assertEqual(self.pa.encode('pfeiffer'), 'VAYVR')


if __name__ == '__main__':
    unittest.main()
