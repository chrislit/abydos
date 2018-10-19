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

"""abydos.tests.test_phonetic_mra.

This module contains unit tests for abydos.phonetic.mra
"""

from __future__ import unicode_literals

import unittest

from abydos.phonetic.mra import mra


class MraTestCases(unittest.TestCase):
    """Test MRA functions.

    test cases for abydos.phonetic.mra
    """

    def test_mra(self):
        """Test abydos.phonetic.mra."""
        self.assertEqual(mra(''), '')

        # https://en.wikipedia.org/wiki/Match_rating_approach
        self.assertEqual(mra('Byrne'), 'BYRN')
        self.assertEqual(mra('Boern'), 'BRN')
        self.assertEqual(mra('Smith'), 'SMTH')
        self.assertEqual(mra('Smyth'), 'SMYTH')
        self.assertEqual(mra('Catherine'), 'CTHRN')
        self.assertEqual(mra('Kathryn'), 'KTHRYN')

        # length checks
        self.assertEqual(mra('Christopher'), 'CHRPHR')
        self.assertEqual(mra('Dickensianistic'), 'DCKSTC')
        self.assertEqual(mra('Acetylcholinesterase'), 'ACTTRS')


if __name__ == '__main__':
    unittest.main()
