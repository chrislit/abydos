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

"""abydos.tests.fingerprint.test_fingerprint_speedcop.

This module contains unit tests for abydos.fingerprint._speedcop
"""

from __future__ import unicode_literals

import unittest

from abydos.fingerprint import omission_key, skeleton_key


class SPEEDCOPTestCases(unittest.TestCase):
    """Test SPEEDCOP functions.

    abydos.fingerprint._speedcop.skeleton_key & .omission_key
    """

    def test_skeleton_key(self):
        """Test abydos.fingerprint._speedcop.skeleton_key."""
        # Base case
        self.assertEqual(skeleton_key(''), '')

        # http://dl.acm.org/citation.cfm?id=358048
        self.assertEqual(skeleton_key('chemogenic'), 'CHMGNEOI')
        self.assertEqual(skeleton_key('chemomagnetic'), 'CHMGNTEOAI')
        self.assertEqual(skeleton_key('chemcal'), 'CHMLEA')
        self.assertEqual(skeleton_key('chemcial'), 'CHMLEIA')
        self.assertEqual(skeleton_key('chemical'), 'CHMLEIA')
        self.assertEqual(skeleton_key('chemicial'), 'CHMLEIA')
        self.assertEqual(skeleton_key('chimical'), 'CHMLIA')
        self.assertEqual(skeleton_key('chemiluminescence'), 'CHMLNSEIU')
        self.assertEqual(skeleton_key('chemiluminescent'), 'CHMLNSTEIU')
        self.assertEqual(skeleton_key('chemicals'), 'CHMLSEIA')
        self.assertEqual(skeleton_key('chemically'), 'CHMLYEIA')

    def test_omission_key(self):
        """Test abydos.fingerprint._speedcop.omission_key."""
        # Base case
        self.assertEqual(omission_key(''), '')

        # http://dl.acm.org/citation.cfm?id=358048
        self.assertEqual(omission_key('microelectronics'), 'MCLNTSRIOE')
        self.assertEqual(omission_key('circumstantial'), 'MCLNTSRIUA')
        self.assertEqual(omission_key('luminescent'), 'MCLNTSUIE')
        self.assertEqual(omission_key('multinucleate'), 'MCLNTUIEA')
        self.assertEqual(omission_key('multinucleon'), 'MCLNTUIEO')
        self.assertEqual(omission_key('cumulene'), 'MCLNUE')
        self.assertEqual(omission_key('luminance'), 'MCLNUIAE')
        self.assertEqual(omission_key('coelomic'), 'MCLOEI')
        self.assertEqual(omission_key('molecule'), 'MCLOEU')
        self.assertEqual(omission_key('cameral'), 'MCLRAE')
        self.assertEqual(omission_key('caramel'), 'MCLRAE')
        self.assertEqual(omission_key('maceral'), 'MCLRAE')
        self.assertEqual(omission_key('lacrimal'), 'MCLRAI')


if __name__ == '__main__':
    unittest.main()
