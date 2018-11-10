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

"""abydos.tests.phonetic.test_phonetic_davidson.

This module contains unit tests for abydos.phonetic._davidson
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.phonetic import davidson


class DavidsonTestCases(unittest.TestCase):
    """Test class Davidson functions.

    test cases for abydos.phonetic._davidson.davidson
    """

    def test_davidson(self):
        """Test abydos.phonetic._davidson.davidson."""
        # Base cases
        self.assertEqual(davidson('', omit_fname=True), '    ')
        self.assertEqual(davidson(''), '    .')

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
            self.assertEqual(davidson(word, omit_fname=True), encoding)


if __name__ == '__main__':
    unittest.main()
