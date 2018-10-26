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

"""abydos.tests.stemmer.test_stemmer_clef.

This module contains unit tests for abydos.stemmer.clef
"""

from __future__ import unicode_literals

import unittest

from abydos.stemmer.clef import clef_german, clef_german_plus, clef_swedish


class CLEFTestCases(unittest.TestCase):
    """Test CLEF functions.

    abydos.stemmer.clef.clef_german, .clef_german_plus, & .clef_swedish
    """

    def test_clef_german(self):
        """Test abydos.stemmer.clef.clef_german."""
        # base case
        self.assertEqual(clef_german(''), '')

        # len <= 2
        self.assertEqual(clef_german('ä'), 'a')
        self.assertEqual(clef_german('er'), 'er')
        self.assertEqual(clef_german('es'), 'es')
        self.assertEqual(clef_german('äh'), 'ah')

        # len > 2
        self.assertEqual(clef_german('deinen'), 'dein')
        self.assertEqual(clef_german('können'), 'konn')
        self.assertEqual(clef_german('Damen'), 'dame')
        self.assertEqual(clef_german('kleines'), 'klein')
        self.assertEqual(clef_german('Namen'), 'name')
        self.assertEqual(clef_german('Äpfel'), 'apfel')
        self.assertEqual(clef_german('Jahre'), 'jahr')
        self.assertEqual(clef_german('Mannes'), 'mann')
        self.assertEqual(clef_german('Häuser'), 'haus')
        self.assertEqual(clef_german('Motoren'), 'motor')
        self.assertEqual(clef_german('kleine'), 'klein')
        self.assertEqual(clef_german('Pfingsten'), 'pfingst')
        self.assertEqual(clef_german('lautest'), 'lautest')
        self.assertEqual(clef_german('lauteste'), 'lautest')
        self.assertEqual(clef_german('lautere'), 'lauter')
        self.assertEqual(clef_german('lautste'), 'lautst')
        self.assertEqual(clef_german('kleinen'), 'klei')

    def test_clef_german_plus(self):
        """Test abydos.stemmer.clef.clef_german_plus."""
        # base case
        self.assertEqual(clef_german_plus(''), '')

        # len <= 2
        self.assertEqual(clef_german_plus('ä'), 'a')
        self.assertEqual(clef_german_plus('er'), 'er')
        self.assertEqual(clef_german_plus('es'), 'es')
        self.assertEqual(clef_german_plus('äh'), 'ah')

        # len > 2
        self.assertEqual(clef_german_plus('deinen'), 'dein')
        self.assertEqual(clef_german_plus('können'), 'konn')
        self.assertEqual(clef_german_plus('Damen'), 'dam')
        self.assertEqual(clef_german_plus('kleines'), 'klein')
        self.assertEqual(clef_german_plus('Namen'), 'nam')
        self.assertEqual(clef_german_plus('Äpfel'), 'apfel')
        self.assertEqual(clef_german_plus('Jahre'), 'jahr')
        self.assertEqual(clef_german_plus('Mannes'), 'mann')
        self.assertEqual(clef_german_plus('Häuser'), 'haus')
        self.assertEqual(clef_german_plus('Motoren'), 'motor')
        self.assertEqual(clef_german_plus('kleine'), 'klein')
        self.assertEqual(clef_german_plus('Pfingsten'), 'pfing')
        self.assertEqual(clef_german_plus('lautest'), 'laut')
        self.assertEqual(clef_german_plus('lauteste'), 'laut')
        self.assertEqual(clef_german_plus('lautere'), 'laut')
        self.assertEqual(clef_german_plus('lautste'), 'laut')
        self.assertEqual(clef_german_plus('kleinen'), 'klein')
        self.assertEqual(clef_german_plus('Pfarrern'), 'pfarr')

    def test_clef_swedish(self):
        """Test abydos.stemmer.clef.clef_swedish."""
        # base case
        self.assertEqual(clef_swedish(''), '')

        # unstemmed
        self.assertEqual(clef_swedish('konung'), 'konung')

        # len <= 3
        self.assertEqual(clef_swedish('km'), 'km')
        self.assertEqual(clef_swedish('ja'), 'ja')
        self.assertEqual(clef_swedish('de'), 'de')
        self.assertEqual(clef_swedish('in'), 'in')
        self.assertEqual(clef_swedish('a'), 'a')
        self.assertEqual(clef_swedish('mer'), 'mer')
        self.assertEqual(clef_swedish('s'), 's')
        self.assertEqual(clef_swedish('e'), 'e')
        self.assertEqual(clef_swedish('oss'), 'oss')
        self.assertEqual(clef_swedish('hos'), 'hos')

        # genitive
        self.assertEqual(clef_swedish('svenskars'), 'svensk')
        self.assertEqual(clef_swedish('stadens'), 'stad')
        self.assertEqual(clef_swedish('kommuns'), 'kommu')
        self.assertEqual(clef_swedish('aftonbladets'), 'aftonblad')

        # len > 7
        self.assertEqual(clef_swedish('fängelser'), 'fäng')
        self.assertEqual(clef_swedish('möjligheten'), 'möjlig')

        # len > 6
        self.assertEqual(clef_swedish('svenskar'), 'svensk')
        self.assertEqual(clef_swedish('myndigheterna'), 'myndighet')
        self.assertEqual(clef_swedish('avgörande'), 'avgör')
        self.assertEqual(clef_swedish('fängelse'), 'fäng')
        self.assertEqual(clef_swedish('viktigaste'), 'viktig')
        self.assertEqual(clef_swedish('kvinnorna'), 'kvinn')
        self.assertEqual(clef_swedish('åklagaren'), 'åklag')

        # len > 5
        self.assertEqual(clef_swedish('tidigare'), 'tidig')
        self.assertEqual(clef_swedish('senast'), 'sen')
        self.assertEqual(clef_swedish('möjlighet'), 'möjlig')

        # len > 4
        self.assertEqual(clef_swedish('svenskar'), 'svensk')
        self.assertEqual(clef_swedish('skriver'), 'skriv')
        self.assertEqual(clef_swedish('människor'), 'människ')
        self.assertEqual(clef_swedish('staden'), 'stad')
        self.assertEqual(clef_swedish('kunnat'), 'kunn')
        self.assertEqual(clef_swedish('samarbete'), 'samarbe')
        self.assertEqual(clef_swedish('aftonbladet'), 'aftonblad')

        # len > 3
        self.assertEqual(clef_swedish('allt'), 'all')
        self.assertEqual(clef_swedish('vilka'), 'vilk')
        self.assertEqual(clef_swedish('länge'), 'läng')
        self.assertEqual(clef_swedish('kommun'), 'kommu')


if __name__ == '__main__':
    unittest.main()
