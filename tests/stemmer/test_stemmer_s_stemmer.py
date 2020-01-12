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

"""abydos.tests.stemmer.test_stemmer_s_stemmer.

This module contains unit tests for abydos.stemmer.SStemmer
"""

import unittest

from abydos.stemmer import SStemmer


class SStemmerTestCases(unittest.TestCase):
    """Test S-stemmer functions.

    abydos.stemmer.SStemmer
    """

    stmr = SStemmer()

    def test_s_stemmer(self):
        """Test abydos.stemmer.SStemmer."""
        # Base case
        self.assertEqual(self.stmr.stem(''), '')

        # Tests from Harman paper
        self.assertEqual(self.stmr.stem('panels'), 'panel')
        self.assertEqual(self.stmr.stem('subjected'), 'subjected')
        self.assertEqual(self.stmr.stem('aerodynamics'), 'aerodynamic')
        self.assertEqual(self.stmr.stem('heating'), 'heating')

        # Additional tests to complete coverage
        self.assertEqual(self.stmr.stem('dairies'), 'dairy')
        self.assertEqual(self.stmr.stem('census'), 'census')
        self.assertEqual(self.stmr.stem('boss'), 'boss')
        self.assertEqual(self.stmr.stem('bosses'), 'bosse')
        self.assertEqual(self.stmr.stem('raises'), 'raise')
        self.assertEqual(self.stmr.stem('fees'), 'fee')
        self.assertEqual(self.stmr.stem('attourneies'), 'attourneie')
        self.assertEqual(self.stmr.stem('portemonnaies'), 'portemonnaie')
        self.assertEqual(self.stmr.stem('foes'), 'foe')
        self.assertEqual(self.stmr.stem('sundaes'), 'sundae')


if __name__ == '__main__':
    unittest.main()
