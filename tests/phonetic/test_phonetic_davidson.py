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

"""abydos.tests.phonetic.test_phonetic_davidson.

This module contains unit tests for abydos.phonetic.Davidson
"""

import unittest

from abydos.phonetic import Davidson, davidson


class DavidsonTestCases(unittest.TestCase):
    """Test class Davidson functions.

    test cases for abydos.phonetic.Davidson
    """

    pa = Davidson(omit_fname=True)

    def test_davidson_encode(self):
        """Test abydos.phonetic.Davidson."""
        # Base cases
        self.assertEqual(self.pa.encode(''), '    ')
        self.assertEqual(Davidson().encode(''), '    .')

        # Test cases from Gadd (1988) "'Fisching fore werds': phonetic
        # retrieval of written text in information systems." Program,
        # 22(3). 222--237.
        # doi:10.1108/eb046999
        test_cases = (
            ('WAIT', 'WT  '),
            ('WEIGHT', 'WGT '),
            ('KNIGHT', 'KNGT'),
            ('NIGHT', 'NGT '),
            ('NITE', 'NT  '),
            ('GNOME', 'GNM '),
            ('NOAM', 'NM  '),
            ('SMIDT', 'SMDT'),
            ('SMIT', 'SMT '),
            ('SMITH', 'SMT '),
            ('SCHMIT', 'SCMT'),
            ('CRAFT', 'CRFT'),
            ('KRAFT', 'KRFT'),
            ('REES', 'RS  '),
            ('REECE', 'RC  '),
        )
        for word, encoding in test_cases:
            self.assertEqual(self.pa.encode(word), encoding)

        # Test wrapper
        self.assertEqual(davidson('WAIT', omit_fname=True), 'WT  ')


if __name__ == '__main__':
    unittest.main()
