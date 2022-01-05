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

"""abydos.tests.stemmer.test_stemmer_stemmer.

This module contains unit tests for abydos.stemmer._Stemmer
"""

import unittest

# noinspection PyProtectedMember
from abydos.stemmer._stemmer import _Stemmer


class SnowballTestCases(unittest.TestCase):
    """Test _Stemmer base class.

    abydos.stemmer._Stemmer
    """

    stmr = _Stemmer()

    def test__stemmer(self):
        """Test abydos.stemmer._Stemmer."""
        # base case
        self.assertEqual(self.stmr.stem(''), '')
        self.assertEqual(self.stmr.stem('word'), 'word')


if __name__ == '__main__':
    unittest.main()
