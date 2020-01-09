# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.tests.fingerprint.test_fingerprint_lc_cutter.

This module contains unit tests for abydos.fingerprint.LCCutter
"""

import unittest

from abydos.fingerprint import LCCutter


class LCCutterTestCases(unittest.TestCase):
    """Test LCCutter functions.

    abydos.fingerprint.LCCutter
    """

    fp = LCCutter()

    def test_lc_cutter_fingerprint(self):
        """Test abydos.fingerprint.LCCutter."""
        # Base case
        self.assertEqual(self.fp.fingerprint(''), '')
        self.assertEqual(self.fp.fingerprint('S'), 'S')

        # Test cases drawn from http://calculate.alptown.com/
        self.assertEqual(self.fp.fingerprint('Cutter'), 'C88847')
        self.assertEqual(self.fp.fingerprint('Quiet'), 'Q548')
        self.assertEqual(self.fp.fingerprint('Schmidt'), 'S36538')
        self.assertEqual(self.fp.fingerprint('Anderson'), 'A5347766')
        self.assertEqual(self.fp.fingerprint('Aziz'), 'A959')
        self.assertEqual(self.fp.fingerprint('I.B.M.'), 'I26')
        self.assertEqual(self.fp.fingerprint('Import'), 'I47678')
        self.assertEqual(self.fp.fingerprint('Sadron'), 'S23766')
        self.assertEqual(self.fp.fingerprint('Stinson'), 'S756766')
        self.assertEqual(self.fp.fingerprint('Cymbal'), 'C96335')
        self.assertEqual(self.fp.fingerprint('Ipswich'), 'I679534')
        self.assertEqual(self.fp.fingerprint('Rhododendron'), 'R46363463766')
        self.assertEqual(self.fp.fingerprint('Colin'), 'C6556')
        self.assertEqual(self.fp.fingerprint('Szelazek'), 'S9453945')
        self.assertEqual(self.fp.fingerprint('Quyen'), 'Q946')

        # Coverage
        self.assertEqual(self.fp.fingerprint('Qdoba'), 'Q2633')
        self.assertEqual(LCCutter(max_length=-1).fingerprint('Qdoba'), 'Q2633')
        self.assertEqual(LCCutter(max_length=3).fingerprint('Qdoba'), 'Q26')


if __name__ == '__main__':
    unittest.main()
