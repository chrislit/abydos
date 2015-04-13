# -*- coding: utf-8 -*-
"""abydos.tests.test_stats

This module contains unit tests for abydos.stats

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
from __future__ import division
import unittest
from abydos.stats import ConfusionTable, amean, gmean, hmean, qmean, cmean, \
    lmean, imean, seiffert_mean, lehmer_mean, heronian_mean, hoelder_mean, \
    agmean, ghmean, aghmean, midrange, median, mode
from math import isnan, sqrt
import numpy as np
from scipy.stats.mstats import hmean, gmean

UNIT_TABLE = ConfusionTable(1, 1, 1, 1)
NULL_TABLE = ConfusionTable(0, 0, 0, 0)
SCALE_TABLE = ConfusionTable(1, 2, 3, 4)
# https://en.wikipedia.org/wiki/Confusion_matrix#Table_of_confusion
CATSNDOGS_TABLE = ConfusionTable(5, 17, 2, 3)
# https://en.wikipedia.org/wiki/Sensitivity_and_specificity#Worked_example
WORKED_EG_TABLE = ConfusionTable(20, 1820, 180, 10)
VERY_POOR_TABLE = ConfusionTable(0, 0, 200, 200)

ALL_TABLES = (UNIT_TABLE, NULL_TABLE, SCALE_TABLE, CATSNDOGS_TABLE,
              WORKED_EG_TABLE, VERY_POOR_TABLE)

#def ct2arrays(ct):
#    y_pred = []
#    y_true = []
#    y_pred += [1]*ct.tpos
#    y_true += [1]*ct.tpos
#    y_pred += [0]*ct.tneg
#    y_true += [0]*ct.tneg
#    y_pred += [1]*ct.fpos
#    y_true += [0]*ct.fpos
#    y_pred += [0]*ct.fneg
#    y_true += [1]*ct.fneg
#    return y_pred, y_true


class ConstructorTestCases(unittest.TestCase):
    """test cases for abydos.stats.ConfusionTable constructors (__init__)
    """
    def test_constructors(self):
        """test abydos.stats.ConfusionTable.__init__ and __eq__
        """
        self.assertEqual(ConfusionTable(), ConfusionTable())
        self.assertEqual(ConfusionTable(), ConfusionTable(0))
        self.assertEqual(ConfusionTable(), ConfusionTable(0, 0))
        self.assertEqual(ConfusionTable(), ConfusionTable(0, 0, 0))
        self.assertEqual(ConfusionTable(), ConfusionTable(0, 0, 0, 0))
        self.assertNotEquals(ConfusionTable(), ConfusionTable(1))
        self.assertNotEquals(ConfusionTable(), ConfusionTable(0, 1))
        self.assertNotEquals(ConfusionTable(), ConfusionTable(0, 0, 1))
        self.assertNotEquals(ConfusionTable(), ConfusionTable(0, 0, 0, 1))

        # test int constructor & __eq__ by value
        self.assertEqual(SCALE_TABLE, ConfusionTable(1, 2, 3, 4))
        # test tuple constructor
        self.assertEqual(SCALE_TABLE, ConfusionTable((1, 2, 3, 4)))
        self.assertEqual(SCALE_TABLE, ConfusionTable((1, 2, 3, 4), 5, 6, 7))
        # test list constructor
        self.assertEqual(SCALE_TABLE, ConfusionTable([1, 2, 3, 4]))
        self.assertEqual(SCALE_TABLE, ConfusionTable([1, 2, 3, 4], 5, 6, 7))
        # test dict constructor
        self.assertEqual(SCALE_TABLE, ConfusionTable({'tp':1, 'tn':2, 'fp':3,
                                                      'fn':4}))
        self.assertEqual(SCALE_TABLE, ConfusionTable({'tp':1, 'tn':2, 'fp':3,
                                                      'fn':4}, 5, 6, 7))
        self.assertEqual(NULL_TABLE, ConfusionTable({}))
        self.assertEqual(NULL_TABLE, ConfusionTable({'pt':1, 'nt':2, 'pf':3,
                                                     'nf':4}))

        # test __eq__ by id()
        self.assertTrue(SCALE_TABLE == SCALE_TABLE)
        self.assertFalse(CATSNDOGS_TABLE == SCALE_TABLE)
        # test __eq__ by tuple
        self.assertTrue(SCALE_TABLE == (1, 2, 3, 4))
        self.assertFalse(CATSNDOGS_TABLE == (1, 2, 3, 4))
        # test __eq__ by list
        self.assertTrue(SCALE_TABLE == [1, 2, 3, 4])
        self.assertFalse(CATSNDOGS_TABLE == [1, 2, 3, 4])
        # test __eq__ by dict
        self.assertTrue(SCALE_TABLE == {'tp':1, 'tn':2, 'fp':3, 'fn':4})
        self.assertFalse(CATSNDOGS_TABLE == {'tp':1, 'tn':2, 'fp':3, 'fn':4})
        # test __eq__ with non-ConfusionTable/tuple/list/dict
        self.assertFalse(SCALE_TABLE == 5)

        # test invalid tuple constructor
        self.assertRaises(AttributeError, ConfusionTable, (1, 2,))


class CastTestCases(unittest.TestCase):
    """test cases for abydos.stats.ConfusionTable cast methods
    """
    def test_tuple(self):
        """test abydos.stats.ConfusionTable.tuple
        """
        self.assertIsInstance(SCALE_TABLE.tuple(), tuple)
        self.assertEqual(SCALE_TABLE.tuple(), (1, 2, 3, 4))
        self.assertEqual(list(SCALE_TABLE.tuple()), [1, 2, 3, 4])

    def test_dict(self):
        """test abydos.stats.ConfusionTable.dict
        """
        self.assertIsInstance(SCALE_TABLE.dict(), dict)
        self.assertEqual(SCALE_TABLE.dict(), {'tp':1, 'tn':2, 'fp':3, 'fn':4})

    def test_str(self):
        """test abydos.stats.ConfusionTable._str_
        """
        self.assertIsInstance(str(SCALE_TABLE), str)
        self.assertEqual(str(SCALE_TABLE), 'tp:1, tn:2, fp:3, fn:4')


class PopulationTestCases(unittest.TestCase):
    """test cases for abydos.stats.ConfusionTable population methods
    """
    def test_correct_pop(self):
        """test abydos.stats.ConfusionTable.correct_pop
        """
        self.assertEqual(UNIT_TABLE.correct_pop(), 2)
        self.assertEqual(NULL_TABLE.correct_pop(), 0)
        self.assertEqual(SCALE_TABLE.correct_pop(), 3)
        self.assertEqual(CATSNDOGS_TABLE.correct_pop(), 22)
        self.assertEqual(WORKED_EG_TABLE.correct_pop(), 1840)

    def test_error_pop(self):
        """test abydos.stats.ConfusionTable.error_pop
        """
        self.assertEqual(UNIT_TABLE.error_pop(), 2)
        self.assertEqual(NULL_TABLE.error_pop(), 0)
        self.assertEqual(SCALE_TABLE.error_pop(), 7)
        self.assertEqual(CATSNDOGS_TABLE.error_pop(), 5)
        self.assertEqual(WORKED_EG_TABLE.error_pop(), 190)

    def test_test_pos_pop(self):
        """test abydos.stats.ConfusionTable.test_pos_pop
        """
        self.assertEqual(UNIT_TABLE.test_pos_pop(), 2)
        self.assertEqual(NULL_TABLE.test_pos_pop(), 0)
        self.assertEqual(SCALE_TABLE.test_pos_pop(), 4)
        self.assertEqual(CATSNDOGS_TABLE.test_pos_pop(), 7)
        self.assertEqual(WORKED_EG_TABLE.test_pos_pop(), 200)

    def test_test_neg_pop(self):
        """test abydos.stats.ConfusionTable.test_neg_pop
        """
        self.assertEqual(UNIT_TABLE.test_neg_pop(), 2)
        self.assertEqual(NULL_TABLE.test_neg_pop(), 0)
        self.assertEqual(SCALE_TABLE.test_neg_pop(), 6)
        self.assertEqual(CATSNDOGS_TABLE.test_neg_pop(), 20)
        self.assertEqual(WORKED_EG_TABLE.test_neg_pop(), 1830)

    def test_cond_pos_pop(self):
        """test abydos.stats.ConfusionTable.cond_pos_pop
        """
        self.assertEqual(UNIT_TABLE.cond_pos_pop(), 2)
        self.assertEqual(NULL_TABLE.cond_pos_pop(), 0)
        self.assertEqual(SCALE_TABLE.cond_pos_pop(), 5)
        self.assertEqual(CATSNDOGS_TABLE.cond_pos_pop(), 8)
        self.assertEqual(WORKED_EG_TABLE.cond_pos_pop(), 30)

    def test_cond_neg_pop(self):
        """test abydos.stats.ConfusionTable.cond_neg_pop
        """
        self.assertEqual(UNIT_TABLE.cond_neg_pop(), 2)
        self.assertEqual(NULL_TABLE.cond_neg_pop(), 0)
        self.assertEqual(SCALE_TABLE.cond_neg_pop(), 5)
        self.assertEqual(CATSNDOGS_TABLE.cond_neg_pop(), 19)
        self.assertEqual(WORKED_EG_TABLE.cond_neg_pop(), 2000)

    def test_population(self):
        """test abydos.stats.ConfusionTable.population
        """
        self.assertEqual(UNIT_TABLE.population(), 4)
        self.assertEqual(NULL_TABLE.population(), 0)
        self.assertEqual(SCALE_TABLE.population(), 10)
        self.assertEqual(CATSNDOGS_TABLE.population(), 27)
        self.assertEqual(WORKED_EG_TABLE.population(), 2030)


class StatisticalRatioTestCases(unittest.TestCase):
    """test cases for abydos.stats.ConfusionTable basic statistical ratio
    methods
    """
    def test_precision(self):
        """test abydos.stats.ConfusionTable.precision
        """
        self.assertEqual(UNIT_TABLE.precision(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.precision()))
        self.assertAlmostEqual(SCALE_TABLE.precision(), 0.25)
        self.assertAlmostEqual(CATSNDOGS_TABLE.precision(), 5/7)
        self.assertAlmostEqual(WORKED_EG_TABLE.precision(), 0.1)

    def test_precision_gain(self):
        """test abydos.stats.ConfusionTable.precision_gain
        """
        self.assertEqual(UNIT_TABLE.precision_gain(), 1)
        self.assertTrue(isnan(NULL_TABLE.precision_gain()))
        self.assertAlmostEqual(SCALE_TABLE.precision_gain(), 0.25/0.5)
        self.assertAlmostEqual(CATSNDOGS_TABLE.precision_gain(), (5/7)/(8/27))
        self.assertAlmostEqual(WORKED_EG_TABLE.precision_gain(), 0.1/(30/2030))

    def test_recall(self):
        """test abydos.stats.ConfusionTable.recall
        """
        self.assertEqual(UNIT_TABLE.recall(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.recall()))
        self.assertAlmostEqual(SCALE_TABLE.recall(), 0.2)
        self.assertAlmostEqual(CATSNDOGS_TABLE.recall(), 5/8)
        self.assertAlmostEqual(WORKED_EG_TABLE.recall(), 2/3)

    def test_specificity(self):
        """test abydos.stats.ConfusionTable.specificity
        """
        self.assertEqual(UNIT_TABLE.specificity(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.specificity()))
        self.assertAlmostEqual(SCALE_TABLE.specificity(), 0.4)
        self.assertAlmostEqual(CATSNDOGS_TABLE.specificity(), 17/19)
        self.assertAlmostEqual(WORKED_EG_TABLE.specificity(), 0.91)

    def test_npv(self):
        """test abydos.stats.ConfusionTable.npv
        """
        self.assertEqual(UNIT_TABLE.npv(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.npv()))
        self.assertAlmostEqual(SCALE_TABLE.npv(), 1/3)
        self.assertAlmostEqual(CATSNDOGS_TABLE.npv(), 17/20)
        self.assertAlmostEqual(WORKED_EG_TABLE.npv(), 182/183)

    def test_fallout(self):
        """test abydos.stats.ConfusionTable.fallout
        """
        self.assertEqual(UNIT_TABLE.fallout(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.fallout()))
        self.assertAlmostEqual(SCALE_TABLE.fallout(), 0.6)
        self.assertAlmostEqual(CATSNDOGS_TABLE.fallout(), 2/19)
        self.assertAlmostEqual(WORKED_EG_TABLE.fallout(), 0.09)

    def test_fdr(self):
        """test abydos.stats.ConfusionTable.fdr
        """
        self.assertEqual(UNIT_TABLE.fdr(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.fdr()))
        self.assertAlmostEqual(SCALE_TABLE.fdr(), 0.75)
        self.assertAlmostEqual(CATSNDOGS_TABLE.fdr(), 2/7)
        self.assertAlmostEqual(WORKED_EG_TABLE.fdr(), 0.9)

    def test_accuracy(self):
        """test abydos.stats.ConfusionTable.accuracy
        """
        self.assertEqual(UNIT_TABLE.accuracy(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.accuracy()))
        self.assertAlmostEqual(SCALE_TABLE.accuracy(), 3/10)
        self.assertAlmostEqual(CATSNDOGS_TABLE.accuracy(), 22/27)
        self.assertAlmostEqual(WORKED_EG_TABLE.accuracy(), 184/203)

    def test_accuracy_gain(self):
        """test abydos.stats.ConfusionTable.accuracy_gain
        """
        self.assertEqual(UNIT_TABLE.accuracy_gain(), 1)
        self.assertTrue(isnan(NULL_TABLE.accuracy_gain()))
        self.assertAlmostEqual(SCALE_TABLE.accuracy_gain(),
                               (3/10)/((5/10)**2+(5/10)**2))
        self.assertAlmostEqual(CATSNDOGS_TABLE.accuracy_gain(),
                               (22/27)/((8/27)**2+(19/27)**2))
        self.assertAlmostEqual(WORKED_EG_TABLE.accuracy_gain(),
                               (184/203)/((30/2030)**2+(2000/2030)**2))

    def test_balanced_accuracy(self):
        """test abydos.stats.ConfusionTable.balanced_accuracy
        """
        self.assertEqual(UNIT_TABLE.balanced_accuracy(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.balanced_accuracy()))
        self.assertAlmostEqual(SCALE_TABLE.balanced_accuracy(), 0.3)
        self.assertAlmostEqual(CATSNDOGS_TABLE.balanced_accuracy(), 231/304)
        self.assertAlmostEqual(WORKED_EG_TABLE.balanced_accuracy(), 473/600)

    def test_informedness(self):
        """test abydos.stats.ConfusionTable.informedness
        """
        self.assertEqual(UNIT_TABLE.informedness(), 0)
        self.assertTrue(isnan(NULL_TABLE.informedness()))
        self.assertAlmostEqual(SCALE_TABLE.informedness(), -0.4)
        self.assertAlmostEqual(CATSNDOGS_TABLE.informedness(), 79/152)
        self.assertAlmostEqual(WORKED_EG_TABLE.informedness(), 2/3-0.09)

    def test_markedness(self):
        """test abydos.stats.ConfusionTable.markedness
        """
        self.assertEqual(UNIT_TABLE.markedness(), 0)
        self.assertTrue(isnan(NULL_TABLE.markedness()))
        self.assertAlmostEqual(SCALE_TABLE.markedness(), -5/12)
        self.assertAlmostEqual(CATSNDOGS_TABLE.markedness(), 79/140)
        self.assertAlmostEqual(WORKED_EG_TABLE.markedness(), 173/1830)


class PrMeansTestCases(unittest.TestCase):
    """test cases for abydos.stats.ConfusionTable precision-recall mean methods
    """
    prre = tuple((tuple((i.precision(), i.recall())) for i in ALL_TABLES))

    def test_pr_amean(self):
        """test abydos.stats.ConfusionTable.pr_amean
        """
        # pylint: disable=no-member
        self.assertEqual(UNIT_TABLE.pr_amean(), np.mean(self.prre[0]))
        self.assertTrue(isnan(NULL_TABLE.pr_amean()))
        self.assertAlmostEqual(SCALE_TABLE.pr_amean(), np.mean(self.prre[2]))
        self.assertAlmostEqual(CATSNDOGS_TABLE.pr_amean(),
                               np.mean(self.prre[3]))
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_amean(),
                               np.mean(self.prre[4]))
        # pylint: enable=no-member

    def test_pr_gmean(self):
        """test abydos.stats.ConfusionTable.pr_gmean
        """
        self.assertEqual(UNIT_TABLE.pr_gmean(), gmean(self.prre[0]))
        self.assertTrue(isnan(NULL_TABLE.pr_gmean()))
        self.assertAlmostEqual(SCALE_TABLE.pr_gmean(), gmean(self.prre[2]))
        self.assertAlmostEqual(CATSNDOGS_TABLE.pr_gmean(), gmean(self.prre[3]))
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_gmean(), gmean(self.prre[4]))

    def test_pr_hmean(self):
        """test abydos.stats.ConfusionTable.pr_hmean
        """
        self.assertEqual(UNIT_TABLE.pr_hmean(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.pr_hmean()))
        self.assertAlmostEqual(SCALE_TABLE.pr_hmean(), hmean(self.prre[2]))
        self.assertAlmostEqual(CATSNDOGS_TABLE.pr_hmean(), hmean(self.prre[3]))
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_hmean(), hmean(self.prre[4]))

    def test_pr_qmean(self):
        """test abydos.stats.ConfusionTable.pr_qmean
        """
        self.assertEqual(UNIT_TABLE.pr_qmean(),
                          sqrt(sum([i**2 for i in self.prre[0]])/2))
        self.assertTrue(isnan(NULL_TABLE.pr_qmean()))
        self.assertAlmostEqual(SCALE_TABLE.pr_qmean(),
                               sqrt(sum([i**2 for i in self.prre[2]])/2))
        self.assertAlmostEqual(CATSNDOGS_TABLE.pr_qmean(),
                               sqrt(sum([i**2 for i in self.prre[3]])/2))
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_qmean(),
                               sqrt(sum([i**2 for i in self.prre[4]])/2))

    def test_pr_cmean(self):
        """test abydos.stats.ConfusionTable.pr_cmean
        """
        self.assertEqual(UNIT_TABLE.pr_cmean(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.pr_cmean()))
        self.assertAlmostEqual(SCALE_TABLE.pr_cmean(), 41/180)
        self.assertAlmostEqual(CATSNDOGS_TABLE.pr_cmean(), 113/168)
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_cmean(), 409/690)

    def test_pr_lmean(self):
        """test abydos.stats.ConfusionTable.pr_lmean
        """
        self.assertEqual(UNIT_TABLE.pr_lmean(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.pr_lmean()))
        self.assertAlmostEqual(SCALE_TABLE.pr_lmean(), 0.2240710058862275)
        self.assertAlmostEqual(CATSNDOGS_TABLE.pr_lmean(), 0.6686496151266621)
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_lmean(), 0.2986983802717959)
        self.assertAlmostEqual(VERY_POOR_TABLE.pr_lmean(), 0.0)

    def test_pr_imean(self):
        """test abydos.stats.ConfusionTable.pr_imean
        """
        self.assertEqual(UNIT_TABLE.pr_imean(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.pr_imean()))
        self.assertAlmostEqual(SCALE_TABLE.pr_imean(), 0.224535791730617)
        self.assertAlmostEqual(CATSNDOGS_TABLE.pr_imean(), 0.6691463467789889)
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_imean(), 0.34277561539033635)
        self.assertTrue(isnan(VERY_POOR_TABLE.pr_imean()))

    def test_pr_seiffert_mean(self):
        """test abydos.stats.ConfusionTable.pr_seiffert_mean
        """
        self.assertTrue(isnan(UNIT_TABLE.pr_seiffert_mean()))
        self.assertTrue(isnan(NULL_TABLE.pr_seiffert_mean()))
        self.assertAlmostEqual(SCALE_TABLE.pr_seiffert_mean(), 0.2245354073)
        self.assertAlmostEqual(CATSNDOGS_TABLE.pr_seiffert_mean(), 0.6691461993)
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_seiffert_mean(), 0.3406355792)
        self.assertTrue(isnan(VERY_POOR_TABLE.pr_seiffert_mean()))

    def test_pr_lehmer_mean(self):
        """test abydos.stats.ConfusionTable.pr_lehmer_mean
        """
        self.assertEqual(UNIT_TABLE.pr_lehmer_mean(3), 0.5)
        self.assertTrue(isnan(NULL_TABLE.pr_lehmer_mean(3)))
        self.assertAlmostEqual(SCALE_TABLE.pr_lehmer_mean(3), 189/820)
        self.assertAlmostEqual(CATSNDOGS_TABLE.pr_lehmer_mean(3), 4275/6328)
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_lehmer_mean(3), 8027/12270)

        self.assertEqual(UNIT_TABLE.pr_lehmer_mean(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.pr_lehmer_mean()))
        self.assertAlmostEqual(SCALE_TABLE.pr_lehmer_mean(), 41/180)
        self.assertAlmostEqual(CATSNDOGS_TABLE.pr_lehmer_mean(), 113/168)
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_lehmer_mean(), 409/690)

        self.assertEqual(UNIT_TABLE.pr_lehmer_mean(2), 0.5)
        self.assertTrue(isnan(NULL_TABLE.pr_lehmer_mean(2)))
        self.assertAlmostEqual(SCALE_TABLE.pr_lehmer_mean(2), 41/180)
        self.assertAlmostEqual(CATSNDOGS_TABLE.pr_lehmer_mean(2), 113/168)
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_lehmer_mean(2), 409/690)

        # check equivalences to other specific means
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_lehmer_mean(0),
                               WORKED_EG_TABLE.pr_hmean())
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_lehmer_mean(0.5),
                               WORKED_EG_TABLE.pr_gmean())
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_lehmer_mean(1),
                               WORKED_EG_TABLE.pr_amean())
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_lehmer_mean(2),
                               WORKED_EG_TABLE.pr_cmean())

    def test_pr_heronian_mean(self):
        """test abydos.stats.ConfusionTable.pr_heronian_mean
        """
        self.assertEqual(UNIT_TABLE.pr_heronian_mean(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.pr_heronian_mean()))
        self.assertAlmostEqual(SCALE_TABLE.pr_heronian_mean(), 0.2245355992)
        self.assertAlmostEqual(CATSNDOGS_TABLE.pr_heronian_mean(), 0.6691462730)
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_heronian_mean(), 0.3416218521)
        self.assertEqual(VERY_POOR_TABLE.pr_heronian_mean(), 0)

    def test_pr_hoelder_mean(self):
        """test abydos.stats.ConfusionTable.pr_hoelder_mean
        """
        self.assertEqual(UNIT_TABLE.pr_hoelder_mean(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.pr_hoelder_mean()))
        self.assertAlmostEqual(SCALE_TABLE.pr_hoelder_mean(),
                               0.22638462845343543)
        self.assertAlmostEqual(CATSNDOGS_TABLE.pr_hoelder_mean(),
                               0.6711293026059334)
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_hoelder_mean(),
                               0.4766783215358364)

        self.assertEqual(UNIT_TABLE.pr_hoelder_mean(0), 0.5)
        self.assertTrue(isnan(NULL_TABLE.pr_hoelder_mean(0)))
        self.assertAlmostEqual(SCALE_TABLE.pr_hoelder_mean(0),
                               0.22360679774997899)
        self.assertAlmostEqual(CATSNDOGS_TABLE.pr_hoelder_mean(0),
                               0.66815310478106094)
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_hoelder_mean(0),
                               0.25819888974716115)

        self.assertEqual(UNIT_TABLE.pr_hoelder_mean(1), 0.5)
        self.assertTrue(isnan(NULL_TABLE.pr_hoelder_mean(1)))
        self.assertAlmostEqual(SCALE_TABLE.pr_hoelder_mean(1), 9/40)
        self.assertAlmostEqual(CATSNDOGS_TABLE.pr_hoelder_mean(1), 75/112)
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_hoelder_mean(1), 23/60)

        self.assertEqual(UNIT_TABLE.pr_hoelder_mean(2), 0.5)
        self.assertTrue(isnan(NULL_TABLE.pr_hoelder_mean(2)))
        self.assertAlmostEqual(SCALE_TABLE.pr_hoelder_mean(2),
                               0.22638462845343543)
        self.assertAlmostEqual(CATSNDOGS_TABLE.pr_hoelder_mean(2),
                               0.6711293026059334)
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_hoelder_mean(2),
                               0.4766783215358364)

        self.assertEqual(UNIT_TABLE.pr_hoelder_mean(3), 0.5)
        self.assertTrue(isnan(NULL_TABLE.pr_hoelder_mean(3)))
        self.assertAlmostEqual(SCALE_TABLE.pr_hoelder_mean(3),
                               0.2277441728906747)
        self.assertAlmostEqual(CATSNDOGS_TABLE.pr_hoelder_mean(3),
                               0.6726059172248808)
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_hoelder_mean(3),
                               0.5297282909519099)

        # check equivalences to other specific means
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_hoelder_mean(-1),
                               WORKED_EG_TABLE.pr_hmean())
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_hoelder_mean(0),
                               WORKED_EG_TABLE.pr_gmean())
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_hoelder_mean(1),
                               WORKED_EG_TABLE.pr_amean())
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_hoelder_mean(2),
                               WORKED_EG_TABLE.pr_qmean())

    def test_pr_agmean(self):
        """test abydos.stats.ConfusionTable.pr_agmean
        Test values computed via http://arithmeticgeometricmean.blogspot.de/
        """
        self.assertEqual(UNIT_TABLE.pr_agmean(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.pr_agmean()))
        self.assertAlmostEqual(SCALE_TABLE.pr_agmean(), 0.2243028580287603)
        self.assertAlmostEqual(CATSNDOGS_TABLE.pr_agmean(), 0.6688977735879823)
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_agmean(), 0.3176780357448827)

    def test_pr_ghmean(self):
        """test abydos.stats.ConfusionTable.pr_ghmean
        """
        self.assertEqual(UNIT_TABLE.pr_ghmean(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.pr_ghmean()))
        self.assertAlmostEqual(SCALE_TABLE.pr_ghmean(), 0.2229128974)
        self.assertAlmostEqual(CATSNDOGS_TABLE.pr_ghmean(), 0.6674092650)
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_ghmean(), 0.2098560781)

    def test_pr_aghmean(self):
        """test abydos.stats.ConfusionTable.pr_aghmean
        """
        self.assertEqual(UNIT_TABLE.pr_aghmean(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.pr_aghmean()))
        self.assertAlmostEqual(SCALE_TABLE.pr_aghmean(), 0.2236067977)
        self.assertAlmostEqual(CATSNDOGS_TABLE.pr_aghmean(), 0.6681531047)
        self.assertAlmostEqual(WORKED_EG_TABLE.pr_aghmean(), 0.2581988897)


class StatisticalMeasureTestCases(unittest.TestCase):
    """test cases for abydos.stats.ConfusionTable statistical measure methods
    """
    prre = tuple((tuple((i.precision(), i.recall())) for i in ALL_TABLES))

    def test_fbeta_score(self):
        """test abydos.stats.ConfusionTable.fbeta_score
        """
        self.assertEqual(UNIT_TABLE.fbeta_score(1), 0.5)
        self.assertTrue(isnan(NULL_TABLE.fbeta_score(1)))
        self.assertAlmostEqual(SCALE_TABLE.fbeta_score(1), 2/9)
        self.assertAlmostEqual(CATSNDOGS_TABLE.fbeta_score(1), 2/3)
        self.assertAlmostEqual(WORKED_EG_TABLE.fbeta_score(1), 4/23)
        self.assertRaises(AttributeError, UNIT_TABLE.fbeta_score, -1)

    def test_f2_score(self):
        """test abydos.stats.ConfusionTable.f2_score
        """
        self.assertEqual(UNIT_TABLE.f2_score(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.f2_score()))
        self.assertAlmostEqual(SCALE_TABLE.f2_score(), 5/24)
        self.assertAlmostEqual(CATSNDOGS_TABLE.f2_score(), 25/39)
        self.assertAlmostEqual(WORKED_EG_TABLE.f2_score(), 5/16)

    def test_fhalf_score(self):
        """test abydos.stats.ConfusionTable.fhalf_score
        """
        self.assertEqual(UNIT_TABLE.fhalf_score(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.fhalf_score()))
        self.assertAlmostEqual(SCALE_TABLE.fhalf_score(), 5/21)
        self.assertAlmostEqual(CATSNDOGS_TABLE.fhalf_score(), 25/36)
        self.assertAlmostEqual(WORKED_EG_TABLE.fhalf_score(), 10/83)

    def test_e_score(self):
        """test abydos.stats.ConfusionTable.e_score
        """
        self.assertEqual(UNIT_TABLE.e_score(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.e_score()))
        self.assertAlmostEqual(SCALE_TABLE.e_score(), 7/9)
        self.assertAlmostEqual(CATSNDOGS_TABLE.e_score(), 1/3)
        self.assertAlmostEqual(WORKED_EG_TABLE.e_score(), 19/23)

    def test_f1_score(self):
        """test abydos.stats.ConfusionTable.f1_score
        """
        self.assertEqual(UNIT_TABLE.f1_score(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.f1_score()))
        self.assertAlmostEqual(SCALE_TABLE.f1_score(), 2/9)
        self.assertAlmostEqual(CATSNDOGS_TABLE.f1_score(), 2/3)
        self.assertAlmostEqual(WORKED_EG_TABLE.f1_score(), 4/23)

    def test_f_measure(self):
        """test abydos.stats.ConfusionTable.f_measure
        """
        self.assertEqual(UNIT_TABLE.f_measure(), 0.5)
        self.assertTrue(isnan(NULL_TABLE.f_measure()))
        self.assertAlmostEqual(SCALE_TABLE.f_measure(), 2/9)
        self.assertAlmostEqual(CATSNDOGS_TABLE.f_measure(), 2/3)
        self.assertAlmostEqual(WORKED_EG_TABLE.f_measure(), 4/23)

    def test_g_measure(self):
        """test abydos.stats.ConfusionTable.g_measure
        """
        self.assertEqual(UNIT_TABLE.g_measure(), gmean(self.prre[0]))
        self.assertTrue(isnan(NULL_TABLE.g_measure()))
        self.assertAlmostEqual(SCALE_TABLE.g_measure(), gmean(self.prre[2]))
        self.assertAlmostEqual(CATSNDOGS_TABLE.g_measure(), gmean(self.prre[3]))
        self.assertAlmostEqual(WORKED_EG_TABLE.g_measure(), gmean(self.prre[4]))

    def test_mcc(self):
        """test abydos.stats.ConfusionTable.mcc
        """
        self.assertEqual(UNIT_TABLE.mcc(), 0)
        self.assertTrue(isnan(NULL_TABLE.mcc()))
        self.assertAlmostEqual(SCALE_TABLE.mcc(), -10/sqrt(600))
        self.assertAlmostEqual(CATSNDOGS_TABLE.mcc(), 79/sqrt(21280))
        self.assertAlmostEqual(WORKED_EG_TABLE.mcc(), 34600/sqrt(21960000000))

    def test_significance(self):
        """test abydos.stats.ConfusionTable.significance
        """
        self.assertEqual(UNIT_TABLE.significance(), 0)
        self.assertTrue(isnan(NULL_TABLE.significance()))
        self.assertAlmostEqual(SCALE_TABLE.significance(), 5/3)
        self.assertAlmostEqual(CATSNDOGS_TABLE.significance(), 79**2/21280*27)
        self.assertAlmostEqual(WORKED_EG_TABLE.significance(),
                               34600**2/21960000000*2030)

    def test_kappa_statistic(self):
        """test abydos.stats.ConfusionTable.kappa_statistic
        """
        quick_kappa = lambda acc, racc: (acc-racc)/(1-racc)

        self.assertEqual(UNIT_TABLE.kappa_statistic(), 0)
        self.assertTrue(isnan(NULL_TABLE.kappa_statistic()))
        self.assertAlmostEqual(SCALE_TABLE.kappa_statistic(),
                               quick_kappa((3/10), (1/2)))
        self.assertAlmostEqual(CATSNDOGS_TABLE.kappa_statistic(),
                               quick_kappa((22/27), (436/27**2)))
        self.assertAlmostEqual(WORKED_EG_TABLE.kappa_statistic(),
                               quick_kappa((184/203),
                                           (((2000*1830)+6000)/2030**2)))


class MeansTestCases(unittest.TestCase):
    """test cases for abydos.stats mean functions
    """
    def test_means(self):
        """test abydos.stats means
        """
        _ones = [1, 1, 1, 1, 1]
        _zeros = [0, 0, 0, 0, 0]
        _one_to_five = [1, 2, 3, 4, 5]
        _onethreefive = [1, 1, 3, 5, 5]
        _floats = [0.5, 0.8, 0.1, 0.2, 0.25]

        self.assertAlmostEqual(amean(_ones), 1)
        self.assertAlmostEqual(amean(_zeros), 0)
        self.assertAlmostEqual(amean(_one_to_five), 3)
        self.assertAlmostEqual(amean(_onethreefive), 3)
        self.assertAlmostEqual(amean(_floats), 0.37)

        self.assertAlmostEqual(gmean(_ones), 1)
        self.assertAlmostEqual(gmean(_zeros), 0)
        self.assertAlmostEqual(gmean(_one_to_five), 2.605171084697352)
        self.assertAlmostEqual(gmean(_onethreefive), 2.3714406097793117)
        self.assertAlmostEqual(gmean(_floats), 0.2885399811814427)

        self.assertAlmostEqual(hmean(_ones), 1)
        self.assertAlmostEqual(hmean(_zeros), 0)
        self.assertAlmostEqual(hmean(_one_to_five), 2.18978102189781)
        self.assertAlmostEqual(hmean(_onethreefive), 1.8292682926829265)
        self.assertAlmostEqual(hmean(_floats), 0.2247191011235955)
        self.assertEqual(hmean([0, 1, 2]), 0)
        self.assertEqual(hmean([1, 2, 3, 0]), 0)
        self.assertTrue(isnan(hmean([0, 0, 1, 2])))
        self.assertTrue(isnan(hmean([1, 0, 2, 0, 3])))
        self.assertTrue(isnan(hmean([1, 0, 2, 0, 3, 0])))
        self.assertTrue(isnan(hmean([1, 0, 2, 0, 3, 0, 0])))
        self.assertEqual(hmean([0, 0]), 0)
        self.assertEqual(hmean([0, 0, 0, 0]), 0)
        self.assertEqual(hmean([1, 1, 1, 1, 1]), 1)
        self.assertEqual(hmean([5, 5, 5, 5, 5]), 5)

        self.assertAlmostEqual(qmean(_ones), 1)
        self.assertAlmostEqual(qmean(_zeros), 0)
        self.assertAlmostEqual(qmean(_one_to_five), 3.3166247903554)
        self.assertAlmostEqual(qmean(_onethreefive), 3.492849839314596)
        self.assertAlmostEqual(qmean(_floats), 0.4477722635447623)

        self.assertAlmostEqual(cmean(_ones), 1)
        self.assertAlmostEqual(cmean(_one_to_five), 3.6666666666666665)
        self.assertAlmostEqual(cmean(_onethreefive), 4.066666666666666)
        self.assertAlmostEqual(cmean(_floats), 0.5418918918918919)

        self.assertAlmostEqual(lmean(_one_to_five), 2.6739681320855766)
        self.assertAlmostEqual(lmean(_floats), 0.301387278840469)
        self.assertRaises(AttributeError, lmean, (1, 1))
        self.assertRaises(AttributeError, lmean, (0.15, 0.15))

        _2ones = [1, 1]
        _2zeros = [0, 0]
        _onetwo = [1, 2]
        _2floats = [0.5, 0.25]

        self.assertRaises(AttributeError, imean, _ones)
        self.assertRaises(AttributeError, imean, _zeros)
        self.assertRaises(AttributeError, imean, _one_to_five)
        self.assertRaises(AttributeError, imean, _onethreefive)
        self.assertRaises(AttributeError, imean, _floats)
        self.assertAlmostEqual(imean(_2ones), 1)
        self.assertTrue(isnan(imean(_2zeros)))
        self.assertAlmostEqual(imean(_onetwo), 1.4715177646857693)
        self.assertAlmostEqual(imean(_2floats), 0.36787944117144233)
        self.assertEqual(imean([1]), 1)
        self.assertEqual(imean([0.05]), 0.05)

        self.assertRaises(AttributeError, seiffert_mean, _ones)
        self.assertRaises(AttributeError, seiffert_mean, _zeros)
        self.assertRaises(AttributeError, seiffert_mean, _one_to_five)
        self.assertRaises(AttributeError, seiffert_mean, _onethreefive)
        self.assertRaises(AttributeError, seiffert_mean, _floats)
        self.assertAlmostEqual(seiffert_mean(_onetwo), 1.4712939827611637)
        self.assertAlmostEqual(seiffert_mean(_2floats), 0.36782349569029094)
        self.assertEqual(seiffert_mean([1]), 1)
        self.assertEqual(seiffert_mean([0.05]), 0.05)

        self.assertAlmostEqual(lehmer_mean(_ones), 1)
        self.assertAlmostEqual(lehmer_mean(_one_to_five), 3.6666666666666665)
        self.assertAlmostEqual(lehmer_mean(_onethreefive), 4.066666666666666)
        self.assertAlmostEqual(lehmer_mean(_floats), 0.5418918918918919)

        self.assertAlmostEqual(heronian_mean(_ones), 1)
        self.assertAlmostEqual(heronian_mean(_zeros), 0)
        self.assertAlmostEqual(heronian_mean(_one_to_five), 2.8421165194322837)
        self.assertAlmostEqual(heronian_mean(_onethreefive), 2.7436226811701165)
        self.assertAlmostEqual(heronian_mean(_floats), 0.33526945542427006)

        self.assertAlmostEqual(hoelder_mean(_ones), 1)
        self.assertAlmostEqual(hoelder_mean(_zeros), 0)
        self.assertAlmostEqual(hoelder_mean(_one_to_five), 3.3166247903554)
        self.assertAlmostEqual(hoelder_mean(_onethreefive), 3.492849839314596)
        self.assertAlmostEqual(hoelder_mean(_floats), 0.4477722635447623)

        self.assertAlmostEqual(agmean(_ones), 1)
        self.assertAlmostEqual(agmean(_zeros), 0)
        self.assertAlmostEqual(agmean(_one_to_five), 2.799103662640505)
        self.assertAlmostEqual(agmean(_onethreefive), 2.6764865062631356)
        self.assertAlmostEqual(agmean(_floats), 0.32800436242611486)

        self.assertAlmostEqual(ghmean(_ones), 1)
        self.assertAlmostEqual(ghmean(_one_to_five), 2.3839666656453167)
        self.assertAlmostEqual(ghmean(_onethreefive), 2.0740491019412035)
        self.assertAlmostEqual(ghmean(_floats), 0.2536468771476393)

        self.assertAlmostEqual(aghmean(_ones), 1)
        self.assertAlmostEqual(aghmean(_one_to_five), 2.5769530579812563)
        self.assertAlmostEqual(aghmean(_onethreefive), 2.3520502484275387)
        self.assertAlmostEqual(aghmean(_floats), 0.28841285333045547)

        self.assertAlmostEqual(midrange(_ones), 1)
        self.assertAlmostEqual(midrange(_zeros), 0)
        self.assertAlmostEqual(midrange(_one_to_five), 3)
        self.assertAlmostEqual(midrange(_onethreefive), 3)
        self.assertAlmostEqual(midrange(_floats), 0.45)

        self.assertAlmostEqual(median(_ones), 1)
        self.assertAlmostEqual(median(_zeros), 0)
        self.assertAlmostEqual(median(_one_to_five), 3)
        self.assertAlmostEqual(median(_onethreefive), 3)
        self.assertAlmostEqual(median(_floats), 0.25)
        self.assertAlmostEqual(median([0, 2, 4, 8]), 3)
        self.assertAlmostEqual(median([0.01, 0.2, 0.4, 5]), 0.3)

        self.assertEqual(mode(_ones), 1)
        self.assertEqual(mode(_zeros), 0)
        self.assertEqual(mode([1, 1, 2, 2, 2]), 2)
        self.assertEqual(mode([1, 5, 5, 2, 5, 2]), 5)


if __name__ == '__main__':
    unittest.main()
