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

"""abydos.tests.phonetic.test_phonetic_pshp_soundex_first.

This module contains unit tests for abydos.phonetic.PSHPSoundexFirst
"""

import unittest

from abydos.phonetic import PSHPSoundexFirst, pshp_soundex_first


class PSHPSoundexTestCases(unittest.TestCase):
    """Test PSHP Soundex functions.

    test cases for abydos.phonetic.PSHPSoundexFirst
    """

    pa = PSHPSoundexFirst()
    pa_german = PSHPSoundexFirst(german=True)
    pa_unl = PSHPSoundexFirst(max_length=-1)

    def test_pshp_soundex_first(self):
        """Test abydos.phonetic.PSHPSoundexFirst."""
        # Base case
        self.assertEqual(self.pa.encode(''), '0000')

        # Examples given in defining paper (Hershberg, et al. 1976)
        self.assertEqual(self.pa.encode('JAMES'), 'J700')
        self.assertEqual(self.pa.encode('JOHN'), 'J500')
        self.assertEqual(self.pa.encode('PAT'), 'P700')
        self.assertEqual(self.pa.encode('PETER'), 'P300')

        # Additions for coverage
        self.assertEqual(self.pa.encode('Giles'), 'J400')
        self.assertEqual(self.pa.encode('Cy'), 'S000')
        self.assertEqual(self.pa.encode('Chris'), 'K500')
        self.assertEqual(self.pa.encode('Caleb'), 'K400')
        self.assertEqual(self.pa.encode('Knabe'), 'N100')
        self.assertEqual(self.pa.encode('Phil'), 'F400')
        self.assertEqual(self.pa.encode('Wieland'), 'V400')
        self.assertEqual(self.pa_german.encode('Wayne'), 'V500')
        self.assertEqual(self.pa_unl.encode('Christopher'), 'K5')
        self.assertEqual(self.pa_unl.encode('Asdaananndsjsjasd'), 'A23553223')
        self.assertEqual(self.pa.encode('Asdaananndsjsjasd'), 'A235')

        # encode_alpha
        self.assertEqual(self.pa.encode_alpha('JAMES'), 'JN')
        self.assertEqual(self.pa.encode_alpha('JOHN'), 'JN')
        self.assertEqual(self.pa.encode_alpha('PAT'), 'PT')
        self.assertEqual(self.pa.encode_alpha('PETER'), 'PT')
        self.assertEqual(self.pa.encode_alpha('Knabe'), 'NP')
        self.assertEqual(self.pa.encode_alpha('Phil'), 'FL')
        self.assertEqual(self.pa.encode_alpha('Wieland'), 'VL')

        # Test wrapper
        self.assertEqual(pshp_soundex_first('Giles'), 'J400')


if __name__ == '__main__':
    unittest.main()
