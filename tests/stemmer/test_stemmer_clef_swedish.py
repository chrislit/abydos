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

"""abydos.tests.stemmer.test_stemmer_clef_swedish.

This module contains unit tests for abydos.stemmer.CLEFSwedish
"""

import unittest

from abydos.stemmer import CLEFSwedish, clef_swedish


class CLEFTestCases(unittest.TestCase):
    """Test CLEF Swedish functions.

    abydos.stemmer.CLEFSwedish
    """

    stmr = CLEFSwedish()

    def test_clef_swedish(self):
        """Test abydos.stemmer.CLEFSwedish."""
        # base case
        self.assertEqual(self.stmr.stem(''), '')

        # unstemmed
        self.assertEqual(self.stmr.stem('konung'), 'konung')

        # len <= 3
        self.assertEqual(self.stmr.stem('km'), 'km')
        self.assertEqual(self.stmr.stem('ja'), 'ja')
        self.assertEqual(self.stmr.stem('de'), 'de')
        self.assertEqual(self.stmr.stem('in'), 'in')
        self.assertEqual(self.stmr.stem('a'), 'a')
        self.assertEqual(self.stmr.stem('mer'), 'mer')
        self.assertEqual(self.stmr.stem('s'), 's')
        self.assertEqual(self.stmr.stem('e'), 'e')
        self.assertEqual(self.stmr.stem('oss'), 'oss')
        self.assertEqual(self.stmr.stem('hos'), 'hos')

        # genitive
        self.assertEqual(self.stmr.stem('svenskars'), 'svensk')
        self.assertEqual(self.stmr.stem('stadens'), 'stad')
        self.assertEqual(self.stmr.stem('kommuns'), 'kommu')
        self.assertEqual(self.stmr.stem('aftonbladets'), 'aftonblad')

        # len > 7
        self.assertEqual(self.stmr.stem('fängelser'), 'fäng')
        self.assertEqual(self.stmr.stem('möjligheten'), 'möjlig')

        # len > 6
        self.assertEqual(self.stmr.stem('svenskar'), 'svensk')
        self.assertEqual(self.stmr.stem('myndigheterna'), 'myndighet')
        self.assertEqual(self.stmr.stem('avgörande'), 'avgör')
        self.assertEqual(self.stmr.stem('fängelse'), 'fäng')
        self.assertEqual(self.stmr.stem('viktigaste'), 'viktig')
        self.assertEqual(self.stmr.stem('kvinnorna'), 'kvinn')
        self.assertEqual(self.stmr.stem('åklagaren'), 'åklag')

        # len > 5
        self.assertEqual(self.stmr.stem('tidigare'), 'tidig')
        self.assertEqual(self.stmr.stem('senast'), 'sen')
        self.assertEqual(self.stmr.stem('möjlighet'), 'möjlig')

        # len > 4
        self.assertEqual(self.stmr.stem('svenskar'), 'svensk')
        self.assertEqual(self.stmr.stem('skriver'), 'skriv')
        self.assertEqual(self.stmr.stem('människor'), 'människ')
        self.assertEqual(self.stmr.stem('staden'), 'stad')
        self.assertEqual(self.stmr.stem('kunnat'), 'kunn')
        self.assertEqual(self.stmr.stem('samarbete'), 'samarbe')
        self.assertEqual(self.stmr.stem('aftonbladet'), 'aftonblad')

        # len > 3
        self.assertEqual(self.stmr.stem('allt'), 'all')
        self.assertEqual(self.stmr.stem('vilka'), 'vilk')
        self.assertEqual(self.stmr.stem('länge'), 'läng')
        self.assertEqual(self.stmr.stem('kommun'), 'kommu')

        # Test wrapper
        self.assertEqual(clef_swedish('svenskars'), 'svensk')


if __name__ == '__main__':
    unittest.main()
