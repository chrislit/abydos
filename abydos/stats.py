# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
import math

class ConfusionTable:
    tp, fn, fp, fn = 0, 0, 0, 0

    def __init__(self, tp=0, tn=0, fp=0, fn=0):
        if isinstance(tp, tuple) or isinstance(tp, list):
            if len(tp) == 4:
                self.tp = tp[0]
                self.tn = tp[1]
                self.fp = tp[2]
                self.fn = tp[3]
            else:
                raise AttributeError('ConfusionTable requires a 4-tuple when being created from a tuple.')
        else:
            self.tp = tp
            self.tn = tn
            self.fp = fp
            self.fn = fn


    def __str__(self):
        """Return a human-readable version of the confusion table
        """
        return 'tp:' + str(self.tp) + ' tn:' + str(self.tn) + ' fp:' + str(self.fp) + ' fn:' + str(self.fn)


    def tuple(self):
        """Return the confusion table as a 4-tuple (tp, tn, fp, fn)
        """
        return (self.tp, self.tn, self.fp, self.fn)


    def dict(self):
        """Return the confusion table as a dict
        """
        return {'tp':self.tp, 'tn':self.tn, 'fp':self.fp, 'fn':self.fn}


    def correct_pop(self):
        """Return the correct population of the confusion table
        """
        return self.tp + self.tn


    def error_pop(self):
        """Return the correct population of the confusion table
        """
        return self.fp + self.fn


    def test_pos_pop(self):
        """Return the correct population of the confusion table
        """
        return self.tp + self.fp


    def test_neg_pop(self):
        """Return the correct population of the confusion table
        """
        return self.tn + self.fn


    def cond_pos_pop(self):
        """Return the correct population of the confusion table
        """
        return self.tp + self.fn


    def cond_neg_pop(self):
        """Return the correct population of the confusion table
        """
        return self.fp + self.tn


    def population(self):
        """Return the population (N) of the confusion table
        """
        return self.tp + self.tn + self.fp + self.fn


    def precision(self):
        """Return the precision of the confusion table

	    Precision is defined as tp / (tp+fp)
	    AKA positive predictive value (PPV)
	    """
        return self.tp / (self.tp + self.fp)


    def recall(self):
        """Return the recall of the confusion table

        Recall is defined as tp / (tp+fn)
        AKA sensitivity
        AKA true positive rate (TPR)
        """
        return self.tp / (self.tp + self.fn)


    def specificity(self):
        """Return the specificity of the confusion table

        Specificity is defined as tn / (tn+fp)
        AKA true negative rate (TNR)
        """
        return self.tn / (self.tn + self.fp)


    def npv(self):
        """Return the negative predictive value (NPV) of the
        confusion table

        NPV is defined as tn / (tn+fn)
        """
        return self.tn / (self.tn + self.fn)


    def fallout(self):
        """Return the fall-out of the confusion table

        Fall-out is defined as fp / (fp+tn)
        AKA false positive rate (FPR)
        """
        return self.fp / (self.fp / self.tn)


    def fdr(self):
        """Return the false discovery rate (FDR) of the confusion
        table

        False discovery rate is defined as fp / (fp+tp)
        """
        return self.fp / (self.fp + self.tp)


    def accuracy(self):
        """Return the accuracy of the confusion table

        Accuracy is defined as (tp + tn) / population
        """
        return (self.tp + self.tn) / self.population()


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
        """Return the geometric mean of precision & recall of the confusion table

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
        p = self.precision()
        r = self.recall()
        return 2 * p * r / (p + r)


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
        p = self.precision()
        r = self.recall()
        if not p or not r:
            return 0
        elif p == r:
            return p
        else:
            return (p - r) / (math.log(p) - math.log(r))


    def pr_cmean(self):
        """Return the contraharmonic mean of precision & recall
        of the confusion table

        The contraharmonic mean is:
        (precision^2 + recall^2) / (precision + recall)
        """
        p = self.precision()
        r = self.recall()
        return (p**2 + r**2)/(p + r)


    def pr_imean(self):
        """Return the identric mean of precision & recall of the
        confusion table

        The identric mean is:
        precision if precision = recall,
        otherwise (1/e) * (precision^precision / recall^recall)^(1 / (precision - recall))
        """
        p = self.precision()
        r = self.recall()
        return (1/math.e) * (p**p/r**r)**(1/(p-r))


    def pr_pmean(self, m=2):
        """Return the power mean of precision & recall of the
        confusion table

        The m-power mean of precision and recall is defined as:
        (0.5 * (precision^m + recall^m))^(1/m)
        """
        return (0.5 * (self.precision()**m + self.recall()**m))**(1/m)


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
        p = self.precision()
        r = self.recall()
        return (1 + beta**2) * p * r / ((beta**2 * p) + r)


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
        return ((self.tp * self.tn) - (self.fp * self.fn)) / math.sqrt((self.tp + self.fp) * (self.tp + self.fn) * (self.tn + self.fp) * (self.tn + self.fn))


    def significance(self):
        """Return the significance of the confusion table

        Significance is defined as:
        (tp * tn - fp * fn)^2 (tp + tn + fp + fn) /
        ((tp + fp)(tp + fn)(tn + fp)(tn + fn))
        """
        return ((self.tp * self.tn - self.fp * self.fn)**2 * (self.tp + self.tn + self.fp + self.fn)) / ((self.tp + self.fp) * (self.tp + self.fn) * (self.tn + self.fp) * (self.tn + self.fn))
