# Copyright 2014-2022 by Christopher C. Little.
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

"""abydos.tests.phonetic.test_phonetic_mra.

This module contains unit tests for abydos.phonetic.MRA
"""

import unittest

from abydos.phonetic import MRA


class MraTestCases(unittest.TestCase):
    """Test MRA functions.

    test cases for abydos.phonetic.MRA
    """

    pa = MRA()

    def test_mra(self):
        """Test abydos.phonetic.MRA."""
        self.assertEqual(self.pa.encode(''), '')

        # https://en.wikipedia.org/wiki/Match_rating_approach
        self.assertEqual(self.pa.encode('Byrne'), 'BYRN')
        self.assertEqual(self.pa.encode('Boern'), 'BRN')
        self.assertEqual(self.pa.encode('Smith'), 'SMTH')
        self.assertEqual(self.pa.encode('Smyth'), 'SMYTH')
        self.assertEqual(self.pa.encode('Catherine'), 'CTHRN')
        self.assertEqual(self.pa.encode('Kathryn'), 'KTHRYN')

        # length checks
        self.assertEqual(self.pa.encode('Christopher'), 'CHRPHR')
        self.assertEqual(self.pa.encode('Dickensianistic'), 'DCKSTC')
        self.assertEqual(self.pa.encode('Acetylcholinesterase'), 'ACTTRS')


if __name__ == '__main__':
    unittest.main()
