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


# pylint: disable=R0904
# pylint: disable=R0915
class CastTestCases(unittest.TestCase):
    """test cases for abydos.stats.ConfusionTable cast methods
    """
    def test_tuple(self):
        """test abydos.stats.ConfusionTable.tuple
        """
        pass

    def test_dict(self):
        """test abydos.stats.ConfusionTable.dict
        """
        pass


class PopulationTestCases(unittest.TestCase):
    """test cases for abydos.stats.ConfusionTable population methods
    """
    def test_correct_pop(self):
        """test abydos.stats.ConfusionTable.correct_pop
        """
        pass

    def test_error_pop(self):
        """test abydos.stats.ConfusionTable.error_pop
        """
        pass

    def test_test_pos_pop(self):
        """test abydos.stats.ConfusionTable.test_pos_pop
        """
        pass

    def test_test_neg_pop(self):
        """test abydos.stats.ConfusionTable.test_neg_pop
        """
        pass

    def test_cond_pos_pop(self):
        """test abydos.stats.ConfusionTable.cond_pos_pop
        """
        pass

    def test_cond_neg_pop(self):
        """test abydos.stats.ConfusionTable.cond_neg_pop
        """
        pass

    def test_population(self):
        """test abydos.stats.ConfusionTable.population
        """
        pass


class StatisticalRatioTestCases(unittest.TestCase):
    """test cases for abydos.stats.ConfusionTable basic statistical ratio
    methods
    """
    def test_precision(self):
        """test abydos.stats.ConfusionTable.precision
        """
        pass

    def test_recall(self):
        """test abydos.stats.ConfusionTable.recall
        """
        pass

    def test_specificity(self):
        """test abydos.stats.ConfusionTable.specificity
        """
        pass

    def test_npv(self):
        """test abydos.stats.ConfusionTable.npv
        """
        pass

    def test_fallout(self):
        """test abydos.stats.ConfusionTable.fallout
        """
        pass

    def test_fdr(self):
        """test abydos.stats.ConfusionTable.fdr
        """
        pass

    def test_accuracy(self):
        """test abydos.stats.ConfusionTable.accuracy
        """
        pass

    def test_balanced_accuracy(self):
        """test abydos.stats.ConfusionTable.balanced_accuracy
        """
        pass

    def test_informedness(self):
        """test abydos.stats.ConfusionTable.informedness
        """
        pass

    def test_markedness(self):
        """test abydos.stats.ConfusionTable.markedness
        """
        pass


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
        pass

    def test_f2_score(self):
        """test abydos.stats.ConfusionTable.f2_score
        """
        pass

    def test_fhalf_score(self):
        """test abydos.stats.ConfusionTable.fhalf_score
        """
        pass

    def test_e_score(self):
        """test abydos.stats.ConfusionTable.e_score
        """
        pass

    def test_f1_score(self):
        """test abydos.stats.ConfusionTable.f1_score
        """
        pass

    def test_f_measure(self):
        """test abydos.stats.ConfusionTable.f_measure
        """
        pass

    def test_g_measure(self):
        """test abydos.stats.ConfusionTable.g_measure
        """
        pass

    def test_mcc(self):
        """test abydos.stats.ConfusionTable.mcc
        """
        pass

    def test_significance(self):
        """test abydos.stats.ConfusionTable.significance
        """
        pass
