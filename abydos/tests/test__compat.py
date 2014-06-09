# -*- coding: utf-8 -*-
"""abydos.tests.test__compat

This module contains unit tests for abydos._compat

Copyright 2014 by Christopher C. Little.
This file is part of Abydos.

Abydos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Abydos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Abydos. If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals
import abydos._compat
import unittest
import sys

class CompatTestCases(unittest.TestCase):
    """test cases for abydos._compat
    """
    def test__compat(self):
        """test abydos._compat
        """
        # pylint: disable=protected-access
        if sys.version_info[0] == 3:
            self.assertTrue(isinstance(abydos._compat._range(5), range))
            self.assertTrue(isinstance(abydos._compat._unicode('abcdefg'), str))
            self.assertTrue(isinstance(abydos._compat._unichr(0x2014), str))
        else:
            self.assertTrue(isinstance(abydos._compat._range(5), xrange))
            self.assertTrue(isinstance(abydos._compat._unicode('abcdefg'),
                                       unicode))
            self.assertTrue(isinstance(abydos._compat._unichr(0x2014), unicode))
        # pylint: enable=protected-access

if __name__ == '__main__':
    unittest.main()
     