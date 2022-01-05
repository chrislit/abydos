# Copyright 2018-2020 by Christopher C. Little.
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

"""abydos.tests.fingerprint.test_fingerprint_occurrence.

This module contains unit tests for abydos.fingerprint.Occurrence
"""

import unittest

from abydos.fingerprint import Occurrence


class OccurrenceFingerprintTestCases(unittest.TestCase):
    """Test Cisłak & Grabowski's occurrence fingerprint functions.

    abydos.fingerprint.Occurrence
    """

    fp = Occurrence()

    def test_occurrence_fingerprint(self):
        """Test abydos.fingerprint.Occurrence."""
        # Base case
        self.assertEqual(self.fp.fingerprint(''), '0' * 16)

        # https://arxiv.org/pdf/1711.08475.pdf
        self.assertEqual(self.fp.fingerprint('instance'), '1110111000010000')

        self.assertEqual(self.fp.fingerprint('inst'), '0100111000000000')
        self.assertEqual(
            Occurrence(15).fingerprint('instance'), '111011100001000'
        )
        self.assertEqual(
            Occurrence(32).fingerprint('instance'),
            '11101110000100000000000000000000',
        )
        self.assertEqual(
            Occurrence(64).fingerprint('instance'),
            f"11101110000100000000000000000000{'0' * 32}",
        )


if __name__ == '__main__':
    unittest.main()
