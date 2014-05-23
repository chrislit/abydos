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
from abydos.stats import ConfusionTable

UNIT_TABLE = ConfusionTable(1, 1, 1, 1)
NULL_TABLE = ConfusionTable(0, 0, 0, 0)
SCALE_TABLE = ConfusionTable(1, 2, 3, 4)
# https://en.wikipedia.org/wiki/Confusion_matrix#Table_of_confusion
CATSNDOGS_TABLE = ConfusionTable(5, 17, 2, 3)
# https://en.wikipedia.org/wiki/Sensitivity_and_specificity#Worked_example
WORKED_EG_TABLE = ConfusionTable(20, 1820, 180, 10)

tables = (UNIT_TABLE, NULL_TABLE, SCALE_TABLE, CATSNDOGS_TABLE, WORKED_EG_TABLE)
def ct2arrays(ct):
    y_pred = []
    y_true = []
    y_pred += [1]*ct.tpos
    y_true += [1]*ct.tpos
    y_pred += [0]*ct.tneg
    y_true += [0]*ct.tneg
    y_pred += [1]*ct.fpos
    y_true += [0]*ct.fpos
    y_pred += [0]*ct.fneg
    y_true += [1]*ct.fneg
    return y_pred, y_true

# pylint: disable=R0904
# pylint: disable=R0915
class ConstructorTestCases(unittest.TestCase):
    """test cases for abydos.stats.ConfusionTable constructors (__init__)
    """
    def test_constructors(self):
        """test abydos.stats.ConfusionTable.__init__ and __eq__
        """
        self.assertEquals(ConfusionTable(), ConfusionTable())
        self.assertEquals(ConfusionTable(), ConfusionTable(0))
        self.assertEquals(ConfusionTable(), ConfusionTable(0, 0))
        self.assertEquals(ConfusionTable(), ConfusionTable(0, 0, 0))
        self.assertEquals(ConfusionTable(), ConfusionTable(0, 0, 0, 0))
        self.assertNotEquals(ConfusionTable(), ConfusionTable(1))
        self.assertNotEquals(ConfusionTable(), ConfusionTable(0, 1))
        self.assertNotEquals(ConfusionTable(), ConfusionTable(0, 0, 1))
        self.assertNotEquals(ConfusionTable(), ConfusionTable(0, 0, 0, 1))

        # test __eq__ by id()
        self.assertEquals(SCALE_TABLE, SCALE_TABLE)
        # test int constructor & __eq__ by value
        self.assertEquals(SCALE_TABLE, ConfusionTable(1, 2, 3, 4))
        # test tuple constructor
        self.assertEquals(SCALE_TABLE, ConfusionTable((1, 2, 3, 4)))
        self.assertEquals(SCALE_TABLE, ConfusionTable((1, 2, 3, 4),
                                                          5, 6, 7))
        # test list constructor
        self.assertEquals(SCALE_TABLE, ConfusionTable([1, 2, 3, 4]))
        self.assertEquals(SCALE_TABLE, ConfusionTable([1, 2, 3, 4],
                                                          5, 6, 7))
        # test dict constructor
        self.assertEquals(SCALE_TABLE, ConfusionTable({'tp':1, 'tn':2,
                                                           'fp':3, 'fn':4}))
        self.assertEquals(SCALE_TABLE, ConfusionTable({'tp':1, 'tn':2,
                                                           'fp':3, 'fn':4}, 
                                                          5, 6, 7))

        # test __eq__ by tuple
        self.assertEquals(SCALE_TABLE, (1, 2, 3, 4))
        # test __eq__ by list
        self.assertEquals(SCALE_TABLE, [1, 2, 3, 4])
        # test __eq__ by dict
        self.assertEquals(SCALE_TABLE, {'tp':1, 'tn':2, 'fp':3, 'fn':4})


class CastTestCases(unittest.TestCase):
    """test cases for abydos.stats.ConfusionTable cast methods
    """
    def test_tuple(self):
        """test abydos.stats.ConfusionTable.tuple
        """
        self.assertIsInstance(SCALE_TABLE.tuple(), tuple)
        self.assertEquals(SCALE_TABLE.tuple(), (1, 2, 3, 4))
        self.assertEquals(list(SCALE_TABLE.tuple()), [1, 2, 3, 4])

    def test_dict(self):
        """test abydos.stats.ConfusionTable.dict
        """
        self.assertIsInstance(SCALE_TABLE.dict(), dict)
        self.assertEquals(SCALE_TABLE.dict(), {'tp':1, 'tn':2, 'fp':3, 'fn':4})


class PopulationTestCases(unittest.TestCase):
    """test cases for abydos.stats.ConfusionTable population methods
    """
    def test_correct_pop(self):
        """test abydos.stats.ConfusionTable.correct_pop
        """
        self.assertEquals(UNIT_TABLE.correct_pop(), 2)
        self.assertEquals(NULL_TABLE.correct_pop(), 0)
        self.assertEquals(SCALE_TABLE.correct_pop(), 3)
        self.assertEquals(CATSNDOGS_TABLE.correct_pop(), 22)
        self.assertEquals(WORKED_EG_TABLE.correct_pop(), 1840)

    def test_error_pop(self):
        """test abydos.stats.ConfusionTable.error_pop
        """
        self.assertEquals(UNIT_TABLE.error_pop(), 2)
        self.assertEquals(NULL_TABLE.error_pop(), 0)
        self.assertEquals(SCALE_TABLE.error_pop(), 7)
        self.assertEquals(CATSNDOGS_TABLE.error_pop(), 5)
        self.assertEquals(WORKED_EG_TABLE.error_pop(), 190)

    def test_test_pos_pop(self):
        """test abydos.stats.ConfusionTable.test_pos_pop
        """
        self.assertEquals(UNIT_TABLE.test_pos_pop(), 2)
        self.assertEquals(NULL_TABLE.test_pos_pop(), 0)
        self.assertEquals(SCALE_TABLE.test_pos_pop(), 4)
        self.assertEquals(CATSNDOGS_TABLE.test_pos_pop(), 7)
        self.assertEquals(WORKED_EG_TABLE.test_pos_pop(), 200)

    def test_test_neg_pop(self):
        """test abydos.stats.ConfusionTable.test_neg_pop
        """
        self.assertEquals(UNIT_TABLE.test_neg_pop(), 2)
        self.assertEquals(NULL_TABLE.test_neg_pop(), 0)
        self.assertEquals(SCALE_TABLE.test_neg_pop(), 6)
        self.assertEquals(CATSNDOGS_TABLE.test_neg_pop(), 20)
        self.assertEquals(WORKED_EG_TABLE.test_neg_pop(), 1830)

    def test_cond_pos_pop(self):
        """test abydos.stats.ConfusionTable.cond_pos_pop
        """
        self.assertEquals(UNIT_TABLE.cond_pos_pop(), 2)
        self.assertEquals(NULL_TABLE.cond_pos_pop(), 0)
        self.assertEquals(SCALE_TABLE.cond_pos_pop(), 5)
        self.assertEquals(CATSNDOGS_TABLE.cond_pos_pop(), 8)
        self.assertEquals(WORKED_EG_TABLE.cond_pos_pop(), 30)

    def test_cond_neg_pop(self):
        """test abydos.stats.ConfusionTable.cond_neg_pop
        """
        self.assertEquals(UNIT_TABLE.cond_neg_pop(), 2)
        self.assertEquals(NULL_TABLE.cond_neg_pop(), 0)
        self.assertEquals(SCALE_TABLE.cond_neg_pop(), 5)
        self.assertEquals(CATSNDOGS_TABLE.cond_neg_pop(), 19)
        self.assertEquals(WORKED_EG_TABLE.cond_neg_pop(), 2000)

    def test_population(self):
        """test abydos.stats.ConfusionTable.population
        """
        self.assertEquals(UNIT_TABLE.population(), 4)
        self.assertEquals(NULL_TABLE.population(), 0)
        self.assertEquals(SCALE_TABLE.population(), 10)
        self.assertEquals(CATSNDOGS_TABLE.population(), 27)
        self.assertEquals(WORKED_EG_TABLE.population(), 2030)


class StatisticalRatioTestCases(unittest.TestCase):
    """test cases for abydos.stats.ConfusionTable basic statistical ratio
    methods
    """
    def test_precision(self):
        """test abydos.stats.ConfusionTable.precision
        """
        self.assertEquals(UNIT_TABLE.precision(), 0.5)
        #self.assertEquals(NULL_TABLE.precision(), )
        self.assertAlmostEqual(SCALE_TABLE.precision(), 0.25)
        self.assertAlmostEqual(CATSNDOGS_TABLE.precision(), 5/7)
        self.assertAlmostEqual(WORKED_EG_TABLE.precision(), 0.1)

    def test_recall(self):
        """test abydos.stats.ConfusionTable.recall
        """
        self.assertEquals(UNIT_TABLE.recall(), 0.5)
        #self.assertEquals(NULL_TABLE.recall(), )
        self.assertAlmostEqual(SCALE_TABLE.recall(), 0.2)
        self.assertAlmostEqual(CATSNDOGS_TABLE.recall(), 5/8)
        self.assertAlmostEqual(WORKED_EG_TABLE.recall(), 2/3)

    def test_specificity(self):
        """test abydos.stats.ConfusionTable.specificity
        """
        self.assertEquals(UNIT_TABLE.specificity(), 0.5)
        #self.assertEquals(NULL_TABLE.specificity(), )
        self.assertAlmostEqual(SCALE_TABLE.specificity(), 0.4)
        self.assertAlmostEqual(CATSNDOGS_TABLE.specificity(), 17/19)
        self.assertAlmostEqual(WORKED_EG_TABLE.specificity(), 0.91)

    def test_npv(self):
        """test abydos.stats.ConfusionTable.npv
        """
        self.assertEquals(UNIT_TABLE.npv(), 0.5)
        #self.assertEquals(NULL_TABLE.npv(), )
        self.assertAlmostEqual(SCALE_TABLE.npv(), 1/3)
        self.assertAlmostEqual(CATSNDOGS_TABLE.npv(), 17/20)
        self.assertAlmostEqual(WORKED_EG_TABLE.npv(), 182/183)

    def test_fallout(self):
        """test abydos.stats.ConfusionTable.fallout
        """
        self.assertEquals(UNIT_TABLE.fallout(), 0.5)
        #self.assertEquals(NULL_TABLE.fallout(), )
        self.assertAlmostEqual(SCALE_TABLE.fallout(), 0.6)
        self.assertAlmostEqual(CATSNDOGS_TABLE.fallout(), 2/19)
        self.assertAlmostEqual(WORKED_EG_TABLE.fallout(), 0.09)

    def test_fdr(self):
        """test abydos.stats.ConfusionTable.fdr
        """
        self.assertEquals(UNIT_TABLE.fdr(), 0.5)
        #self.assertEquals(NULL_TABLE.fdr(), )
        self.assertAlmostEqual(SCALE_TABLE.fdr(), 0.75)
        self.assertAlmostEqual(CATSNDOGS_TABLE.fdr(), 2/7)
        self.assertAlmostEqual(WORKED_EG_TABLE.fdr(), 0.9)

    def test_accuracy(self):
        """test abydos.stats.ConfusionTable.accuracy
        """
        self.assertEquals(UNIT_TABLE.accuracy(), 0.5)
        # self.assertEquals(NULL_TABLE.accuracy(), )
        self.assertAlmostEqual(SCALE_TABLE.accuracy(), 3/10)
        self.assertAlmostEqual(CATSNDOGS_TABLE.accuracy(), 22/27)
        self.assertAlmostEqual(WORKED_EG_TABLE.accuracy(), 184/203)

    def test_balanced_accuracy(self):
        """test abydos.stats.ConfusionTable.balanced_accuracy
        """
        self.assertEquals(UNIT_TABLE.balanced_accuracy(), 0.5)
        #self.assertEquals(NULL_TABLE.balanced_accuracy(), )
        self.assertAlmostEqual(SCALE_TABLE.balanced_accuracy(), 0.3)
        self.assertAlmostEqual(CATSNDOGS_TABLE.balanced_accuracy(), 231/304)
        self.assertAlmostEqual(WORKED_EG_TABLE.balanced_accuracy(), 473/600)

    def test_informedness(self):
        """test abydos.stats.ConfusionTable.informedness
        """
        self.assertEquals(UNIT_TABLE.informedness(), 0)
        #self.assertEquals(NULL_TABLE.informedness(), )
        self.assertAlmostEqual(SCALE_TABLE.informedness(), -0.4)
        self.assertAlmostEqual(CATSNDOGS_TABLE.informedness(), 79/152)
        self.assertAlmostEqual(WORKED_EG_TABLE.informedness(), 2/3-0.09)

    def test_markedness(self):
        """test abydos.stats.ConfusionTable.markedness
        """
        self.assertEquals(UNIT_TABLE.markedness(), 0)
        #self.assertEquals(NULL_TABLE.markedness(), )
        self.assertAlmostEqual(SCALE_TABLE.markedness(), -5/12)
        self.assertAlmostEqual(CATSNDOGS_TABLE.markedness(), 79/140)
        self.assertAlmostEqual(WORKED_EG_TABLE.markedness(), 173/1830)


class PrMeansTestCases(unittest.TestCase):
    """test cases for abydos.stats.ConfusionTable precision-recall mean methods
    """
    def test_pr_mean(self):
        """test abydos.stats.ConfusionTable.pr_mean
        """
        pass

    def test_pr_gmean(self):
        """test abydos.stats.ConfusionTable.pr_gmean
        """
        pass

    def test_pr_hmean(self):
        """test abydos.stats.ConfusionTable.pr_hmean
        """
        pass

    def test_pr_qmean(self):
        """test abydos.stats.ConfusionTable.pr_qmean
        """
        pass

    def test_pr_lmean(self):
        """test abydos.stats.ConfusionTable.pr_lmean
        """
        pass

    def test_pr_cmean(self):
        """test abydos.stats.ConfusionTable.pr_cmean
        """
        pass

    def test_pr_imean(self):
        """test abydos.stats.ConfusionTable.pr_imean
        """
        pass

    def test_pr_pmean(self):
        """test abydos.stats.ConfusionTable.pr_pmean
        """
        pass


class StatisticalMeasureTestCases(unittest.TestCase):
    """test cases for abydos.stats.ConfusionTable statistical measure methods
    """
    def test_fbeta_score(self):
        """test abydos.stats.ConfusionTable.fbeta_score
        """
        self.assertEquals(UNIT_TABLE.fbeta_score(1), 0.5)
        #self.assertEquals(NULL_TABLE.fbeta_score(1), )
        self.assertAlmostEqual(SCALE_TABLE.fbeta_score(1), 2/9)
        self.assertAlmostEqual(CATSNDOGS_TABLE.fbeta_score(1), 2/3)
        #self.assertAlmostEqual(WORKED_EG_TABLE.fbeta_score(1), 0.17391304347826089)

    def test_f2_score(self):
        """test abydos.stats.ConfusionTable.f2_score
        """
        self.assertEquals(UNIT_TABLE.f2_score(), 0.5)
        #self.assertEquals(NULL_TABLE.f2_score(), )
        #self.assertAlmostEqual(SCALE_TABLE.f2_score(), 0.23809523809523808)
        #self.assertAlmostEqual(CATSNDOGS_TABLE.f2_score(), 0.69444444444444442)
        #self.assertAlmostEqual(WORKED_EG_TABLE.f2_score(), 0.3125)

    def test_fhalf_score(self):
        """test abydos.stats.ConfusionTable.fhalf_score
        """
        self.assertEquals(UNIT_TABLE.fhalf_score(), 0.5)
        #self.assertEquals(NULL_TABLE.fhalf_score(), )
        #self.assertAlmostEqual(SCALE_TABLE.fhalf_score(), 0.20833333333333334)
        #self.assertAlmostEqual(CATSNDOGS_TABLE.fhalf_score(), 0.64102564102564108)
        #self.assertAlmostEqual(WORKED_EG_TABLE.fhalf_score(), 0.12048192771084337)

    def test_e_score(self):
        """test abydos.stats.ConfusionTable.e_score
        """
        pass

    def test_f1_score(self):
        """test abydos.stats.ConfusionTable.f1_score
        """
        self.assertEquals(UNIT_TABLE.f1_score(), 0.5)
        #self.assertEquals(NULL_TABLE.f1_score(), )
        self.assertAlmostEqual(SCALE_TABLE.f1_score(), 2/9)
        self.assertAlmostEqual(CATSNDOGS_TABLE.f1_score(), 2/3)
        self.assertAlmostEqual(WORKED_EG_TABLE.f1_score(), 0.17391304347826089)

    def test_f_measure(self):
        """test abydos.stats.ConfusionTable.f_measure
        """
        self.assertEquals(UNIT_TABLE.f_measure(), 0.5)
        #self.assertEquals(NULL_TABLE.f_measure(), )
        self.assertAlmostEqual(SCALE_TABLE.f_measure(), 2/9)
        self.assertAlmostEqual(CATSNDOGS_TABLE.f_measure(), 2/3)
        self.assertAlmostEqual(WORKED_EG_TABLE.f_measure(), 0.17391304347826089)

    def test_g_measure(self):
        """test abydos.stats.ConfusionTable.g_measure
        """
        pass

    def test_mcc(self):
        """test abydos.stats.ConfusionTable.mcc
        """
        self.assertEquals(UNIT_TABLE.mcc(), 0)
        #self.assertEquals(NULL_TABLE.mcc(), )
        self.assertAlmostEqual(SCALE_TABLE.mcc(), -0.40824829046386302)
        self.assertAlmostEqual(CATSNDOGS_TABLE.mcc(), 0.54155339089324317)
        self.assertAlmostEqual(WORKED_EG_TABLE.mcc(), 0.23348550853492078)

    def test_significance(self):
        """test abydos.stats.ConfusionTable.significance
        """
        pass
