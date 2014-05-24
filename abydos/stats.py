# -*- coding: utf-8 -*-
"""abydos.stats

The stats module defines functions for calculating various statistical data
about linguistic objects.

This includes the ConfusionTable object, which includes members cable of
calculating the following data based on a confusion table:
    population counts
    precision, recall, specificity, negative predictive value, fall-out,
        false discovery rate, accuracy, balanced accuracy, informedness,
        and markedness
    various means of the precision & recall, including: arithmetic, geometric,
        harmonic, quadratic, logarithmic, contraharmonic, identic, & power
        means
    F_{β}-scores, E-scores, G-measures, along with special functions for
        F1, F-1/2, and F2 scores
    significance & Matthews correlation coefficient calculation


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
from ._compat import _unicode
import math

class ConfusionTable(object):
    """ConfusionTable object

    This object is initialized by passing either four integers (or a tuple of
    four integers) representing the squares of a confusion table:
    true positives, true negatives, false positives, and false negatives

    The object possesses methods for the caluculation of various statistics
    based on the confusion table.
    """
    tpos, tneg, fpos, fneg = 0, 0, 0, 0

    def __init__(self, tp=0, tn=0, fp=0, fn=0):
        if isinstance(tp, tuple) or isinstance(tp, list):
            if len(tp) == 4:
                self.tpos = tp[0]
                self.tneg = tp[1]
                self.fpos = tp[2]
                self.fneg = tp[3]
            else:
                raise AttributeError('ConfusionTable requires a 4-tuple when \
                being created from a tuple.')
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
        """Return True if two ConfusionTables are the same object or all four
        of their attributes are equal
        """
        if isinstance(other, ConfusionTable):
            if id(self) == id(other):
                return True
            if (self.tpos == other.tpos and self.tneg == other.tneg and
                self.fpos == other.fpos and self. fneg == other.fneg):
                return True
        elif isinstance(other, tuple) or isinstance(other, list):
            if (self.tpos == other[0] and self.tneg == other[1] and
                self.fpos == other[2] and self.fneg == other[3]):
                return True
        elif isinstance(other, dict):
            if (self.tpos == other['tp'] and self.tneg == other['tn'] and
                self.fpos == other['fp'] and self.fneg == other['fn']):
                return True 
        return False


    def __str__(self):
        """Return a human-readable version of the confusion table
        """
        return ('tp:' + _unicode(self.tpos) + ' tn:' + _unicode(self.tneg) +
                ' fp:' + _unicode(self.fpos) + ' fn:' + _unicode(self.fneg))


    def tuple(self):
        """Return the confusion table as a 4-tuple (tp, tn, fp, fn)
        """
        return (self.tpos, self.tneg, self.fpos, self.fneg)


    def dict(self):
        """Return the confusion table as a dict
        """
        return {'tp':self.tpos, 'tn':self.tneg,
                'fp':self.fpos, 'fn':self.fneg}


    def correct_pop(self):
        """Return the correct population of the confusion table
        """
        return self.tpos + self.tneg


    def error_pop(self):
        """Return the error population of the confusion table
        """
        return self.fpos + self.fneg


    def test_pos_pop(self):
        """Return the test positive population of the confusion table
        """
        return self.tpos + self.fpos


    def test_neg_pop(self):
        """Return the test negative population of the confusion table
        """
        return self.tneg + self.fneg


    def cond_pos_pop(self):
        """Return the condition positive population of the confusion table
        """
        return self.tpos + self.fneg


    def cond_neg_pop(self):
        """Return the condition negative population of the confusion table
        """
        return self.fpos + self.tneg


    def population(self):
        """Return the population (N) of the confusion table
        """
        return self.tpos + self.tneg + self.fpos + self.fneg


    def precision(self):
        """Return the precision of the confusion table

	    Precision is defined as tp / (tp+fp)
	    AKA positive predictive value (PPV)
	    """
        if self.tpos + self.fpos == 0:
            return float('NaN')
        return self.tpos / (self.tpos + self.fpos)


    def recall(self):
        """Return the recall of the confusion table

        Recall is defined as tp / (tp+fn)
        AKA sensitivity
        AKA true positive rate (TPR)
        """
        if self.tpos + self.fneg == 0:
            return float('NaN')
        return self.tpos / (self.tpos + self.fneg)


    def specificity(self):
        """Return the specificity of the confusion table

        Specificity is defined as tn / (tn+fp)
        AKA true negative rate (TNR)
        """
        if self.tneg + self.fpos == 0:
            return float('NaN')
        return self.tneg / (self.tneg + self.fpos)


    def npv(self):
        """Return the negative predictive value (NPV) of the
        confusion table

        NPV is defined as tn / (tn+fn)
        """
        if self.tneg + self.fneg == 0:
            return float('NaN')
        return self.tneg / (self.tneg + self.fneg)


    def fallout(self):
        """Return the fall-out of the confusion table

        Fall-out is defined as fp / (fp+tn)
        AKA false positive rate (FPR)
        """
        if self.fpos + self.tneg == 0:
            return float('NaN')
        return self.fpos / (self.fpos + self.tneg)


    def fdr(self):
        """Return the false discovery rate (FDR) of the confusion
        table

        False discovery rate is defined as fp / (fp+tp)
        """
        if self.fpos + self.tpos == 0:
            return float('NaN')
        return self.fpos / (self.fpos + self.tpos)


    def accuracy(self):
        """Return the accuracy of the confusion table

        Accuracy is defined as (tp + tn) / population
        """
        if self.population() == 0:
            return float('NaN')
        return (self.tpos + self.tneg) / self.population()


    def balanced_accuracy(self):
        """Return the balanced accuracy of the confusion table

        Balanced accuracy is defined as
        (sensitivity+specificity) / 2
        """
        return 0.5 * (self.recall() + self.specificity())


    def informedness(self):
        """Return the informedness of the confusion table

        Informedness is defined as sensitivity+specificity-1.
        AKA Youden's J statistic
        """
        return self.recall() + self.specificity() - 1


    def markedness(self):
        """Return the markedness of the confusion table

        Markedness is defined as precision + npv -1
        """
        return self.precision() + self.npv() - 1


    def pr_mean(self):
        """Return the arithmetic mean of precision & recall of the
        confusion table

        The arithmetic mean of precision and recall is defined as:
        (precision * recall)/2
        """
        return (self.precision() + self.recall()) / 2


    def pr_gmean(self):
        """Return the geometric mean of precision & recall of the
        confusion table

        The geometric mean of precision and recall is defined as:
        √(precision * recall)
        """
        return math.sqrt(self.precision() * self.recall())


    def pr_hmean(self):
        """Return the harmonic mean of precision & recall of the
        confusion table

        The geometric mean of precision and recall is defined as:
        sqrt(precision * recall)
        """
        precision = self.precision()
        recall = self.recall()
        return 2 * precision * recall / (precision + recall)


    def pr_qmean(self):
        """Return the quadratic mean of precision & recall of the
        confusion table

        The quadratic mean of precision and recall is defined as:
        √((precision^2 + recall^2)/2)
        """
        return math.sqrt((self.precision()**2 + self.recall()**2) / 2)


    def pr_lmean(self):
        """Return the logarithmic mean of precision & recall of
        the confusion table

        The logarithmic mean is:
        0 if either precision or recall is 0,
        the precision if they are equal,
        otherwise (precision - recall) / ln(precision) - ln(recall)
        """
        precision = self.precision()
        recall = self.recall()
        if not precision or not recall:
            return 0
        elif precision == recall:
            return precision
        else:
            return ((precision - recall) /
                    (math.log(precision) - math.log(recall)))


    def pr_cmean(self):
        """Return the contraharmonic mean of precision & recall
        of the confusion table

        The contraharmonic mean is:
        (precision^2 + recall^2) / (precision + recall)
        """
        precision = self.precision()
        recall = self.recall()
        return (precision**2 + recall**2)/(precision + recall)


    def pr_imean(self):
        """Return the identric mean of precision & recall of the
        confusion table

        The identric mean is:
        precision if precision = recall,
        otherwise (1/e) *
                (precision^precision / recall^recall)^(1 / (precision - recall))
        """
        precision = self.precision()
        recall = self.recall()
        if precision <= 0 or recall <= 0:
            return float('NaN')
        elif precision == recall:
            return precision
        return ((1/math.e) *
                (precision**precision/recall**recall)**(1/(precision-recall)))


    def pr_pmean(self, exp=2):
        """Return the power mean of precision & recall of the
        confusion table

        The exp mean of precision and recall is defined as:
        (0.5 * (precision^exp + recall^exp))^(1/exp)
        """
        return (0.5 * (self.precision()**exp + self.recall()**exp))**(1/exp)


    def fbeta_score(self, beta=1):
        """Return the F_{β} score of the confusion table

        F_{β} for a positive real value β "measures the
        effectiveness of retrieval with respect to a user who
        attaches β times as much importance to recall as
        precision" (van Rijsbergen 1979)

        F_{β} score is defined as:
        (1 + β^2) * precision * recall /
        ((β^2 * precision) + recall)
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
        """
        return self.fbeta_score(2)


    def fhalf_score(self):
        """Return the F_{0.5} score of the confusion table,
        which emphasizes precision over recall in comparison
        to the F_{1} score
        """
        return self.fbeta_score(0.5)


    def e_score(self, beta=1):
        """Return the E-score (Van Rijsbergen's effectiveness
        measure)
        """
        return 1-self.fbeta_score(beta)


    def f1_score(self):
        """Return the F_{1} score of the confusion table

        F_{1} score is the harmonic mean of precision and recall:
        2*(precision*recall) / (precision+recall)
        """
        return self.pr_hmean()


    def f_measure(self):
        """Return the F-measure of the confusion table

        F-measure is the harmonic mean of precision and recall:
        2*(precision*recall) / (precision+recall)
        """
        return self.pr_hmean()


    def g_measure(self):
        """Return the G-measure of the confusion table

        G-measure is the geometric mean of precision and recall:
        √(precision * recall)
        """
        return self.pr_gmean()


    def mcc(self):
        """Return the Matthews correlation coefficient of the
        confusion table

        The Matthews correlation coefficient is defined as:
        ((tp * tn) - (fp * fn)) /
        sqrt((tp + fp)(tp + fn)(tn + fp)(tn + fn))
        """
        if ((self.tpos + self.fpos) * (self.tpos + self.fneg) *
            (self.tneg + self.fpos) * (self.tneg + self.fneg)) == 0:
            return float('NaN')
        return (((self.tpos * self.tneg) - (self.fpos * self.fneg)) /
                math.sqrt((self.tpos + self.fpos) * (self.tpos + self.fneg) *
                          (self.tneg + self.fpos) * (self.tneg + self.fneg)))


    def significance(self):
        """Return the significance of the confusion table

        Significance is defined as:
        (tp * tn - fp * fn)^2 (tp + tn + fp + fn) /
        ((tp + fp)(tp + fn)(tn + fp)(tn + fn))
        """
        if ((self.tpos + self.fpos) * (self.tpos + self.fneg) *
            (self.tneg + self.fpos) * (self.tneg + self.fneg)) == 0:
            return float('NaN')
        return (((self.tpos * self.tneg - self.fpos * self.fneg)**2 *
                 (self.tpos + self.tneg + self.fpos + self.fneg)) /
                ((self.tpos + self.fpos) * (self.tpos + self.fneg) *
                 (self.tneg + self.fpos) * (self.tneg + self.fneg)))
