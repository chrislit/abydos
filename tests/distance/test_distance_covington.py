# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_covington.

This module contains unit tests for abydos.distance.Covington
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Covington

from six import PY2


class CovingtonTestCases(unittest.TestCase):
    """Test Covington functions.

    abydos.distance.Covington
    """

    cmp = Covington()

    def test_covington_dist(self):
        """Test abydos.distance.Covington.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.014705882352941176)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.4772727272727273)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.2592592593)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.2592592593)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.2037037037)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.2037037037)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.3578947368
        )

        self.assertEqual(self.cmp.dist('bcd', 'bcd'), 0.0)

    def test_covington_sim(self):
        """Test abydos.distance.Covington.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 1.0)
        self.assertEqual(self.cmp.sim('a', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.9852941176470589)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.5227272727272727)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.7407407407)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.7407407407)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.7962962963)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.7962962963)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.6421052632
        )

        self.assertEqual(self.cmp.sim('bcd', 'bcd'), 1.0)

    def test_covington_dist_abs(self):
        """Test abydos.distance.Covington.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 50)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 50)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 130)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 130)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 5)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 210)

        self.assertAlmostEqual(self.cmp.dist_abs('Nigel', 'Niall'), 140)
        self.assertAlmostEqual(self.cmp.dist_abs('Niall', 'Nigel'), 140)
        self.assertAlmostEqual(self.cmp.dist_abs('Colin', 'Coiln'), 110)
        self.assertAlmostEqual(self.cmp.dist_abs('Coiln', 'Colin'), 110)
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 340
        )

    def test_covington_alignments(self):
        """Test abydos.distance.Covington.alignments."""
        if PY2:  # skip tests of alignments on Python 2.7
            return

        self.assertEqual(
            repr(self.cmp.alignments('yo', 'ze', top_n=1)[0]),
            "Alignment(src='yo', tar='ze', score=130)",
        )
        self.assertEqual(
            repr(self.cmp.alignments('tres', 'trwa', top_n=1)[0]),
            "Alignment(src='tr-es', tar='trwa-', score=130)",
        )
        self.assertEqual(
            repr(self.cmp.alignments('detir', 'dir', top_n=1)[0]),
            "Alignment(src='detir', tar='d--ir', score=95)",
        )
        self.assertEqual(
            repr(self.cmp.alignments('niy', 'kni', top_n=1)[0]),
            "Alignment(src='-niy', tar='kni-', score=105)",
        )
        self.assertEqual(
            repr(self.cmp.alignments('hart', 'kordis', top_n=1)[0]),
            "Alignment(src='hart--', tar='kordis', score=240)",
        )
        self.assertEqual(
            repr(self.cmp.alignments('niy', 'genu', top_n=1)[0]),
            "Alignment(src='--niy', tar='genu-', score=170)",
        )
        self.assertEqual(
            repr(self.cmp.alignments('namesa', 'namiqs', top_n=1)[0]),
            "Alignment(src='name-sa', tar='namiqs-', score=135)",
        )
        self.assertEqual(
            repr(self.cmp.alignments('kentum', 'satem', top_n=1)[0]),
            "Alignment(src='kentum', tar='sa-tem', score=170)",
        )
        self.assertEqual(
            repr(self.cmp.alignments('kentum', 'hekaton', top_n=1)[0]),
            "Alignment(src='--kentum', tar='heka-ton', score=260)",
        )
        self.assertEqual(
            repr(self.cmp.alignments('doter', 'tugatir', top_n=2)[1]),
            "Alignment(src='do--ter', tar='tugatir', score=210)",
        )
        self.assertEqual(
            repr(self.cmp.alignments('sit', 'sedere', top_n=1)[0]),
            "Alignment(src='sit---', tar='sedere', score=220)",
        )

        self.assertEqual(
            repr(self.cmp.alignments('doter', 'tugatir', top_n=0)),
            "[Alignment(src='--doter', tar='tugatir', score=210), \
Alignment(src='do--ter', tar='tugatir', score=210), \
Alignment(src='d--oter', tar='tugatir', score=210)]",
        )
        self.assertEqual(
            repr(self.cmp.alignments('sit', 'sed')),
            "[Alignment(src='sit', tar='sed', score=90), \
Alignment(src='s-it', tar='sed-', score=200), \
Alignment(src='sit-', tar='s-ed', score=200), \
Alignment(src='--sit', tar='sed--', score=240), \
Alignment(src='sit--', tar='--sed', score=240), \
Alignment(src='-sit', tar='se-d', score=260), \
Alignment(src='si-t', tar='-sed', score=260), \
Alignment(src='-sit', tar='sed-', score=300), \
Alignment(src='sit-', tar='-sed', score=300)]",
        )
        self.assertEqual(
            repr(self.cmp.alignments('sit', 'sīt', top_n=1)[0]),
            "Alignment(src='sit', tar='sīt', score=10)",
        )


if __name__ == '__main__':
    unittest.main()
