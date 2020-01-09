# Copyright 2014-2020 by Christopher C. Little.
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

r"""abydos.stats._confusion_table.

This includes the ConfusionTable object, which includes members capable of
calculating the following data based on a confusion table:

    - population counts
    - precision, recall, specificity, negative predictive value, fall-out,
      false discovery rate, accuracy, balanced accuracy, informedness,
      and markedness
    - various means of the precision & recall, including: arithmetic,
      geometric, harmonic, quadratic, logarithmic, contraharmonic,
      identric (exponential), & Hölder (power/generalized) means
    - :math:`F_{\beta}`-scores, :math:`E`-scores, :math:`G`-measures, along
      with special functions for :math:`F_{1}`, :math:`F_{0.5}`, &
      :math:`F_{2}` scores
    - significance & Matthews correlation coefficient calculation
"""

import math

from deprecation import deprecated

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
    qmean,
    seiffert_mean,
)
from .. import __version__

__all__ = ['ConfusionTable']


class ConfusionTable(object):
    """ConfusionTable object.

    This object is initialized by passing either four integers (or a tuple of
    four integers) representing the squares of a confusion table:
    true positives, true negatives, false positives, and false negatives

    The object possesses methods for the calculation of various statistics
    based on the confusion table.
    """

    _tp, _tn, _fp, _fn = 0, 0, 0, 0

    def __init__(self, tp=0, tn=0, fp=0, fn=0):
        """Initialize ConfusionTable.

        Parameters
        ----------
        tp : int or a tuple, list, or dict
            True positives; If a tuple or list is supplied, it must include 4
            values in the order [tp, tn, fp, fn]. If a dict is supplied, it
            must have 4 keys, namely 'tp', 'tn', 'fp', & 'fn'.
        tn : int
            True negatives
        fp : int
            False positives
        fn : int
            False negatives

        Raises
        ------
        AttributeError
            ConfusionTable requires a 4-tuple when being created from a tuple.

        Examples
        --------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct == ConfusionTable((120, 60, 20, 30))
        True
        >>> ct == ConfusionTable([120, 60, 20, 30])
        True
        >>> ct == ConfusionTable({'tp': 120, 'tn': 60, 'fp': 20, 'fn': 30})
        True


        .. versionadded:: 0.1.0

        """
        if isinstance(tp, (tuple, list)):
            if len(tp) == 4:
                self._tp = tp[0]
                self._tn = tp[1]
                self._fp = tp[2]
                self._fn = tp[3]
            else:
                raise AttributeError(
                    'ConfusionTable requires a 4-tuple when being created '
                    + 'from a tuple.'
                )
        elif isinstance(tp, dict):
            if 'tp' in tp:
                self._tp = tp['tp']
            if 'tn' in tp:
                self._tn = tp['tn']
            if 'fp' in tp:
                self._fp = tp['fp']
            if 'fn' in tp:
                self._fn = tp['fn']
        else:
            self._tp = tp
            self._tn = tn
            self._fp = fp
            self._fn = fn

    def __eq__(self, other):
        """Perform eqality (==) comparison.

        Compares a ConfusionTable to another ConfusionTable or its equivalent
        in the form of a tuple, list, or dict.

        Parameters
        ----------
        other : ConfusionTable
            Another ConfusionTable object to compare to

        Returns
        -------
        bool
            True if two ConfusionTables are the same object or all four of
            their attributes are equal

        Examples
        --------
        >>> ct1 = ConfusionTable(120, 60, 20, 30)
        >>> ct2 = ConfusionTable(120, 60, 20, 30)
        >>> ct3 = ConfusionTable(60, 30, 10, 15)

        >>> ct1 == ct2
        True
        >>> ct1 == ct3
        False

        >>> ct1 != ct2
        False
        >>> ct1 != ct3
        True


        .. versionadded:: 0.1.0

        """
        if isinstance(other, ConfusionTable):
            if id(self) == id(other):
                return True
            if (
                self._tp == other.true_pos()
                and self._tn == other.true_neg()
                and self._fp == other.false_pos()
                and self._fn == other.false_neg()
            ):
                return True
        elif isinstance(other, (tuple, list)):
            if (
                self._tp == other[0]
                and self._tn == other[1]
                and self._fp == other[2]
                and self._fn == other[3]
            ):
                return True
        elif isinstance(other, dict):
            if (
                self._tp == other['tp']
                and self._tn == other['tn']
                and self._fp == other['fp']
                and self._fn == other['fn']
            ):
                return True
        return False

    def __str__(self):
        """Cast to str.

        Returns
        -------
        str
            A human-readable version of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> str(ct)
        'tp:120, tn:60, fp:20, fn:30'


        .. versionadded:: 0.1.0

        """
        return 'tp:{}, tn:{}, fp:{}, fn:{}'.format(
            self._tp, self._tn, self._fp, self._fn
        )

    def __repr__(self):
        """Return representation.

        Returns
        -------
        str
            A string representation of the ConfusionTable that can be used to
            recreate it

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> repr(ct)
        'ConfusionTable(tp=120, tn=60, fp=20, fn=30)'


        .. versionadded:: 0.4.0

        """
        return 'ConfusionTable(tp={}, tn={}, fp={}, fn={})'.format(
            self._tp, self._tn, self._fp, self._fn
        )

    def to_tuple(self):
        """Cast to tuple.

        Returns
        -------
        tuple
            The confusion table as a 4-tuple (tp, tn, fp, fn)

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.to_tuple()
        (120, 60, 20, 30)


        .. versionadded:: 0.1.0

        """
        return self._tp, self._tn, self._fp, self._fn

    def to_dict(self):
        """Cast to dict.

        Returns
        -------
        dict
            The confusion table as a dict

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> import pprint
        >>> pprint.pprint(ct.to_dict())
        {'fn': 30, 'fp': 20, 'tn': 60, 'tp': 120}


        .. versionadded:: 0.1.0

        """
        return {'tp': self._tp, 'tn': self._tn, 'fp': self._fp, 'fn': self._fn}

    def true_pos(self):
        """Return true positives.

        Returns
        -------
        int
            The true positives of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.true_pos()
        120


        .. versionadded:: 0.1.0

        """
        return self._tp

    def true_neg(self):
        """Return true negatives.

        Returns
        -------
        int
            The true negatives of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.true_neg()
        60


        .. versionadded:: 0.1.0

        """
        return self._tn

    def false_pos(self):
        """Return false positives.

        AKA Type I error

        Returns
        -------
        int
            The false positives of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.false_pos()
        20


        .. versionadded:: 0.1.0

        """
        return self._fp

    def false_neg(self):
        """Return false negatives.

        AKA Type II error

        Returns
        -------
        int
            The false negatives of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.false_neg()
        30


        .. versionadded:: 0.1.0

        """
        return self._fn

    def correct_pop(self):
        """Return correct population.

        Returns
        -------
        int
            The correct population of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.correct_pop()
        180


        .. versionadded:: 0.1.0

        """
        return self._tp + self._tn

    def error_pop(self):
        """Return error population.

        Returns
        -------
        int
            The error population of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.error_pop()
        50


        .. versionadded:: 0.1.0

        """
        return self._fp + self._fn

    def pred_pos_pop(self):
        """Return predicted positive population.

        Returns
        -------
        int
            The predicted positive population of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.pred_pos_pop()
        140


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.4.0
            renamed from test_pos_pop


        .. versionadded:: 0.1.0

        """
        return self._tp + self._fp

    def pred_neg_pop(self):
        """Return predicted negative population.

        Returns
        -------
        int
            The predicted negative population of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.pred_neg_pop()
        90


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.4.0
            renamed from test_neg_pop


        .. versionadded:: 0.1.0

        """
        return self._tn + self._fn

    def cond_pos_pop(self):
        """Return condition positive population.

        Returns
        -------
        int
            The condition positive population of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.cond_pos_pop()
        150


        .. versionadded:: 0.1.0

        """
        return self._tp + self._fn

    def cond_neg_pop(self):
        """Return condition negative population.

        Returns
        -------
        int
            The condition negative population of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.cond_neg_pop()
        80


        .. versionadded:: 0.1.0

        """
        return self._fp + self._tn

    def population(self):
        """Return population, N.

        Returns
        -------
        int
            The population (N) of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.population()
        230


        .. versionadded:: 0.1.0

        """
        return self._tp + self._tn + self._fp + self._fn

    def precision(self):
        r"""Return precision.

        Precision is defined as

            .. math::

                \frac{tp}{tp + fp}

        AKA positive predictive value (PPV)

        Cf. https://en.wikipedia.org/wiki/Precision_and_recall

        Cf. https://en.wikipedia.org/wiki/Information_retrieval#Precision

        Returns
        -------
        float
            The precision of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.precision()
        0.8571428571428571


        .. versionadded:: 0.1.0

        """
        try:
            return self._tp / (self._tp + self._fp)
        except ZeroDivisionError:
            return float('nan')

    def precision_gain(self):
        r"""Return gain in precision.

        The gain in precision is defined as

            .. math::

                G(precision) = \frac{precision}{random~ precision}

        Cf. https://en.wikipedia.org/wiki/Gain_(information_retrieval)

        Returns
        -------
        float
            The gain in precision of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.precision_gain()
        1.3142857142857143


        .. versionadded:: 0.1.0

        """
        try:
            random_precision = self.cond_pos_pop() / self.population()
            return self.precision() / random_precision
        except ZeroDivisionError:
            return float('nan')

    def recall(self):
        r"""Return recall.

        Recall is defined as

            .. math::

                \frac{tp}{tp + fn}

        AKA sensitivity

        AKA true positive rate (TPR)

        Cf. https://en.wikipedia.org/wiki/Precision_and_recall

        Cf. https://en.wikipedia.org/wiki/Sensitivity_(test)

        Cf. https://en.wikipedia.org/wiki/Information_retrieval#Recall

        Returns
        -------
        float
            The recall of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.recall()
        0.8


        .. versionadded:: 0.1.0

        """
        try:
            return self._tp / (self._tp + self._fn)
        except ZeroDivisionError:
            return float('nan')

    def specificity(self):
        r"""Return specificity.

        Specificity is defined as

            .. math::

                \frac{tn}{tn + fp}

        AKA true negative rate (TNR)

        AKA inverse recall

        Cf. https://en.wikipedia.org/wiki/Specificity_(tests)

        Returns
        -------
        float
            The specificity of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.specificity()
        0.75


        .. versionadded:: 0.1.0

        """
        try:
            return self._tn / (self._tn + self._fp)
        except ZeroDivisionError:
            return float('nan')

    def fnr(self):
        r"""Return false negative rate.

        False negative rate is defined as

            .. math::

                \frac{fn}{tp + fn}

        AKA miss rate

        Cf. https://en.wikipedia.org/wiki/False_negative_rate

        Returns
        -------
        float
            The false negative rate of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> round(ct.fnr(), 8)
        0.2


        .. versionadded:: 0.4.0

        """
        return 1 - self.recall()

    def npv(self):
        r"""Return negative predictive value (NPV).

        NPV is defined as

            .. math::

                \frac{tn}{tn + fn}

        AKA inverse precision

        Cf. https://en.wikipedia.org/wiki/Negative_predictive_value

        Returns
        -------
        float
            The negative predictive value of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.npv()
        0.6666666666666666


        .. versionadded:: 0.1.0

        """
        try:
            return self._tn / (self._tn + self._fn)
        except ZeroDivisionError:
            return float('nan')

    def false_omission_rate(self):
        r"""Return false omission rate (FOR).

        FOR is defined as

            .. math::

                \frac{fn}{tn + fn}

        Cf. https://en.wikipedia.org/wiki/False_omission_rate

        Returns
        -------
        float
            The false omission rate of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.false_omission_rate()
        0.3333333333333333


        .. versionadded:: 0.4.0

        """
        try:
            return self._fn / (self._tn + self._fn)
        except ZeroDivisionError:
            return float('nan')

    def fallout(self):
        r"""Return fall-out.

        Fall-out is defined as

            .. math::

                \frac{fp}{fp + tn}

        AKA false positive rate (FPR)

        Cf. https://en.wikipedia.org/wiki/Information_retrieval#Fall-out

        Returns
        -------
        float
            The fall-out of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.fallout()
        0.25


        .. versionadded:: 0.1.0

        """
        return 1 - self.specificity()

    def pos_likelihood_ratio(self):
        r"""Return positive likelihood ratio.

        Positive likelihood ratio is defined as

            .. math::

                \frac{recall}{1-specificity}

        Cf.
        https://en.wikipedia.org/wiki/Likelihood_ratios_in_diagnostic_testing

        Returns
        -------
        float
            The positive likelihood ratio of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.pos_likelihood_ratio()
        3.2


        .. versionadded:: 0.4.0

        """
        return self.recall() / (1.0 - self.specificity())

    def neg_likelihood_ratio(self):
        r"""Return negative likelihood ratio.

        Negative likelihood ratio is defined as

            .. math::

                \frac{1-recall}{specificity}

        Cf.
        https://en.wikipedia.org/wiki/Likelihood_ratios_in_diagnostic_testing

        Returns
        -------
        float
            The negative likelihood ratio of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.neg_likelihood_ratio()
        0.2666666666666666


        .. versionadded:: 0.4.0

        """
        return (1.0 - self.recall()) / self.specificity()

    def diagnostic_odds_ratio(self):
        r"""Return diagnostic odds ratio.

        Diagnostic odds ratio is defined as

            .. math::

                \frac{tp \cdot tn}{fp \cdot fn}

        Cf.
        https://en.wikipedia.org/wiki/Diagnostic_odds_ratio

        Returns
        -------
        float
            The negative likelihood ratio of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.diagnostic_odds_ratio()
        12.0


        .. versionadded:: 0.4.0

        """
        try:
            return (self._tp * self._tn) / (self._fp * self._fn)
        except ZeroDivisionError:
            return float('nan')

    def fdr(self):
        r"""Return false discovery rate (FDR).

        False discovery rate is defined as

            .. math::

                \frac{fp}{fp + tp}

        Cf. https://en.wikipedia.org/wiki/False_discovery_rate

        Returns
        -------
        float
            The false discovery rate of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.fdr()
        0.14285714285714285


        .. versionadded:: 0.1.0

        """
        try:
            return self._fp / (self._fp + self._tp)
        except ZeroDivisionError:
            return float('nan')

    def accuracy(self):
        r"""Return accuracy.

        Accuracy is defined as

            .. math::

                \frac{tp + tn}{population}

        Cf. https://en.wikipedia.org/wiki/Accuracy

        Returns
        -------
        float
            The accuracy of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.accuracy()
        0.782608695652174


        .. versionadded:: 0.1.0

        """
        try:
            return (self._tp + self._tn) / self.population()
        except ZeroDivisionError:
            return float('nan')

    def accuracy_gain(self):
        r"""Return gain in accuracy.

        The gain in accuracy is defined as

            .. math::

                G(accuracy) = \frac{accuracy}{random~ accuracy}

        Cf. https://en.wikipedia.org/wiki/Gain_(information_retrieval)

        Returns
        -------
        float
            The gain in accuracy of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.accuracy_gain()
        1.4325259515570934


        .. versionadded:: 0.1.0

        """
        try:
            random_accuracy = (
                self.cond_pos_pop() / self.population()
            ) ** 2 + (self.cond_neg_pop() / self.population()) ** 2
            return self.accuracy() / random_accuracy
        except ZeroDivisionError:
            return float('nan')

    def balanced_accuracy(self):
        r"""Return balanced accuracy.

        Balanced accuracy is defined as

            .. math::

                \frac{sensitivity + specificity}{2}

        Cf. https://en.wikipedia.org/wiki/Accuracy

        Returns
        -------
        float
            The balanced accuracy of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.balanced_accuracy()
        0.775


        .. versionadded:: 0.1.0

        """
        return 0.5 * (self.recall() + self.specificity())

    def error_rate(self):
        r"""Return error rate.

        Error rate is defined as

            .. math::

                \frac{fp + fn}{population}

        Returns
        -------
        float
            The error rate of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.error_rate()
        0.21739130434782608


        .. versionadded:: 0.4.0

        """
        try:
            return (self._fn + self._fp) / (
                self._fn + self._fp + self._tn + self._tp
            )
        except ZeroDivisionError:
            return float('nan')

    def prevalence(self):
        r"""Return prevalence.

        Prevalence is defined as

            .. math::

                \frac{condition positive}{population}

        Cf. https://en.wikipedia.org/wiki/Prevalence

        Returns
        -------
        float
            The prevelence of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.prevalence()
        0.6521739130434783


        .. versionadded:: 0.4.0

        """
        try:
            return self.cond_pos_pop() / self.population()
        except ZeroDivisionError:
            return float('nan')

    def informedness(self):
        """Return informedness.

        Informedness is defined as

            .. math::

                sensitivity + specificity - 1

        AKA Youden's J statistic (:cite:`Youden:1950`)

        AKA DeltaP'

        Cf. https://en.wikipedia.org/wiki/Youden%27s_J_statistic

        Returns
        -------
        float
            The informedness of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.informedness()
        0.55


        .. versionadded:: 0.1.0

        """
        return self.recall() + self.specificity() - 1

    def markedness(self):
        """Return markedness.

        Markedness is defined as

            .. math::

                precision + npv - 1

        AKA DeltaP

        Returns
        -------
        float
            The markedness of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.markedness()
        0.5238095238095237


        .. versionadded:: 0.1.0

        """
        return self.precision() + self.npv() - 1

    def pr_amean(self):
        r"""Return arithmetic mean of precision & recall.

        The arithmetic mean of precision and recall is defined as

            .. math::

                \frac{precision \cdot recall}{2}

        Cf. https://en.wikipedia.org/wiki/Arithmetic_mean

        Returns
        -------
        float
            The arithmetic mean of the confusion table's precision & recall

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.pr_amean()
        0.8285714285714285


        .. versionadded:: 0.1.0

        """
        return amean((self.precision(), self.recall()))

    def pr_gmean(self):
        r"""Return geometric mean of precision & recall.

        The geometric mean of precision and recall is defined as:

            .. math::

                \sqrt{precision \cdot recall}

        Cf. https://en.wikipedia.org/wiki/Geometric_mean

        Returns
        -------
        float
            The geometric mean of the confusion table's precision & recall

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.pr_gmean()
        0.828078671210825


        .. versionadded:: 0.1.0

        """
        return gmean((self.precision(), self.recall()))

    def pr_hmean(self):
        r"""Return harmonic mean of precision & recall.

        The harmonic mean of precision and recall is defined as

            .. math::

                \frac{2 \cdot precision \cdot recall}{precision + recall}

        Cf. https://en.wikipedia.org/wiki/Harmonic_mean

        Returns
        -------
        float
            The harmonic mean of the confusion table's precision & recall

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.pr_hmean()
        0.8275862068965516


        .. versionadded:: 0.1.0

        """
        return hmean((self.precision(), self.recall()))

    def pr_qmean(self):
        r"""Return quadratic mean of precision & recall.

        The quadratic mean of precision and recall is defined as

            .. math::

                \sqrt{\frac{precision^{2} + recall^{2}}{2}}

        Cf. https://en.wikipedia.org/wiki/Quadratic_mean

        Returns
        -------
        float
            The quadratic mean of the confusion table's precision & recall

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.pr_qmean()
        0.8290638930598233


        .. versionadded:: 0.1.0

        """
        return qmean((self.precision(), self.recall()))

    def pr_cmean(self):
        r"""Return contraharmonic mean of precision & recall.

        The contraharmonic mean is

            .. math::

                \frac{precision^{2} + recall^{2}}{precision + recall}

        Cf. https://en.wikipedia.org/wiki/Contraharmonic_mean

        Returns
        -------
        float
            The contraharmonic mean of the confusion table's precision & recall

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.pr_cmean()
        0.8295566502463055


        .. versionadded:: 0.1.0

        """
        return cmean((self.precision(), self.recall()))

    def pr_lmean(self):
        r"""Return logarithmic mean of precision & recall.

        The logarithmic mean is:
        0 if either precision or recall is 0,
        the precision if they are equal,
        otherwise

            .. math::

                \frac{precision - recall}
                {ln(precision) - ln(recall)}

        Cf. https://en.wikipedia.org/wiki/Logarithmic_mean

        Returns
        -------
        float
            The logarithmic mean of the confusion table's precision & recall

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.pr_lmean()
        0.8282429171492667


        .. versionadded:: 0.1.0

        """
        precision = self.precision()
        recall = self.recall()
        if not precision or not recall:
            return 0.0
        elif precision == recall:
            return precision
        return (precision - recall) / (math.log(precision) - math.log(recall))

    def pr_imean(self):
        r"""Return identric (exponential) mean of precision & recall.

        The identric mean is:
        precision if precision = recall,
        otherwise

            .. math::

                \frac{1}{e} \cdot
                \sqrt[precision - recall]{\frac{precision^{precision}}
                {recall^{recall}}}

        Cf. https://en.wikipedia.org/wiki/Identric_mean

        Returns
        -------
        float
            The identric mean of the confusion table's precision & recall

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.pr_imean()
        0.8284071826325543


        .. versionadded:: 0.1.0

        """
        return imean((self.precision(), self.recall()))

    def pr_seiffert_mean(self):
        r"""Return Seiffert's mean of precision & recall.

        Seiffert's mean of precision and recall is

            .. math::

                \frac{precision - recall}{4 \cdot arctan
                \sqrt{\frac{precision}{recall}} - \pi}

        It is defined in :cite:`Seiffert:1993`.

        Returns
        -------
        float
            Seiffert's mean of the confusion table's precision & recall

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.pr_seiffert_mean()
        0.8284071696048312


        .. versionadded:: 0.1.0

        """
        return seiffert_mean((self.precision(), self.recall()))

    def pr_lehmer_mean(self, exp=2.0):
        r"""Return Lehmer mean of precision & recall.

        The Lehmer mean is

            .. math::

                \frac{precision^{exp} + recall^{exp}}
                {precision^{exp-1} + recall^{exp-1}}

        Cf. https://en.wikipedia.org/wiki/Lehmer_mean

        Parameters
        ----------
        exp : float
            The exponent of the Lehmer mean

        Returns
        -------
        float
            The Lehmer mean for the given exponent of the confusion table's
            precision & recall

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.pr_lehmer_mean()
        0.8295566502463055


        .. versionadded:: 0.1.0

        """
        return lehmer_mean((self.precision(), self.recall()), exp)

    def pr_heronian_mean(self):
        r"""Return Heronian mean of precision & recall.

        The Heronian mean of precision and recall is defined as

            .. math::

                \frac{precision + \sqrt{precision \cdot recall} + recall}{3}

        Cf. https://en.wikipedia.org/wiki/Heronian_mean

        Returns
        -------
        float
            The Heronian mean of the confusion table's precision & recall

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.pr_heronian_mean()
        0.8284071761178939


        .. versionadded:: 0.1.0

        """
        return heronian_mean((self.precision(), self.recall()))

    def pr_hoelder_mean(self, exp=2):
        r"""Return Hölder (power/generalized) mean of precision & recall.

        The power mean of precision and recall is defined as

            .. math::

                \frac{1}{2} \cdot
                \sqrt[exp]{precision^{exp} + recall^{exp}}

        for :math:`exp \ne 0`, and the geometric mean for :math:`exp = 0`

        Cf. https://en.wikipedia.org/wiki/Generalized_mean

        Parameters
        ----------
        exp : float
            The exponent of the Hölder mean

        Returns
        -------
        float
            The Hölder mean for the given exponent of the confusion table's
            precision & recall

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.pr_hoelder_mean()
        0.8290638930598233


        .. versionadded:: 0.1.0

        """
        return hoelder_mean((self.precision(), self.recall()), exp)

    def pr_agmean(self):
        """Return arithmetic-geometric mean of precision & recall.

        Iterates between arithmetic & geometric means until they converge to
        a single value (rounded to 12 digits)

        Cf. https://en.wikipedia.org/wiki/Arithmetic-geometric_mean

        Returns
        -------
        float
            The arithmetic-geometric mean of the confusion table's precision &
            recall

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.pr_agmean()
        0.8283250315702829


        .. versionadded:: 0.1.0

        """
        return agmean((self.precision(), self.recall()))

    def pr_ghmean(self):
        """Return geometric-harmonic mean of precision & recall.

        Iterates between geometric & harmonic means until they converge to
        a single value (rounded to 12 digits)

        Cf. https://en.wikipedia.org/wiki/Geometric-harmonic_mean

        Returns
        -------
        float
            The geometric-harmonic mean of the confusion table's precision &
            recall

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.pr_ghmean()
        0.8278323841238441


        .. versionadded:: 0.1.0

        """
        return ghmean((self.precision(), self.recall()))

    def pr_aghmean(self):
        """Return arithmetic-geometric-harmonic mean of precision & recall.

        Iterates over arithmetic, geometric, & harmonic means until they
        converge to a single value (rounded to 12 digits), following the
        method described in :cite:`Raissouli:2009`.

        Returns
        -------
        float
            The arithmetic-geometric-harmonic mean of the confusion table's
            precision & recall

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.pr_aghmean()
        0.8280786712108288


        .. versionadded:: 0.1.0

        """
        return aghmean((self.precision(), self.recall()))

    def fbeta_score(self, beta=1.0):
        r"""Return :math:`F_{\beta}` score.

        :math:`F_{\beta}` for a positive real value :math:`\beta` "measures
        the effectiveness of retrieval with respect to a user who
        attaches :math:`\beta` times as much importance to recall as
        precision" (van Rijsbergen 1979)

        :math:`F_{\beta}` score is defined as

            .. math::

                (1 + \beta^2) \cdot \frac{precision \cdot recall}
                {((\beta^2 \cdot precision) + recall)}

        Cf. https://en.wikipedia.org/wiki/F1_score

        Parameters
        ----------
        beta : float
            The :math:`\beta` parameter in the above formula

        Returns
        -------
        float
            The :math:`F_{\beta}` of the confusion table

        Raises
        ------
        AttributeError
            Beta must be a positive real value

        Examples
        --------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.fbeta_score()
        0.8275862068965518
        >>> ct.fbeta_score(beta=0.1)
        0.8565371024734982


        .. versionadded:: 0.1.0

        """
        if beta <= 0.0:
            raise AttributeError('Beta must be a positive real value.')
        precision = self.precision()
        recall = self.recall()
        return (
            (1.0 + beta ** 2)
            * precision
            * recall
            / ((beta ** 2 * precision) + recall)
        )

    def f2_score(self):
        """Return :math:`F_{2}`.

        The :math:`F_{2}` score emphasizes recall over precision in comparison
        to the :math:`F_{1}` score

        Cf. https://en.wikipedia.org/wiki/F1_score

        Returns
        -------
        float
            The :math:`F_{2}` of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.f2_score()
        0.8108108108108109


        .. versionadded:: 0.1.0

        """
        return self.fbeta_score(2.0)

    def fhalf_score(self):
        """Return :math:`F_{0.5}` score.

        The :math:`F_{0.5}` score emphasizes precision over recall in
        comparison to the :math:`F_{1}` score

        Cf. https://en.wikipedia.org/wiki/F1_score

        Returns
        -------
        float
            The :math:`F_{0.5}` score of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.fhalf_score()
        0.8450704225352114


        .. versionadded:: 0.1.0

        """
        return self.fbeta_score(0.5)

    def e_score(self, beta=1.0):
        r"""Return :math:`E`-score.

        This is Van Rijsbergen's effectiveness measure:
        :math:`E=1-F_{\beta}`.

        Cf. https://en.wikipedia.org/wiki/Information_retrieval#F-measure

        Parameters
        ----------
        beta : float
            The :math:`\beta` parameter in the above formula

        Returns
        -------
        float
            The :math:`E`-score of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.e_score()
        0.17241379310344818


        .. versionadded:: 0.1.0

        """
        return 1.0 - self.fbeta_score(beta)

    def f1_score(self):
        r"""Return :math:`F_{1}` score.

        :math:`F_{1}` score is the harmonic mean of precision and recall

            .. math::

                2 \cdot \frac{precision \cdot recall}{precision + recall}

        Cf. https://en.wikipedia.org/wiki/F1_score

        Returns
        -------
        float
            The :math:`F_{1}` of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.f1_score()
        0.8275862068965518


        .. versionadded:: 0.1.0

        """
        return self.fbeta_score(1.0)

    @deprecated(
        deprecated_in='0.4.0',
        removed_in='0.6.0',
        current_version=__version__,
        details='Use the ConfusionTable.pr_hmean method instead.',
    )
    def f_measure(self):
        r"""Return :math:`F`-measure.

        :math:`F`-measure is the harmonic mean of precision and recall

            .. math::

                2 \cdot \frac{precision \cdot recall}{precision + recall}

        Cf. https://en.wikipedia.org/wiki/F1_score

        Returns
        -------
        float
            The math:`F`-measure of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.f_measure()
        0.8275862068965516


        .. versionadded:: 0.1.0

        """
        return self.pr_hmean()

    def jaccard(self):
        r"""Return Jaccard index.

        The Jaccard index of a confusion table is

            .. math::

                \frac{tp}{tp+fp+fn}

        Returns
        -------
        float
            The Jaccard index of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.jaccard()
        0.7058823529411765


        .. versionadded:: 0.4.0

        """
        try:
            return self._tp / (self._tp + self._fp + self._fn)
        except ZeroDivisionError:
            return float('nan')

    @deprecated(
        deprecated_in='0.4.0',
        removed_in='0.6.0',
        current_version=__version__,
        details='Use the ConfusionTable.pr_gmean method instead.',
    )
    def g_measure(self):
        r"""Return G-measure.

        :math:`G`-measure is the geometric mean of precision and recall:

            .. math::

                \sqrt{precision \cdot recall}

        This is identical to the Fowlkes–Mallows (FM) index for two
        clusters.

        Cf. https://en.wikipedia.org/wiki/F1_score#G-measure

        Cf. https://en.wikipedia.org/wiki/Fowlkes%E2%80%93Mallows_index

        Returns
        -------
        float
            The :math:`G`-measure of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.g_measure()
        0.828078671210825


        .. versionadded:: 0.1.0

        """
        return self.pr_gmean()

    def d_measure(self):
        r"""Return D-measure.

        :math:`D`-measure is defined as

            .. math::

                1-\frac{1}{\frac{1}{precision}+\frac{1}{recall}-1}

        Returns
        -------
        float
            The :math:`D`-measure of the confusion table

        Examples
        --------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.d_measure()
        0.2941176470588237


        .. versionadded:: 0.4.0

        """
        return 1.0 - (
            1.0 / (1.0 / self.precision() + 1.0 / self.recall() - 1.0)
        )

    def mcc(self):
        r"""Return Matthews correlation coefficient (MCC).

        The Matthews correlation coefficient is defined in
        :cite:`Matthews:1975` as:

            .. math::

                \frac{(tp \cdot tn) - (fp \cdot fn)}
                {\sqrt{(tp + fp)(tp + fn)(tn + fp)(tn + fn)}}

        This is equivalent to the geometric mean of informedness and
        markedness, defined above.

        Cf. https://en.wikipedia.org/wiki/Matthews_correlation_coefficient

        Returns
        -------
        float
            The Matthews correlation coefficient of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.mcc()
        0.5367450401216932


        .. versionadded:: 0.1.0

        """
        try:
            return ((self._tp * self._tn) - (self._fp * self._fn)) / math.sqrt(
                (self._tp + self._fp)
                * (self._tp + self._fn)
                * (self._tn + self._fp)
                * (self._tn + self._fn)
            )
        except ZeroDivisionError:
            return float('nan')

    def significance(self):
        r"""Return the significance, :math:`\chi^{2}`.

        Significance is defined as

            .. math::

                \chi^{2} =
                \frac{(tp \cdot tn - fp \cdot fn)^{2} (tp + tn + fp + fn)}
                {((tp + fp)(tp + fn)(tn + fp)(tn + fn)}`

        Also: :math:`\chi^{2} = MCC^{2} \cdot n`

        Cf. https://en.wikipedia.org/wiki/Pearson%27s_chi-square_test

        Returns
        -------
        float
            The significance of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.significance()
        66.26190476190476


        .. versionadded:: 0.1.0

        """
        try:
            return (
                (self._tp * self._tn - self._fp * self._fn) ** 2
                * (self._tp + self._tn + self._fp + self._fn)
            ) / (
                (self._tp + self._fp)
                * (self._tp + self._fn)
                * (self._tn + self._fp)
                * (self._tn + self._fn)
            )
        except ZeroDivisionError:
            return float('nan')

    def kappa_statistic(self):
        r"""Return κ statistic.

        The κ statistic is defined as

            .. math::

                \kappa = \frac{accuracy - random~ accuracy}
                {1 - random~ accuracy}`

        The κ statistic compares the performance of the classifier relative to
        the performance of a random classifier. :math:`\kappa` = 0 indicates
        performance identical to random. :math:`\kappa` = 1 indicates perfect
        predictive success. :math:`\kappa` = -1 indicates perfect predictive
        failure.

        Returns
        -------
        float
            The κ statistic of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.kappa_statistic()
        0.5344129554655871


        .. versionadded:: 0.1.0

        """
        try:
            random_accuracy = (
                (self._tn + self._fp) * (self._tn + self._fn)
                + (self._fn + self._tp) * (self._fp + self._tp)
            ) / self.population() ** 2
            return (self.accuracy() - random_accuracy) / (1 - random_accuracy)
        except ZeroDivisionError:
            return float('nan')

    def phi_coefficient(self):
        r"""Return φ coefficient.

        The :math:`\phi` coefficient is defined as

            .. math::

                \phi = \frac{tp \cdot tn - fp \cdot tn}
                {\sqrt{(tp + fp) \cdot (tp + fn) \cdot (tn + fp) \cdot
                (tn + fn)}}

        Returns
        -------
        float
            The φ coefficient of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.phi_coefficient()
        0.5367450401216932


        .. versionadded:: 0.4.0

        """
        try:
            return ((self._tp * self._tn) - (self._fp * self._fn)) / (
                (self._tp + self._fn)
                * (self._tp + self._fp)
                * (self._tn + self._fn)
                * (self._tn + self._fp)
            ) ** 0.5
        except ZeroDivisionError:
            return float('nan')

    def joint_entropy(self):
        """Return the joint entropy.

        Implementation based on https://github.com/Magnetic/proficiency-metric

        Returns
        -------
        float
            The joint entropy of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.joint_entropy()
        1.1680347446270396


        .. versionadded:: 0.4.0

        """
        try:
            return (
                math.log(self.population())
                - sum(_ * math.log(_) for _ in self.to_tuple())
                / self.population()
            )
        except ValueError:
            return float('nan')

    def actual_entropy(self):
        """Return the actual entropy.

        Implementation based on https://github.com/Magnetic/proficiency-metric

        Returns
        -------
        float
            The actual entropy of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.actual_entropy()
        0.6460905050608101


        .. versionadded:: 0.4.0

        """
        try:
            return (
                math.log(self.population())
                - sum(
                    _ * math.log(_)
                    for _ in (self.cond_pos_pop(), self.cond_neg_pop())
                )
                / self.population()
            )
        except ValueError:
            return float('nan')

    def predicted_entropy(self):
        """Return the predicted entropy.

        Implementation based on https://github.com/Magnetic/proficiency-metric

        Returns
        -------
        float
            The predicted entropy of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.predicted_entropy()
        0.6693279632926457


        .. versionadded:: 0.4.0

        """
        try:
            return (
                math.log(self.population())
                - sum(
                    _ * math.log(_)
                    for _ in (self.pred_pos_pop(), self.pred_neg_pop())
                )
                / self.population()
            )
        except ValueError:
            return float('nan')

    def mutual_information(self):
        """Return the mutual information.

        Implementation based on https://github.com/Magnetic/proficiency-metric

        Returns
        -------
        float
            The mutual information of the confusion table

        Cf. https://en.wikipedia.org/wiki/Mutual_information

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.mutual_information()
        0.14738372372641576


        .. versionadded:: 0.4.0

        """
        try:
            return (
                sum(
                    _[0] * math.log(self.population() * _[0] / _[1])
                    for _ in (
                        (
                            (
                                self._fp,
                                self.cond_neg_pop() * self.pred_pos_pop(),
                            ),
                            (
                                self._fn,
                                self.cond_pos_pop() * self.pred_neg_pop(),
                            ),
                            (
                                self._tn,
                                self.cond_neg_pop() * self.pred_neg_pop(),
                            ),
                            (
                                self._tp,
                                self.cond_pos_pop() * self.pred_pos_pop(),
                            ),
                        )
                    )
                )
                / self.population()
            )
        except ZeroDivisionError:
            return float('nan')

    def proficiency(self):
        """Return the proficiency.

        Implementation based on https://github.com/Magnetic/proficiency-metric
        :cite:`Steingold:2015`

        AKA uncertainty coefficient

        Cf. https://en.wikipedia.org/wiki/Uncertainty_coefficient

        Returns
        -------
        float
            The proficiency of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.proficiency()
        0.228116219897929


        .. versionadded:: 0.4.0

        """
        return self.mutual_information() / self.actual_entropy()

    def igr(self):
        """Return information gain ratio.

        Implementation based on https://github.com/Magnetic/proficiency-metric

        Cf. https://en.wikipedia.org/wiki/Information_gain_ratio

        Returns
        -------
        float
            The information gain ratio of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.igr()
        0.22019657299448012


        .. versionadded:: 0.4.0

        """
        return self.mutual_information() / self.predicted_entropy()

    def dependency(self):
        """Return dependency.

        Implementation based on https://github.com/Magnetic/proficiency-metric

        Returns
        -------
        float
            The dependency of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.dependency()
        0.12618094145262454


        .. versionadded:: 0.4.0

        """
        return self.mutual_information() / self.joint_entropy()

    def lift(self):
        """Return lift.

        Implementation based on https://github.com/Magnetic/proficiency-metric

        Returns
        -------
        float
            The lift of the confusion table

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.lift()
        1.3142857142857143


        .. versionadded:: 0.4.0

        """
        try:
            return (
                self._tp
                * self.population()
                / (self.pred_pos_pop() * self.cond_pos_pop())
            )
        except ZeroDivisionError:
            return float('nan')


if __name__ == '__main__':
    import doctest

    doctest.testmod()
