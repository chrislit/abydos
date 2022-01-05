# Copyright 2014-2022 by Christopher C. Little.
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

"""abydos.tests.stemmer.test_stemmer_clef_german.

This module contains unit tests for abydos.stemmer.CLEFGerman
"""

import unittest

from abydos.stemmer import CLEFGerman


class CLEFGermanTestCases(unittest.TestCase):
    """Test CLEF German functions.

    abydos.stemmer.CLEFGerman
    """

    stmr = CLEFGerman()

    def test_clef_german(self):
        """Test abydos.stemmer.CLEFGerman."""
        # base case
        self.assertEqual(self.stmr.stem(''), '')

        # len <= 2
        self.assertEqual(self.stmr.stem('ä'), 'a')
        self.assertEqual(self.stmr.stem('er'), 'er')
        self.assertEqual(self.stmr.stem('es'), 'es')
        self.assertEqual(self.stmr.stem('äh'), 'ah')

        # len > 2
        self.assertEqual(self.stmr.stem('deinen'), 'dein')
        self.assertEqual(self.stmr.stem('können'), 'konn')
        self.assertEqual(self.stmr.stem('Damen'), 'dame')
        self.assertEqual(self.stmr.stem('kleines'), 'klein')
        self.assertEqual(self.stmr.stem('Namen'), 'name')
        self.assertEqual(self.stmr.stem('Äpfel'), 'apfel')
        self.assertEqual(self.stmr.stem('Jahre'), 'jahr')
        self.assertEqual(self.stmr.stem('Mannes'), 'mann')
        self.assertEqual(self.stmr.stem('Häuser'), 'haus')
        self.assertEqual(self.stmr.stem('Motoren'), 'motor')
        self.assertEqual(self.stmr.stem('kleine'), 'klein')
        self.assertEqual(self.stmr.stem('Pfingsten'), 'pfingst')
        self.assertEqual(self.stmr.stem('lautest'), 'lautest')
        self.assertEqual(self.stmr.stem('lauteste'), 'lautest')
        self.assertEqual(self.stmr.stem('lautere'), 'lauter')
        self.assertEqual(self.stmr.stem('lautste'), 'lautst')
        self.assertEqual(self.stmr.stem('kleinen'), 'klei')


if __name__ == '__main__':
    unittest.main()
