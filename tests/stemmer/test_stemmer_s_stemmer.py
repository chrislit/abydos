# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

This module contains unit tests for abydos.stemmer._s_stemmer
"""

from __future__ import unicode_literals

import unittest

from abydos.stemmer import s_stemmer


class SStemmerTestCases(unittest.TestCase):
    """Test S-stemmer functions.

    abydos.stemmer._s_stemmer.s_stemmer
    """

    def test_s_stemmer(self):
        """Test abydos.stemmer._s_stemmer.s_stemmer."""
        # Base case
        self.assertEqual(s_stemmer(''), '')

        # Tests from Harman paper
        self.assertEqual(s_stemmer('panels'), 'panel')
        self.assertEqual(s_stemmer('subjected'), 'subjected')
        self.assertEqual(s_stemmer('aerodynamics'), 'aerodynamic')
        self.assertEqual(s_stemmer('heating'), 'heating')

        # Additional tests to complete coverage
        self.assertEqual(s_stemmer('dairies'), 'dairy')
        self.assertEqual(s_stemmer('census'), 'census')
        self.assertEqual(s_stemmer('boss'), 'boss')
        self.assertEqual(s_stemmer('bosses'), 'bosse')
        self.assertEqual(s_stemmer('raises'), 'raise')
        self.assertEqual(s_stemmer('fees'), 'fee')
        self.assertEqual(s_stemmer('attourneies'), 'attourneie')
        self.assertEqual(s_stemmer('portemonnaies'), 'portemonnaie')
        self.assertEqual(s_stemmer('foes'), 'foe')
        self.assertEqual(s_stemmer('sundaes'), 'sundae')


if __name__ == '__main__':
    unittest.main()
