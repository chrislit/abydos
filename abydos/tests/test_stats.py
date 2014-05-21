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

class cast_test_cases(unittest.TestCase):
    def test_tuple(self):
        pass

    def test_dict(self):
        pass


class population_test_cases(unittest.TestCase):
    def test_correct_pop(self):
        pass

    def test_error_pop(self):
        pass

    def test_test_pos_pop(self):
        pass

    def test_test_neg_pop(self):
        pass

    def test_cond_pos_pop(self):
        pass

    def test_cond_neg_pop(self):
        pass

    def test_population(self):
        pass


class statistical_ratio_test_cases(unittest.TestCase):
    def test_precision(self):
        pass

    def test_recall(self):
        pass

    def test_specificity(self):
        pass

    def test_npv(self):
        pass

    def test_fallout(self):
        pass

    def test_fdr(self):
        pass

    def test_accuracy(self):
        pass

    def test_balanced_accuracy(self):
        pass

    def test_informedness(self):
        pass

    def test_markedness(self):
        pass


class pr_means_test_cases(unittest.TestCase):
    def test_pr_mean(self):
        pass

    def test_pr_gmean(self):
        pass

    def test_pr_hmean(self):
        pass

    def test_pr_qmean(self):
        pass

    def test_pr_lmean(self):
        pass

    def test_pr_cmean(self):
        pass

    def test_pr_imean(self):
        pass

    def test_pr_pmean(self):
        pass


class statistical_measure_test_cases(unittest.TestCase):
    def test_fbeta_score(self):
        pass

    def test_f2_score(self):
        pass

    def test_fhalf_score(self):
        pass

    def test_e_score(self):
        pass

    def test_f1_score(self):
        pass

    def test_f_measure(self):
        pass

    def test_g_measure(self):
        pass

    def test_mcc(self):
        pass

    def test_significance(self):
        pass
