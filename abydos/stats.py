# -*- coding: utf-8 -*-

# Copyright 2014-2015 by Christopher C. Little.
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

"""abydos.stats

The stats module defines functions for calculating various statistical data
about linguistic objects.

This includes the ConfusionTable object, which includes members cable of
calculating the following data based on a confusion table:
    - population counts
    - precision, recall, specificity, negative predictive value, fall-out,
        false discovery rate, accuracy, balanced accuracy, informedness,
        and markedness
    - various means of the precision & recall, including: arithmetic,
        geometric, harmonic, quadratic, logarithmic, contraharmonic,
        identric, & Hölder (power) means
    - :math:`F_{β}`-scores, :math:`E`-scores, :math:`G`-measures, along with
        special functions for :math:`F_{1}`, :math:`F_{0.5}`, & :math:`F_{2}`
        scores
    - significance & Matthews correlation coefficient calculation

Functions are provided for calculating the following means:
    - arithmetic
    - geometric
    - harmonic
    - quadratic
    - contraharmonic
    - logarithmic,
    - identric
    - Seiffert's
    - Lehmer
    - Heronian
    - Hölder (power)
    - arithmetic-geometric
    - geometric-harmonic
    - arithmetic-geometric-harmonic
And for calculating:
    - midrange
    - median
    - mode
"""

from __future__ import unicode_literals
from __future__ import division
import math
from .util import prod
from ._compat import _range
from collections import Counter


class ConfusionTable(object):
    """ConfusionTable object

    This object is initialized by passing either four integers (or a tuple of
    four integers) representing the squares of a confusion table:
    true positives, true negatives, false positives, and false negatives

    The object possesses methods for the calculation of various statistics
    based on the confusion table.
    """
    tpos, tneg, fpos, fneg = 0, 0, 0, 0

    def __init__(self, tp=0, tn=0, fp=0, fn=0):
        """ConfusionTable constructor

        :param int tp: true positives (or a tuple, list, or dict); If a tuple
            or list is supplied, it must include 4 values in the order [tp, tn,
            fp, fn]. If a dict is supplied, it must have 4 keys, namely 'tp',
            'tn', 'fp', & 'fn'.
        :param int tn: true negatives
        :param int fp: false positives
        :param int fn: false negatives
        """
        if isinstance(tp, tuple) or isinstance(tp, list):
            if len(tp) == 4:
                self.tpos = tp[0]
                self.tneg = tp[1]
                self.fpos = tp[2]
                self.fneg = tp[3]
            else:
                raise AttributeError('ConfusionTable requires a 4-tuple ' +
                                     'when being created from a tuple.')
        elif isinstance(tp, dict):
            if 'tp' in tp:
                self.tpos = tp['tp']
            if 'tn' in tp:
                self.tneg = tp['tn']
            if 'fp' in tp:
                self.fpos = tp['fp']
            if 'fn' in tp:
                self.fneg = tp['fn']
        else:
            self.tpos = tp
            self.tneg = tn
            self.fpos = fp
            self.fneg = fn

    def __eq__(self, other):
        """eqality operator (==)

        Compares a ConfusionTable to another ConfusionTable or its equivalent
        in the form of a tuple, list, or dict.

        :returns: True if two ConfusionTables are the same object or all four
        of their attributes are equal
        :rtype: bool
        """
        if isinstance(other, ConfusionTable):
            if id(self) == id(other):
                return True
            if ((self.tpos == other.tpos and self.tneg == other.tneg and
                 self.fpos == other.fpos and self. fneg == other.fneg)):
                return True
        elif isinstance(other, tuple) or isinstance(other, list):
            if ((self.tpos == other[0] and self.tneg == other[1] and
                 self.fpos == other[2] and self.fneg == other[3])):
                return True
        elif isinstance(other, dict):
            if ((self.tpos == other['tp'] and self.tneg == other['tn'] and
                 self.fpos == other['fp'] and self.fneg == other['fn'])):
                return True
        return False

    def __str__(self):
        """cast to str

        :returns: a human-readable version of the confusion table
        :rtype: str
        """
        return ('tp:' + str(self.tpos) + ', tn:' + str(self.tneg) + ', fp:' +
                str(self.fpos) + ', fn:' + str(self.fneg))

    def tuple(self):
        """cast to tuple

        :returns: the confusion table as a 4-tuple (tp, tn, fp, fn)
        :rtype: tuple
        """
        return (self.tpos, self.tneg, self.fpos, self.fneg)

    def dict(self):
        """cast to dict

        :returns: the confusion table as a dict
        :rtype: dict
        """
        return {'tp': self.tpos, 'tn': self.tneg,
                'fp': self.fpos, 'fn': self.fneg}

    def correct_pop(self):
        """correct population

        :returns: the correct population of the confusion table
        :rtype: int
        """
        return self.tpos + self.tneg

    def error_pop(self):
        """error population

        :returns: The error population of the confusion table
        :rtype: int
        """
        return self.fpos + self.fneg

    def test_pos_pop(self):
        """test positive population

        :returns: The test positive population of the confusion table
        :rtype: int
        """
        return self.tpos + self.fpos

    def test_neg_pop(self):
        """test negative population

        :returns: The test negative population of the confusion table
        :rtype: int
        """
        return self.tneg + self.fneg

    def cond_pos_pop(self):
        """condition positive population

        :returns: The condition positive population of the confusion table
        :rtype: int
        """
        return self.tpos + self.fneg

    def cond_neg_pop(self):
        """condition negative population

        :returns: The condition negative population of the confusion table
        :rtype: int
        """
        return self.fpos + self.tneg

    def population(self):
        """population (N)

        :returns: The population (N) of the confusion table
        :rtype: int
        """
        return self.tpos + self.tneg + self.fpos + self.fneg

    def precision(self):
        """precision

        Precision is defined as :math:`\\frac{tp}{tp + fp}`

        AKA positive predictive value (PPV)

        Cf. https://en.wikipedia.org/wiki/Precision_and_recall
        Cf. https://en.wikipedia.org/wiki/Information_retrieval#Precision

        :returns: The precision of the confusion table
        :rtype: float
        """
        if self.tpos + self.fpos == 0:
            return float('NaN')
        return self.tpos / (self.tpos + self.fpos)

    def precision_gain(self):
        """gain in precision

        The gain in precision is defined as:
        :math:`G(precision) = \\frac{precision}{random~ precision}`

        Cf. https://en.wikipedia.org/wiki/Gain_(information_retrieval)

        :returns: The gain in precision of the confusion table
        :rtype: float
        """
        if self.population() == 0:
            return float('NaN')
        random_precision = self.cond_pos_pop()/self.population()
        return self.precision()/random_precision

    def recall(self):
        """recall

        Recall is defined as :math:`\\frac{tp}{tp + fn}

        AKA sensitivity
        AKA true positive rate (TPR)

        Cf. https://en.wikipedia.org/wiki/Precision_and_recall
        Cf. https://en.wikipedia.org/wiki/Sensitivity_(test)
        Cf. https://en.wikipedia.org/wiki/Information_retrieval#Recall

        :returns: The recall of the confusion table
        :rtype: float
        """
        if self.tpos + self.fneg == 0:
            return float('NaN')
        return self.tpos / (self.tpos + self.fneg)

    def specificity(self):
        """specificity

        Specificity is defined as :math:`\\frac{tn}{tn + fp}`

        AKA true negative rate (TNR)

        Cf. https://en.wikipedia.org/wiki/Specificity_(tests)

        :returns: The specificity of the confusion table
        :rtype: float
        """
        if self.tneg + self.fpos == 0:
            return float('NaN')
        return self.tneg / (self.tneg + self.fpos)

    def npv(self):
        """negative predictive value (NPV)

        NPV is defined as :math:`\\frac{tn}{tn + fn}`

        Cf. https://en.wikipedia.org/wiki/Negative_predictive_value

        :returns: The negative predictive value of the confusion table
        :rtype: float
        """
        if self.tneg + self.fneg == 0:
            return float('NaN')
        return self.tneg / (self.tneg + self.fneg)

    def fallout(self):
        """fall-out

        Fall-out is defined as :math:`\\frac{fp}{fp + tn}`
        AKA false positive rate (FPR)

        Cf. https://en.wikipedia.org/wiki/Information_retrieval#Fall-out

        :returns: The fall-out of the confusion table
        :rtype: float
        """
        if self.fpos + self.tneg == 0:
            return float('NaN')
        return self.fpos / (self.fpos + self.tneg)

    def fdr(self):
        """false discovery rate (FDR)

        False discovery rate is defined as :math:`\\frac{fp}{fp + tp}`

        Cf. https://en.wikipedia.org/wiki/False_discovery_rate

        :returns: The false discovery rate of the confusion table
        :rtype: float
        """
        if self.fpos + self.tpos == 0:
            return float('NaN')
        return self.fpos / (self.fpos + self.tpos)

    def accuracy(self):
        """accuracy

        Accuracy is defined as :math:`\\frac{tp + tn}{population}`

        Cf. https://en.wikipedia.org/wiki/Accuracy

        :returns: The accuracy of the confusion table
        :rtype: float
        """
        if self.population() == 0:
            return float('NaN')
        return (self.tpos + self.tneg) / self.population()

    def accuracy_gain(self):
        """gain in accuracy

        The gain in accuracy is defined as:
        :math:`G(accuracy) = \frac{accuracy}{random~ accuracy}`

        Cf. https://en.wikipedia.org/wiki/Gain_(information_retrieval)

        :returns: The gain in accuracy of the confusion table
        :rtype: float
        """
        if self.population() == 0:
            return float('NaN')
        random_accuracy = ((self.cond_pos_pop()/self.population())**2 +
                           (self.cond_neg_pop()/self.population())**2)
        return self.accuracy()/random_accuracy

    def balanced_accuracy(self):
        """balanced accuracy

        Balanced accuracy is defined as
        :math:`\\frac{sensitivity + specificity}{2}`

        Cf. https://en.wikipedia.org/wiki/Accuracy

        :returns: The balanced accuracy of the confusion table
        :rtype: float
        """
        return 0.5 * (self.recall() + self.specificity())

    def informedness(self):
        """informedness

        Informedness is defined as :math:`sensitivity + specificity - 1`.
        AKA Youden's J statistic
        AKA DeltaP'

        Cf. https://en.wikipedia.org/wiki/Youden%27s_J_statistic
        Cf.
        http://dspace.flinders.edu.au/xmlui/bitstream/handle/2328/27165/Powers%20Evaluation.pdf

        :returns: The informedness of the confusion table
        :rtype: float
        """
        return self.recall() + self.specificity() - 1

    def markedness(self):
        """markedness

        Markedness is defined as :math:`precision + npv - 1`
        AKA DeltaP

        Cf. https://en.wikipedia.org/wiki/Youden%27s_J_statistic
        Cf.
        http://dspace.flinders.edu.au/xmlui/bitstream/handle/2328/27165/Powers%20Evaluation.pdf

        :returns: The markedness of the confusion table
        :rtype: float
        """
        return self.precision() + self.npv() - 1

    def pr_amean(self):
        """arithmetic mean of precision & recall

        The arithmetic mean of precision and recall is defined as:
        :math:`\\frac{precision \\cdot recall}{2}`

        Cf. https://en.wikipedia.org/wiki/Arithmetic_mean

        :returns: The arithmetic mean of the confusion table's precision &
            recall
        :rtype: float
        """
        return amean((self.precision(), self.recall()))

    def pr_gmean(self):
        """geometric mean of precision & recall

        The geometric mean of precision and recall is defined as:
        :math:`\\sqrt{precision \\cdot recall}`

        Cf. https://en.wikipedia.org/wiki/Geometric_mean

        :returns: The geometric mean of the confusion table's precision &
            recall
        :rtype: float
        """
        return gmean((self.precision(), self.recall()))

    def pr_hmean(self):
        """harmonic mean of precision & recall

        The harmonic mean of precision and recall is defined as:
        :math:`\\frac{2 \\cdot precision \\cdot recall}{precision + recall}`

        Cf. https://en.wikipedia.org/wiki/Harmonic_mean

        :returns: The harmonic mean of the confusion table's precision & recall
        :rtype: float
        """
        return hmean((self.precision(), self.recall()))

    def pr_qmean(self):
        """quadratic mean of precision & recall

        The quadratic mean of precision and recall is defined as:
        :math:`\\sqrt{\\frac{precision^{2} + recall^{2}}{2}}`

        Cf. https://en.wikipedia.org/wiki/Quadratic_mean

        :returns: The quadratic mean of the confusion table's precision &
            recall
        :rtype: float
        """
        return qmean((self.precision(), self.recall()))

    def pr_cmean(self):
        """contraharmonic mean of precision & recall

        The contraharmonic mean is:
        :math:`\\frac{precision^{2} + recall^{2}}{precision + recall}`

        Cf. https://en.wikipedia.org/wiki/Contraharmonic_mean

        :returns: The contraharmonic mean of the confusion table's precision &
            recall
        :rtype: float
        """
        return cmean((self.precision(), self.recall()))

    def pr_lmean(self):
        """logarithmic mean of precision & recall

        The logarithmic mean is:
        0 if either precision or recall is 0,
        the precision if they are equal,
        otherwise :math:`\\frac{precision - recall}
        {ln(precision) - ln(recall)}`

        Cf. https://en.wikipedia.org/wiki/Logarithmic_mean

        :returns: The logarithmic mean of the confusion table's precision &
            recall
        :rtype: float
        """
        precision = self.precision()
        recall = self.recall()
        if not precision or not recall:
            return 0.0
        elif precision == recall:
            return precision
        else:
            return ((precision - recall) /
                    (math.log(precision) - math.log(recall)))

    def pr_imean(self):
        """identric mean of precision & recall

        The identric mean is:
        precision if precision = recall,
        otherwise :math:`\\frac{1}{e} \\cdot
        \\sqrt[precision - recall]\\frac{precision^{precision}}
        {recall^{recall}}`

        Cf. https://en.wikipedia.org/wiki/Identric_mean

        :returns: The identric mean of the confusion table's precision & recall
        :rtype: float
        """
        return imean((self.precision(), self.recall()))

    def pr_seiffert_mean(self):
        """Seiffert's mean of precision & recall

        Seiffert's mean of precision and recall is:
        :math:`\\frac{precision - recall}{4 \\cdot arctan
        \\sqrt{\\frac{precision}{recall}} - π}`

        Cf. http://www.helsinki.fi/~hasto/pp/miaPreprint.pdf

        :returns: Seiffer's mean of the confusion table's precision & recall
        :rtype: float
        """
        return seiffert_mean((self.precision(), self.recall()))

    def pr_lehmer_mean(self, exp=2):
        """Lehmer mean of precision & recall

        The Lehmer mean is:
        :math:`\\frac{precision^{exp} + recall^{exp}}
        {precision^{exp-1} + recall^{exp-1}}`

        Cf. https://en.wikipedia.org/wiki/Lehmer_mean

        :param numeric exp: The exponent of the Lehmer mean
        :returns: The Lehmer mean for the given exponent of the confusion
            table's precision & recall
        :rtype: float
        """
        return lehmer_mean((self.precision(), self.recall()), exp)

    def pr_heronian_mean(self):
        """Heronian mean of precision & recall

        The Heronian mean of precision and recall is defined as:
        :math:`\\frac{precision + \\sqrt{precision \\cdot recall} + recall}{3}`

        Cf. https://en.wikipedia.org/wiki/Heronian_mean

        :returns: The Heronian mean of the confusion table's precision & recall
        :rtype: float
        """
        return heronian_mean((self.precision(), self.recall()))

    def pr_hoelder_mean(self, exp=2):
        """Hölder (power) mean of precision & recall

        The power mean of precision and recall is defined as:
        :math:`\\frac{1}{2} \\cdot
        \sqrt[exp]{precision^{exp} + recall^{exp}}`
        for :math:`exp \\ne 0`, and the geometric mean for :math:`exp = 0`

        Cf. https://en.wikipedia.org/wiki/Generalized_mean

        :param numeric exp: The exponent of the Hölder mean
        :returns: The Hölder mean for the given exponent of the confusion
            table's precision & recall
        :rtype: float
        """
        return hoelder_mean((self.precision(), self.recall()), exp)

    def pr_agmean(self):
        """arithmetic-geometric mean of precision & recall

        Iterates between arithmetic & geometric means until they converge to
        a single value (rounded to 12 digits)
        Cf. https://en.wikipedia.org/wiki/Arithmetic–geometric_mean

        :returns: The arithmetic-geometric mean of the confusion table's
            precision & recall
        :rtype: float
        """
        return agmean((self.precision(), self.recall()))

    def pr_ghmean(self):
        """geometric-harmonic mean of precision & recall

        Iterates between geometric & harmonic means until they converge to
        a single value (rounded to 12 digits)
        Cf. https://en.wikipedia.org/wiki/Geometric–harmonic_mean

        :returns: The geometric-harmonic mean of the confusion table's
            precision & recall
        :rtype: float
        """
        return ghmean((self.precision(), self.recall()))

    def pr_aghmean(self):
        """arithmetic-geometric-harmonic mean of precision & recall

        Iterates over arithmetic, geometric, & harmonic means until they
        converge to a single value (rounded to 12 digits), following the
        method described by Raïssouli, Leazizi, & Chergui:
        http://www.emis.de/journals/JIPAM/images/014_08_JIPAM/014_08.pdf

        :returns: The arithmetic-geometric-harmonic mean of the confusion
            table's precision & recall
        :rtype: float
        """
        return aghmean((self.precision(), self.recall()))

    def fbeta_score(self, beta=1):
        """:math:`F_{β}` score

        :math:`F_{β}` for a positive real value :math:`β` "measures the
        effectiveness of retrieval with respect to a user who
        attaches :math:`β` times as much importance to recall as
        precision" (van Rijsbergen 1979)

        :math:`F_{β}` score is defined as:
        :math:`(1 + β^2) \\cdot \\frac{precision \\cdot recall}
        {((β^2 \\cdot precision) + recall)}`

        Cf. https://en.wikipedia.org/wiki/F1_score

        :returns: The :math:`F_{β}` of the confusion table
        :rtype: float
        """
        if beta <= 0:
            raise AttributeError('Beta must be a positive real value.')
        precision = self.precision()
        recall = self.recall()
        return ((1 + beta**2) *
                precision * recall / ((beta**2 * precision) + recall))

    def f2_score(self):
        """Return the F_{2} score of the confusion table,
        which emphasizes recall over precision in comparison
        to the F_{1} score

        Cf. https://en.wikipedia.org/wiki/F1_score

        :returns: The  of the confusion table
        :rtype: float
        """
        return self.fbeta_score(2)

    def fhalf_score(self):
        """Return the F_{0.5} score of the confusion table,
        which emphasizes precision over recall in comparison
        to the F_{1} score

        Cf. https://en.wikipedia.org/wiki/F1_score

        :returns: The  of the confusion table
        :rtype: float
        """
        return self.fbeta_score(0.5)

    def e_score(self, beta=1):
        """Return the E-score (Van Rijsbergen's effectiveness
        measure)

        Cf. https://en.wikipedia.org/wiki/Information_retrieval#F-measure

        :returns: The  of the confusion table
        :rtype: float
        """
        return 1-self.fbeta_score(beta)

    def f1_score(self):
        """Return the F_{1} score of the confusion table

        F_{1} score is the harmonic mean of precision and recall:
        2*(precision*recall) / (precision+recall)

        Cf. https://en.wikipedia.org/wiki/F1_score

        :returns: The  of the confusion table
        :rtype: float
        """
        return self.pr_hmean()

    def f_measure(self):
        """Return the F-measure of the confusion table

        F-measure is the harmonic mean of precision and recall:
        2*(precision*recall) / (precision+recall)

        Cf. https://en.wikipedia.org/wiki/F1_score

        :returns: The  of the confusion table
        :rtype: float
        """
        return self.pr_hmean()

    def g_measure(self):
        """G-measure

        G-measure is the geometric mean of precision and recall:
        √(precision * recall)

        Cf. https://en.wikipedia.org/wiki/F1_score#G-measure

        :returns: The :math:`G`-measure of the confusion table
        :rtype: float
        """
        return self.pr_gmean()

    def mcc(self):
        """Matthews correlation coefficient (MCC)

        The Matthews correlation coefficient is defined as:
        ((tp * tn) - (fp * fn)) /
        sqrt((tp + fp)(tp + fn)(tn + fp)(tn + fn))

        This is equivalent to the geometric mean of informedness and
        markedness, defined above.

        Cf. https://en.wikipedia.org/wiki/Matthews_correlation_coefficient

        :returns: The Matthews correlation coefficient of the confusion table
        :rtype: float
        """
        if (((self.tpos + self.fpos) * (self.tpos + self.fneg) *
             (self.tneg + self.fpos) * (self.tneg + self.fneg))) == 0:
            return float('NaN')
        return (((self.tpos * self.tneg) - (self.fpos * self.fneg)) /
                math.sqrt((self.tpos + self.fpos) * (self.tpos + self.fneg) *
                          (self.tneg + self.fpos) * (self.tneg + self.fneg)))

    def significance(self):
        """Return the significance (χ²) of the confusion table

        Significance is defined as:
        χ² = (tp * tn - fp * fn)^2 (tp + tn + fp + fn) /
                                ((tp + fp)(tp + fn)(tn + fp)(tn + fn))

        Also: χ² = MCC²*n

        Cf. https://en.wikipedia.org/wiki/Pearson%27s_chi-square_test

        :returns: The significance of the confusion table
        :rtype: float
        """
        if (((self.tpos + self.fpos) * (self.tpos + self.fneg) *
             (self.tneg + self.fpos) * (self.tneg + self.fneg))) == 0:
            return float('NaN')
        return (((self.tpos * self.tneg - self.fpos * self.fneg)**2 *
                 (self.tpos + self.tneg + self.fpos + self.fneg)) /
                ((self.tpos + self.fpos) * (self.tpos + self.fneg) *
                 (self.tneg + self.fpos) * (self.tneg + self.fneg)))

    def kappa_statistic(self):
        """κ statistic

        The κ statistic is defined as:
        κ = (accuracy - random accuracy) / (1 - random accuracy)

        The κstatistic compares the performance of the classifier relative to
        the performance of a random classifier. κ = 0 indicates performance
        identical to random. κ = 1 indicates perfect predictive success.
        κ = -1 indicates perfect predictive failure.

        :returns: The κ statistic of the confusion table
        :rtype: float
        """
        if self.population() == 0:
            return float('NaN')
        random_accuracy = (((self.tneg + self.fpos) *
                            (self.tneg + self.fneg) +
                            (self.fneg + self.tpos) *
                            (self.fpos + self.tpos)) /
                           self.population()**2)
        return (self.accuracy()-random_accuracy) / (1-random_accuracy)


def amean(nums):
    """Return the arithmetic mean of a series of numbers

    The arithmetic mean is defined as:
    Σ(nums)/|nums|

    Cf. https://en.wikipedia.org/wiki/Arithmetic_mean

    :param list nums: A series of numbers
    :returns: The arithmetric mean of nums
    :rtype: float
    """
    return sum(nums)/len(nums)


def gmean(nums):
    """Return the geometric mean of a series of numbers

    The geometric mean is defined as:
    Π(nums)^(1/|nums|)

    Cf. https://en.wikipedia.org/wiki/Geometric_mean

    :param list nums: A series of numbers
    :returns: The geometric mean of nums
    :rtype: float
    """
    return prod(nums)**(1/len(nums))


def hmean(nums):
    """Return the harmonic mean of a series of numbers

    The harmonic mean is defined as:
    |nums| / Σ_i(1/nums_i)

    Following the behavior of Wolfram|Alpha:
    If one of the values in nums is 0, return 0.
    If more than one value in nums is 0, return NaN.

    Cf. https://en.wikipedia.org/wiki/Harmonic_mean

    :param list nums: A series of numbers
    :returns: The harmonic mean of nums
    :rtype: float
    """
    if len(nums) < 1:
        raise AttributeError('hmean requires at least one value')
    elif len(nums) == 1:
        return nums[0]
    else:
        for i in _range(1, len(nums)):
            if nums[0] != nums[i]:
                break
        else:
            return nums[0]

    if 0 in nums:
        if nums.count(0) > 1:
            return float('nan')
        return 0
    return len(nums)/sum([1/i for i in nums])


def qmean(nums):
    """Return the quadratic mean of a series of numbers

    Arguments:
    nums -- a tuple, list, or set of numbers

    The quadratic mean of precision and recall is defined as:
    √(Σ_i(num_i^2)/|nums|)

    Cf. https://en.wikipedia.org/wiki/Quadratic_mean

    :param list nums: A series of numbers
    :returns: The quadratic mean of nums
    :rtype: float
    """
    return (sum([i**2 for i in nums])/len(nums))**(0.5)


def cmean(nums):
    """Return the contraharmonic mean of a series of numbers

    Arguments:
    nums -- a tuple, list, or set of numbers

    The contraharmonic mean is:
    Σ_i(x_i^2)/Σx

    Cf. https://en.wikipedia.org/wiki/Contraharmonic_mean

    :param list nums: A series of numbers
    :returns: The contraharmonic mean of nums
    :rtype: float
    """
    return sum([x**2 for x in nums])/sum(nums)


def lmean(nums):
    """Return the logarithmic mean of a series of numbers

    The logarithmic mean of an arbitrary series is defined by
    http://www.survo.fi/papers/logmean.pdf
    as:
    L(x_1, x_2, ..., x_n) = (n-1)! * Σ_i(x_i /  Π_j[i!=j] (log (x_i/x_j)))

    Cf. https://en.wikipedia.org/wiki/Logarithmic_mean

    :param list nums: A series of numbers
    :returns: The logarithmic mean of nums
    :rtype: float
    """
    if len(nums) != len(set(nums)):
        raise AttributeError('No two values in the nums list may be equal.')
    rolling_sum = 0
    for i in _range(len(nums)):
        rolling_prod = 1
        for j in _range(len(nums)):
            if i != j:
                rolling_prod *= (math.log(nums[i]/nums[j]))
        rolling_sum += nums[i]/rolling_prod
    return math.factorial(len(nums)-1) * rolling_sum


def imean(nums):
    """Return the identric (exponential) mean of a pair of numbers

    The identric mean of two numbers x and y is:
    x if x == y
    otherwise (1/e) * (x^x / y^y)^(1 / (x-y))

    Cf. https://en.wikipedia.org/wiki/Identric_mean

    :param list nums: A series of numbers
    :returns: The identric mean of nums
    :rtype: float
    """
    if len(nums) == 1:
        return nums[0]
    if len(nums) > 2:
        raise AttributeError('imean supports no more than two values')
    if nums[0] <= 0 or nums[1] <= 0:
        return float('NaN')
    elif nums[0] == nums[1]:
        return nums[0]
    return ((1/math.e) *
            (nums[0]**nums[0]/nums[1]**nums[1])**(1/(nums[0]-nums[1])))


def seiffert_mean(nums):
    """Return Seiffert's mean of a pair of numbers

    Seiffert's mean of two numbers x and y is:
    (x - y) / (4 * arctan(√(x/y)) - π)

    Cf. http://www.helsinki.fi/~hasto/pp/miaPreprint.pdf

    :param list nums: A series of numbers
    :returns: Sieffert's mean of nums
    :rtype: float
    """
    if len(nums) == 1:
        return nums[0]
    if len(nums) > 2:
        raise AttributeError('seiffert_mean supports no more than two values')
    if nums[0]+nums[1] == 0 or nums[0]-nums[1] == 0:
        return float('NaN')
    return (nums[0]-nums[1])/(2*math.asin((nums[0]-nums[1])/(nums[0]+nums[1])))


def lehmer_mean(nums, exp=2):
    """Return the Lehmer mean of a series of numbers

    The Lehmer mean is:
    Σ_i(x_i^p)/Σ_i(x_i^(p-1))

    Cf. https://en.wikipedia.org/wiki/Lehmer_mean

    :param list nums: A series of numbers
    :param numeric exp: The exponent of the Lehmer mean
    :returns: The Lehmer mean of nums for the given exponent
    :rtype: float
    """
    return sum([x**exp for x in nums])/sum([x**(exp-1) for x in nums])


def heronian_mean(nums):
    """Return the Heronian mean of a series of numbers

    The Heronian mean is:
    Σ_i,j((x_i*x_j)^(1/2))/(|nums|*(|nums|+1)/2)
    for j >= i

    Cf. https://en.wikipedia.org/wiki/Heronian_mean

    :param list nums: A series of numbers
    :returns: The Heronian mean of nums
    :rtype: float
    """
    mag = len(nums)
    rolling_sum = 0
    for i in _range(mag):
        for j in _range(i, mag):
            if nums[i] == nums[j]:
                rolling_sum += nums[i]
            else:
                rolling_sum += (nums[i]*nums[j])**(0.5)
    return rolling_sum * 2 / (mag*(mag+1))


def hoelder_mean(nums, exp=2):
    """Return the Hölder (power) mean of a series of numbers

    The Hölder mean is defined as:
    ((1/|nums|)*Σ_i(x_i^p))^(1/p)
    for p != 0, and the geometric mean for p == 0

    Cf. https://en.wikipedia.org/wiki/Generalized_mean

    :param list nums: A series of numbers
    :param numeric exp: The exponent of the Hölder mean
    :returns: The Hölder mean of nums for the given exponent
    :rtype: float
    """
    if exp == 0:
        return gmean(nums)
    return ((1/len(nums)) * sum([i**exp for i in nums]))**(1/exp)


def agmean(nums):
    """Return the arithmetic-geometric mean of a series of numbers

    Iterates between arithmetic & geometric means until they converge to
    a single value (rounded to 12 digits)
    Cf. https://en.wikipedia.org/wiki/Arithmetic–geometric_mean

    :param list nums: A series of numbers
    :returns: The arithmetic-geometric mean of nums
    :rtype: float
    """
    m_a = amean(nums)
    m_g = gmean(nums)
    if math.isnan(m_a) or math.isnan(m_g):
        return float('nan')
    while round(m_a, 12) != round(m_g, 12):
        m_a, m_g = (m_a+m_g)/2, (m_a*m_g)**(1/2)
    return m_a


def ghmean(nums):
    """Return the geometric-harmonic mean of a series of numbers

    Iterates between geometric & harmonic means until they converge to
    a single value (rounded to 12 digits)
    Cf. https://en.wikipedia.org/wiki/Geometric–harmonic_mean

    :param list nums: A series of numbers
    :returns: The geometric-harmonic mean of nums
    :rtype: float
    """
    m_g = gmean(nums)
    m_h = hmean(nums)
    if math.isnan(m_g) or math.isnan(m_h):
        return float('nan')
    while round(m_h, 12) != round(m_g, 12):
        m_g, m_h = (m_g*m_h)**(1/2), (2*m_g*m_h)/(m_g+m_h)
    return m_g


def aghmean(nums):
    """Return the arithmetic-geometric-harmonic mean of a series of numbers

    Iterates over arithmetic, geometric, & harmonic means until they
    converge to a single value (rounded to 12 digits), following the
    method described by Raïssouli, Leazizi, & Chergui:
    http://www.emis.de/journals/JIPAM/images/014_08_JIPAM/014_08.pdf

    :param list nums: A series of numbers
    :returns: The arithmetic-geometric-harmonic mean of nums
    :rtype: float
    """
    m_a = amean(nums)
    m_g = gmean(nums)
    m_h = hmean(nums)
    if math.isnan(m_a) or math.isnan(m_g) or math.isnan(m_h):
        return float('nan')
    while (round(m_a, 12) != round(m_g, 12) and
           round(m_g, 12) != round(m_h, 12)):
        m_a, m_g, m_h = ((m_a+m_g+m_h)/3,
                         (m_a*m_g*m_h)**(1/3),
                         3/(1/m_a+1/m_g+1/m_h))
    return m_a


def midrange(nums):
    """Return the median of a series of numbers

    The midrange is the arithmetic mean of the maximum & minimum of a series.

    Cf. https://en.wikipedia.org/wiki/Midrange

    :param list nums: A series of numbers
    :returns: The midrange of nums
    :rtype: float
    """
    return 0.5*(max(nums)+min(nums))


def median(nums):
    """Return the median of a series of numbers

    With numbers sorted by value, the median is the middle value (if there is
    an odd number of values) or the arithmetic mean of the two middle values
    (if there is an even number of values).

    Cf. https://en.wikipedia.org/wiki/Median

    :param list nums: A series of numbers
    :returns: The median of nums
    :rtype: float
    """
    nums = sorted(nums)
    mag = len(nums)
    if mag % 2:
        mag = int((mag-1)/2)
        return nums[mag]
    else:
        mag = int(mag/2)
        return (nums[mag-1]+nums[mag])/2


def mode(nums):
    """Calculate the mode

    The mode of a series is the most common element of that series

    Cf. https://en.wikipedia.org/wiki/Mode_(statistics)

    :param list nums: A series of numbers
    :returns: The mode of nums
    :rtype: float
    """
    return Counter(nums).most_common(1)[0][0]
