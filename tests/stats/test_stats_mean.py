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

"""abydos.tests.stats.test_stats_mean.

This module contains unit tests for abydos.stats mean functions
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest
from math import isnan

from abydos.stats import (
    aghmean,
    agmean,
    amean,
    cmean,
    ghmean,
    gmean,
    heronian_mean,
    hmean,
    hoelder_mean,
    imean,
    lehmer_mean,
    lmean,
    median,
    midrange,
    mode,
    qmean,
    seiffert_mean,
    std,
    var,
)


class MeansTestCases(unittest.TestCase):
    """Test abydos.stats mean functions."""

    _ones = [1, 1, 1, 1, 1]
    _zeros = [0, 0, 0, 0, 0]
    _one_to_five = [1, 2, 3, 4, 5]
    _onethreefive = [1, 1, 3, 5, 5]
    _floats = [0.5, 0.8, 0.1, 0.2, 0.25]
    _has_inf = [0, 1, 2, float('inf')]
    _2ones = [1, 1]
    _2zeros = [0, 0]
    _onetwo = [1, 2]
    _2floats = [0.5, 0.25]

    def test_means_amean(self):
        """Test abydos.stats.amean."""
        self.assertAlmostEqual(amean(self._ones), 1)
        self.assertAlmostEqual(amean(self._zeros), 0)
        self.assertAlmostEqual(amean(self._one_to_five), 3)
        self.assertAlmostEqual(amean(self._onethreefive), 3)
        self.assertAlmostEqual(amean(self._floats), 0.37)

    def test_means_gmean(self):
        """Test abydos.stats.gmean."""
        self.assertAlmostEqual(gmean(self._ones), 1)
        self.assertAlmostEqual(gmean(self._zeros), 0)
        self.assertAlmostEqual(gmean(self._one_to_five), 2.605171084697352)
        self.assertAlmostEqual(gmean(self._onethreefive), 2.3714406097793117)
        self.assertAlmostEqual(gmean(self._floats), 0.2885399811814427)

    def test_means_hmean(self):
        """Test abydos.stats.hmean."""
        self.assertAlmostEqual(hmean(self._ones), 1)
        self.assertAlmostEqual(hmean(self._zeros), 0)
        self.assertAlmostEqual(hmean(self._one_to_five), 2.18978102189781)
        self.assertAlmostEqual(hmean(self._onethreefive), 1.8292682926829265)
        self.assertAlmostEqual(hmean(self._floats), 0.2247191011235955)
        self.assertEqual(hmean([0, 1, 2]), 0)
        self.assertEqual(hmean([1, 2, 3, 0]), 0)
        self.assertTrue(isnan(hmean([0, 0, 1, 2])))
        self.assertTrue(isnan(hmean([1, 0, 2, 0, 3])))
        self.assertTrue(isnan(hmean([1, 0, 2, 0, 3, 0])))
        self.assertTrue(isnan(hmean([1, 0, 2, 0, 3, 0, 0])))
        self.assertEqual(hmean([0, 0]), 0)
        self.assertEqual(hmean([5, 5, 5, 5, 5]), 5)
        self.assertEqual(hmean([0]), 0)
        self.assertEqual(hmean([8]), 8)
        self.assertRaises(ValueError, hmean, ([]))

    def test_means_qmean(self):
        """Test abydos.stats.qmean."""
        self.assertAlmostEqual(qmean(self._ones), 1)
        self.assertAlmostEqual(qmean(self._zeros), 0)
        self.assertAlmostEqual(qmean(self._one_to_five), 3.3166247903554)
        self.assertAlmostEqual(qmean(self._onethreefive), 3.492849839314596)
        self.assertAlmostEqual(qmean(self._floats), 0.4477722635447623)

    def test_means_cmean(self):
        """Test abydos.stats.cmean."""
        self.assertAlmostEqual(cmean(self._ones), 1)
        self.assertAlmostEqual(cmean(self._one_to_five), 3.6666666666666665)
        self.assertAlmostEqual(cmean(self._onethreefive), 4.066666666666666)
        self.assertAlmostEqual(cmean(self._floats), 0.5418918918918919)

    def test_means_lmean(self):
        """Test abydos.stats.lmean."""
        self.assertAlmostEqual(lmean(self._one_to_five), 2.6739681320855766)
        self.assertAlmostEqual(lmean(self._floats), 0.301387278840469)
        self.assertEqual(lmean([1, 1]), 1)
        self.assertEqual(lmean([2, 2]), 2)
        self.assertRaises(ValueError, lmean, (1, 1, 1))
        self.assertRaises(ValueError, lmean, (0.15, 0.15, 1))

    def test_means_imean(self):
        """Test abydos.stats.imean."""
        self.assertRaises(ValueError, imean, self._ones)
        self.assertRaises(ValueError, imean, self._zeros)
        self.assertRaises(ValueError, imean, self._one_to_five)
        self.assertRaises(ValueError, imean, self._onethreefive)
        self.assertRaises(ValueError, imean, self._floats)
        self.assertAlmostEqual(imean(self._2ones), 1)
        self.assertTrue(isnan(imean(self._2zeros)))
        self.assertAlmostEqual(imean(self._onetwo), 1.4715177646857693)
        self.assertAlmostEqual(imean(self._2floats), 0.36787944117144233)
        self.assertEqual(imean([1]), 1)
        self.assertEqual(imean([0.05]), 0.05)

    def test_means_seiffert_mean(self):
        """Test abydos.stats.seiffert_mean."""
        self.assertRaises(ValueError, seiffert_mean, self._ones)
        self.assertRaises(ValueError, seiffert_mean, self._zeros)
        self.assertRaises(ValueError, seiffert_mean, self._one_to_five)
        self.assertRaises(ValueError, seiffert_mean, self._onethreefive)
        self.assertRaises(ValueError, seiffert_mean, self._floats)
        self.assertAlmostEqual(seiffert_mean(self._onetwo), 1.4712939827611637)
        self.assertAlmostEqual(
            seiffert_mean(self._2floats), 0.36782349569029094
        )
        self.assertEqual(seiffert_mean([1]), 1)
        self.assertEqual(seiffert_mean([0.05]), 0.05)
        self.assertTrue(isnan(seiffert_mean([1, 1])))

    def test_means_lehmer_mean(self):
        """Test abydos.stats.lehmer_mean."""
        self.assertAlmostEqual(lehmer_mean(self._ones), 1)
        self.assertAlmostEqual(
            lehmer_mean(self._one_to_five), 3.6666666666666665
        )
        self.assertAlmostEqual(
            lehmer_mean(self._onethreefive), 4.066666666666666
        )
        self.assertAlmostEqual(lehmer_mean(self._floats), 0.5418918918918919)

    def test_means_heronian_mean(self):
        """Test abydos.stats.heronian_mean."""
        self.assertAlmostEqual(heronian_mean(self._ones), 1)
        self.assertAlmostEqual(heronian_mean(self._zeros), 0)
        self.assertAlmostEqual(
            heronian_mean(self._one_to_five), 2.8421165194322837
        )
        self.assertAlmostEqual(
            heronian_mean(self._onethreefive), 2.7436226811701165
        )
        self.assertAlmostEqual(
            heronian_mean(self._floats), 0.33526945542427006
        )

    def test_means_hoelder_mean(self):
        """Test abydos.stats.hoelder_mean."""
        self.assertAlmostEqual(hoelder_mean(self._ones), 1)
        self.assertAlmostEqual(hoelder_mean(self._zeros), 0)
        self.assertAlmostEqual(
            hoelder_mean(self._one_to_five), 3.3166247903554
        )
        self.assertAlmostEqual(
            hoelder_mean(self._onethreefive), 3.492849839314596
        )
        self.assertAlmostEqual(hoelder_mean(self._floats), 0.4477722635447623)
        self.assertAlmostEqual(
            hoelder_mean(self._floats, 0), gmean(self._floats)
        )

    def test_means_agmean(self):
        """Test abydos.stats.agmean."""
        self.assertAlmostEqual(agmean(self._ones), 1)
        self.assertAlmostEqual(agmean(self._zeros), 0)
        self.assertAlmostEqual(agmean(self._one_to_five), 2.799103662640505)
        self.assertAlmostEqual(agmean(self._onethreefive), 2.6764865062631356)
        self.assertAlmostEqual(agmean(self._floats), 0.32800436242611486)
        self.assertTrue(isnan(agmean(self._has_inf)))

    def test_means_ghmean(self):
        """Test abydos.stats.ghmean."""
        self.assertAlmostEqual(ghmean(self._ones), 1)
        self.assertAlmostEqual(ghmean(self._one_to_five), 2.3839666656453167)
        self.assertAlmostEqual(ghmean(self._onethreefive), 2.0740491019412035)
        self.assertAlmostEqual(ghmean(self._floats), 0.2536468771476393)
        self.assertTrue(isnan(ghmean(self._has_inf)))

    def test_means_aghmean(self):
        """Test abydos.stats.aghmean."""
        self.assertAlmostEqual(aghmean(self._ones), 1)
        self.assertAlmostEqual(aghmean(self._one_to_five), 2.5769530579812563)
        self.assertAlmostEqual(aghmean(self._onethreefive), 2.3520502484275387)
        self.assertAlmostEqual(aghmean(self._floats), 0.28841285333045547)
        self.assertTrue(isnan(aghmean(self._has_inf)))

    def test_means_midrange(self):
        """Test abydos.stats.midrange."""
        self.assertAlmostEqual(midrange(self._ones), 1)
        self.assertAlmostEqual(midrange(self._zeros), 0)
        self.assertAlmostEqual(midrange(self._one_to_five), 3)
        self.assertAlmostEqual(midrange(self._onethreefive), 3)
        self.assertAlmostEqual(midrange(self._floats), 0.45)

    def test_means_median(self):
        """Test abydos.stats.median."""
        self.assertAlmostEqual(median(self._ones), 1)
        self.assertAlmostEqual(median(self._zeros), 0)
        self.assertAlmostEqual(median(self._one_to_five), 3)
        self.assertAlmostEqual(median(self._onethreefive), 3)
        self.assertAlmostEqual(median(self._floats), 0.25)
        self.assertAlmostEqual(median([0, 2, 4, 8]), 3)
        self.assertAlmostEqual(median([0.01, 0.2, 0.4, 5]), 0.3)

    def test_means_mode(self):
        """Test abydos.stats.mode."""
        self.assertEqual(mode(self._ones), 1)
        self.assertEqual(mode(self._zeros), 0)
        self.assertEqual(mode([1, 1, 2, 2, 2]), 2)
        self.assertEqual(mode([1, 5, 5, 2, 5, 2]), 5)

    def test_means_var(self):
        """Test abydos.stats.var."""
        self.assertAlmostEqual(var(self._ones), 0)
        self.assertAlmostEqual(var(self._zeros), 0)
        self.assertAlmostEqual(var(self._one_to_five), 2)
        self.assertAlmostEqual(var(self._onethreefive), 3.2)

    def test_means_std(self):
        """Test abydos.stats.std."""
        self.assertAlmostEqual(std(self._ones), 0)
        self.assertAlmostEqual(std(self._zeros), 0)
        self.assertAlmostEqual(std(self._one_to_five), 2 ** 0.5)
        self.assertAlmostEqual(std(self._onethreefive), 3.2 ** 0.5)


if __name__ == '__main__':
    unittest.main()
