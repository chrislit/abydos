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

r"""abydos.stats.

The stats module defines functions for calculating various statistical data
about linguistic objects.

Functions are provided for calculating the following means:

    - arithmetic mean (:py:func:`.amean`)
    - geometric mean (:py:func:`.gmean`)
    - harmonic mean (:py:func:`.hmean`)
    - quadratic mean (:py:func:`.qmean`)
    - contraharmonic mean (:py:func:`.cmean`)
    - logarithmic mean (:py:func:`.lmean`)
    - identric (exponential) mean (:py:func:`.imean`)
    - Seiffert's mean (:py:func:`.seiffert_mean`)
    - Lehmer mean (:py:func:`.lehmer_mean`)
    - Heronian mean (:py:func:`.heronian_mean`)
    - Hölder (power/generalized) mean (:py:func:`.hoelder_mean`)
    - arithmetic-geometric mean (:py:func:`.agmean`)
    - geometric-harmonic mean (:py:func:`.ghmean`)
    - arithmetic-geometric-harmonic mean (:py:func:`.aghmean`)

And for calculating:

    - midrange (:py:func:`.midrange`)
    - median (:py:func:`.median`)
    - mode (:py:func:`.mode`)
    - variance (:py:func:`.var`)
    - standard deviation (:py:func:`.std`)

Some examples of the basic functions:

>>> nums = [16, 49, 55, 49, 6, 40, 23, 47, 29, 85, 76, 20]
>>> amean(nums)
41.25
>>> aghmean(nums)
32.42167170892585
>>> heronian_mean(nums)
37.931508950381925
>>> mode(nums)
49
>>> std(nums)
22.876935255113754



Two pairwise functions are provided:

    - mean pairwise similarity (:py:func:`.mean_pairwise_similarity`), which
      returns the mean similarity (using a supplied similarity function) among
      each item in a collection
    - pairwise similarity statistics
      (:py:func:`.pairwise_similarity_statistics`), which returns the max, min,
      mean, and standard deviation of pairwise similarities between two
      collections

The confusion table class (:py:class:`.ConfusionTable`) can be constructed in
a number of ways:

    - four values, representing true positives, true negatives,
      false positives, and false negatives, can be passed to the constructor
    - a list or tuple with four values, representing true positives,
      true negatives, false positives, and false negatives, can be passed to
      the constructor
    - a dict with keys 'tp', 'tn', 'fp', 'fn', each assigned to the values for
      true positives, true negatives, false positives, and false negatives
      can be passed to the constructor

The :py:class:`.ConfusionTable` class has methods:

    - :py:meth:`.to_tuple` extracts the :py:class:`.ConfusionTable` values as a
      tuple: (:math:`w`, :math:`x`, :math:`y`, :math:`z`)
    - :py:meth:`.to_dict` extracts the :py:class:`.ConfusionTable` values as a
      dict: {'tp'::math:`w`, 'tn'::math:`x`, 'fp'::math:`y`, 'fn'::math:`z`}
    - :py:meth:`.true_pos` returns the number of true positives
    - :py:meth:`.true_neg` returns the number of true negatives
    - :py:meth:`.false_pos` returns the number of false positives
    - :py:meth:`.false_neg` returns the number of false negatives
    - :py:meth:`.correct_pop` returns the correct population
    - :py:meth:`.error_pop` returns the error population
    - :py:meth:`.test_pos_pop` returns the test positive population
    - :py:meth:`.test_neg_pop` returns the test negative population
    - :py:meth:`.cond_pos_pop` returns the condition positive population
    - :py:meth:`.cond_neg_pop` returns the condition negative population
    - :py:meth:`.population` returns the total population
    - :py:meth:`.precision` returns the precision
    - :py:meth:`.precision_gain` returns the precision gain
    - :py:meth:`.recall` returns the recall
    - :py:meth:`.specificity` returns the specificity
    - :py:meth:`.npv` returns the negative predictive value
    - :py:meth:`.fallout` returns the fallout
    - :py:meth:`.fdr` returns the false discovery rate
    - :py:meth:`.accuracy` returns the accuracy
    - :py:meth:`.accuracy_gain` returns the accuracy gain
    - :py:meth:`.balanced_accuracy` returns the balanced accuracy
    - :py:meth:`.informedness` returns the informedness
    - :py:meth:`.markedness` returns the markedness
    - :py:meth:`.pr_amean` returns the arithmetic mean of precision & recall
    - :py:meth:`.pr_gmean` returns the geometric mean of precision & recall
    - :py:meth:`.pr_hmean` returns the harmonic mean of precision & recall
    - :py:meth:`.pr_qmean` returns the quadratic mean of precision & recall
    - :py:meth:`.pr_cmean` returns the contraharmonic mean of precision &
      recall
    - :py:meth:`.pr_lmean` returns the logarithmic mean of precision & recall
    - :py:meth:`.pr_imean` returns the identric mean of precision & recall
    - :py:meth:`.pr_seiffert_mean` returns Seiffert's mean of precision &
      recall
    - :py:meth:`.pr_lehmer_mean` returns the Lehmer mean of precision & recall
    - :py:meth:`.pr_heronian_mean` returns the Heronian mean of precision &
      recall
    - :py:meth:`.pr_hoelder_mean` returns the Hölder mean of precision & recall
    - :py:meth:`.pr_agmean` returns the arithmetic-geometric mean of precision
      & recall
    - :py:meth:`.pr_ghmean` returns the geometric-harmonic mean of precision &
      recall
    - :py:meth:`.pr_aghmean` returns the arithmetic-geometric-harmonic mean of
      precision & recall
    - :py:meth:`.fbeta_score` returns the :math:`F_{beta}` score
    - :py:meth:`.f2_score` returns the :math:`F_2` score
    - :py:meth:`.fhalf_score` returns the :math:`F_{\frac{1}{2}}` score
    - :py:meth:`.e_score` returns the :math:`E` score
    - :py:meth:`.f1_score` returns the :math:`F_1` score
    - :py:meth:`.f_measure` returns the F measure
    - :py:meth:`.g_measure` returns the G measure
    - :py:meth:`.mcc` returns Matthews correlation coefficient
    - :py:meth:`.significance` returns the significance
    - :py:meth:`.kappa_statistic` returns the Kappa statistic


>>> ct = ConfusionTable(120, 60, 20, 30)
>>> ct.f1_score()
0.8275862068965516
>>> ct.mcc()
0.5367450401216932
>>> ct.specificity()
0.75
>>> ct.significance()
66.26190476190476


The :py:class:`.ConfusionTable` class also supports checking for equality with
another :py:class:`.ConfusionTable` and casting to string with ``str()``:

>>> (ConfusionTable({'tp':120, 'tn':60, 'fp':20, 'fn':30}) ==
... ConfusionTable(120, 60, 20, 30))
True
>>> str(ConfusionTable(120, 60, 20, 30))
'tp:120, tn:60, fp:20, fn:30'

----

"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._confusion_table import ConfusionTable
from ._mean import (
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
from ._pairwise import mean_pairwise_similarity, pairwise_similarity_statistics

__all__ = [
    'ConfusionTable',
    'amean',
    'gmean',
    'hmean',
    'agmean',
    'ghmean',
    'aghmean',
    'cmean',
    'imean',
    'lmean',
    'qmean',
    'heronian_mean',
    'hoelder_mean',
    'lehmer_mean',
    'seiffert_mean',
    'median',
    'midrange',
    'mode',
    'std',
    'var',
    'mean_pairwise_similarity',
    'pairwise_similarity_statistics',
]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
