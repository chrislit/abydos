# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.tests.fingerprint.test_fingerprint_consonant.

This module contains unit tests for abydos.fingerprint.Consonant
"""

import unittest

from abydos.fingerprint import Consonant


class ConsonantTestCases(unittest.TestCase):
    """Test Taft's consonant coding functions.

    abydos.fingerprint.Consonant
    """

    def test_consonant_fingerprint(self):
        """Test abydos.fingerprint.Consonant."""
        # Base case
        self.assertEqual(Consonant().fingerprint(''), '')

        # Test cases from paper
        self.assertEqual(Consonant(variant=1).fingerprint('ABRAMS'), 'ABRMS')
        self.assertEqual(Consonant(variant=2).fingerprint('ARROW'), 'ARR')
        self.assertEqual(Consonant(variant=3).fingerprint('ABRAHAM'), 'ABRM')
        self.assertEqual(
            Consonant(variant=1, doubles=False).fingerprint('ARROW'), 'ARW'
        )
        self.assertEqual(
            Consonant(variant=2, doubles=False).fingerprint('ARROW'), 'AR'
        )
        self.assertEqual(
            Consonant(variant=3, doubles=False).fingerprint('GARRETH'), 'GRT'
        )

        # coverage
        self.assertEqual(Consonant(vowels='R').fingerprint('ARROW'), 'AOW')


if __name__ == '__main__':
    unittest.main()
