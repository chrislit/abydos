# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_stuart_tau.

This module contains unit tests for abydos.distance.StuartTau
"""

import unittest

from abydos.distance import StuartTau


class StuartTauTestCases(unittest.TestCase):
    """Test StuartTau functions.

    abydos.distance.StuartTau
    """

    cmp = StuartTau()
    cmp_no_d = StuartTau(alphabet=0)

    def test_stuart_tau_sim(self):
        """Test abydos.distance.StuartTau.sim."""
        # Base cases
        self.assertEqual(self.cmp.sim('', ''), 0.5025510204081632)
        self.assertEqual(self.cmp.sim('a', ''), 0.5025380049979176)
        self.assertEqual(self.cmp.sim('', 'a'), 0.5025380049979176)
        self.assertEqual(self.cmp.sim('abc', ''), 0.5025249895876718)
        self.assertEqual(self.cmp.sim('', 'abc'), 0.5025249895876718)
        self.assertEqual(self.cmp.sim('abc', 'abc'), 0.5025510204081632)
        self.assertEqual(self.cmp.sim('abcd', 'efgh'), 0.5024859433569346)

        self.assertAlmostEqual(self.cmp.sim('Nigel', 'Niall'), 0.5025119742)
        self.assertAlmostEqual(self.cmp.sim('Niall', 'Nigel'), 0.5025119742)
        self.assertAlmostEqual(self.cmp.sim('Colin', 'Coiln'), 0.5025119742)
        self.assertAlmostEqual(self.cmp.sim('Coiln', 'Colin'), 0.5025119742)
        self.assertAlmostEqual(
            self.cmp.sim('ATCAACGAGT', 'AACGATTAG'), 0.5025054665
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.sim('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.sim('a', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'a'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', ''), 0.0)
        self.assertEqual(self.cmp_no_d.sim('', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.sim('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.sim('abcd', 'efgh'), 0.3)

        self.assertAlmostEqual(
            self.cmp_no_d.sim('Nigel', 'Niall'), 0.4259259259
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Niall', 'Nigel'), 0.4259259259
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Colin', 'Coiln'), 0.4259259259
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('Coiln', 'Colin'), 0.4259259259
        )
        self.assertAlmostEqual(
            self.cmp_no_d.sim('ATCAACGAGT', 'AACGATTAG'), 0.5
        )

    def test_stuart_tau_dist(self):
        """Test abydos.distance.StuartTau.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.49744897959183676)
        self.assertEqual(self.cmp.dist('a', ''), 0.49746199500208244)
        self.assertEqual(self.cmp.dist('', 'a'), 0.49746199500208244)
        self.assertEqual(self.cmp.dist('abc', ''), 0.4974750104123282)
        self.assertEqual(self.cmp.dist('', 'abc'), 0.4974750104123282)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.49744897959183676)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 0.49751405664306536)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.4974880258)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.4974880258)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.4974880258)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.4974880258)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.4974945335
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.dist('', ''), 0.0)
        self.assertEqual(self.cmp_no_d.dist('a', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp_no_d.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp_no_d.dist('abcd', 'efgh'), 0.7)

        self.assertAlmostEqual(
            self.cmp_no_d.dist('Nigel', 'Niall'), 0.5740740741
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Niall', 'Nigel'), 0.5740740741
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Colin', 'Coiln'), 0.5740740741
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('Coiln', 'Colin'), 0.5740740741
        )
        self.assertAlmostEqual(
            self.cmp_no_d.dist('ATCAACGAGT', 'AACGATTAG'), 0.5
        )

    def test_stuart_tau_corr(self):
        """Test abydos.distance.StuartTau.corr."""
        # Base cases
        self.assertEqual(self.cmp.corr('', ''), 0.00510204081632653)
        self.assertEqual(self.cmp.corr('a', ''), 0.005076009995835068)
        self.assertEqual(self.cmp.corr('', 'a'), 0.005076009995835068)
        self.assertEqual(self.cmp.corr('abc', ''), 0.005049979175343606)
        self.assertEqual(self.cmp.corr('', 'abc'), 0.005049979175343606)
        self.assertEqual(self.cmp.corr('abc', 'abc'), 0.00510204081632653)
        self.assertEqual(self.cmp.corr('abcd', 'efgh'), 0.0049718867138692216)

        self.assertAlmostEqual(self.cmp.corr('Nigel', 'Niall'), 0.0050239484)
        self.assertAlmostEqual(self.cmp.corr('Niall', 'Nigel'), 0.0050239484)
        self.assertAlmostEqual(self.cmp.corr('Colin', 'Coiln'), 0.0050239484)
        self.assertAlmostEqual(self.cmp.corr('Coiln', 'Colin'), 0.0050239484)
        self.assertAlmostEqual(
            self.cmp.corr('ATCAACGAGT', 'AACGATTAG'), 0.0050109329
        )

        # Tests with alphabet=0 (no d factor)
        self.assertEqual(self.cmp_no_d.corr('', ''), 1.0)
        self.assertEqual(self.cmp_no_d.corr('a', ''), -1.0)
        self.assertEqual(self.cmp_no_d.corr('', 'a'), -1.0)
        self.assertEqual(self.cmp_no_d.corr('abc', ''), -1.0)
        self.assertEqual(self.cmp_no_d.corr('', 'abc'), -1.0)
        self.assertEqual(self.cmp_no_d.corr('abc', 'abc'), 1.0)
        self.assertEqual(self.cmp_no_d.corr('abcd', 'efgh'), -0.4)

        self.assertAlmostEqual(
            self.cmp_no_d.corr('Nigel', 'Niall'), -0.1481481481
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Niall', 'Nigel'), -0.1481481481
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Colin', 'Coiln'), -0.1481481481
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('Coiln', 'Colin'), -0.1481481481
        )
        self.assertAlmostEqual(
            self.cmp_no_d.corr('ATCAACGAGT', 'AACGATTAG'), 0.0
        )


if __name__ == '__main__':
    unittest.main()
