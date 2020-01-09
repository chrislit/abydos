# -*- coding: utf-8 -*-

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

"""abydos.tests.fingerprint.test_fingerprint_extract_position_frequence.

This module contains unit tests for abydos.fingerprint.ExtractPositionFrequency
"""

import unittest

from abydos.fingerprint import ExtractPositionFrequency


class ExtractPositionFrequencyTestCases(unittest.TestCase):
    """Test ExtractPositionFrequency functions.

    abydos.fingerprint.ExtractPositionFrequency
    """

    fp = ExtractPositionFrequency()

    def test_extract_position_frequence_fingerprint(self):
        """Test abydos.fingerprint.ExtractPositionFrequency."""
        # Base case
        self.assertEqual(self.fp.fingerprint(''), '')

        # Test cases from paper
        self.assertEqual(self.fp.fingerprint('Wilkinson'), 'WKON')


if __name__ == '__main__':
    unittest.main()
