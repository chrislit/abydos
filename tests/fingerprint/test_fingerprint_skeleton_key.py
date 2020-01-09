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

"""abydos.tests.fingerprint.test_fingerprint_skeleton_key.

This module contains unit tests for abydos.fingerprint.SkeletonKey
"""

import unittest

from abydos.fingerprint import SkeletonKey, skeleton_key


class SkeletonKeyTestCases(unittest.TestCase):
    """Test SkeletonKey functions.

    abydos.fingerprint.SkeletonKey
    """

    fp = SkeletonKey()

    def test_skeleton_key(self):
        """Test abydos.fingerprint.SkeletonKey."""
        # Base case
        self.assertEqual(self.fp.fingerprint(''), '')

        # http://dl.acm.org/citation.cfm?id=358048
        self.assertEqual(self.fp.fingerprint('chemogenic'), 'CHMGNEOI')
        self.assertEqual(self.fp.fingerprint('chemomagnetic'), 'CHMGNTEOAI')
        self.assertEqual(self.fp.fingerprint('chemcal'), 'CHMLEA')
        self.assertEqual(self.fp.fingerprint('chemcial'), 'CHMLEIA')
        self.assertEqual(self.fp.fingerprint('chemical'), 'CHMLEIA')
        self.assertEqual(self.fp.fingerprint('chemicial'), 'CHMLEIA')
        self.assertEqual(self.fp.fingerprint('chimical'), 'CHMLIA')
        self.assertEqual(self.fp.fingerprint('chemiluminescence'), 'CHMLNSEIU')
        self.assertEqual(self.fp.fingerprint('chemiluminescent'), 'CHMLNSTEIU')
        self.assertEqual(self.fp.fingerprint('chemicals'), 'CHMLSEIA')
        self.assertEqual(self.fp.fingerprint('chemically'), 'CHMLYEIA')

        # Test wrapper
        self.assertEqual(skeleton_key('chemogenic'), 'CHMGNEOI')


if __name__ == '__main__':
    unittest.main()
