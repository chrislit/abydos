# -*- coding: utf-8 -*-
"""abydos.tests.test_stemmer

This module contains unit tests for abydos.stemmer

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
import unittest
from abydos.stemmer import _m_degree, porter

class PorterTestCases(unittest.TestCase):
    """test cases for abydos.stemmer._m_degree, abydos.stemmer.porter 
    """
    def test_m_degree(self):
        """test abydos.stemmer._m_degree
        """
        # base case
        self.assertEqual(_m_degree(''), 0)

        # m==0
        self.assertEqual(_m_degree('TR'), 0)
        self.assertEqual(_m_degree('EE'), 0)
        self.assertEqual(_m_degree('TREE'), 0)
        self.assertEqual(_m_degree('Y'), 0)
        self.assertEqual(_m_degree('BY'), 0)

        # m==1
        self.assertEqual(_m_degree('TROUBLE'), 1)
        self.assertEqual(_m_degree('OATS'), 1)
        self.assertEqual(_m_degree('TREES'), 1)
        self.assertEqual(_m_degree('IVY'), 1)

        # m==2
        self.assertEqual(_m_degree('TROUBLES'), 2)
        self.assertEqual(_m_degree('PRIVATE'), 2)
        self.assertEqual(_m_degree('OATEN'), 2)
        self.assertEqual(_m_degree('ORRERY'), 2)

    def test_porter(self):
        """test abydos.stemmer.porter
        """
        pass
