# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from math import sqrt

def precision(stats):
    """Return the precision, given a 4-tuple:
    (true positives [tp], true negatives [tn],
     false positives [fp], false negatives [fn])

    Precision is defined as tp / (tp+fp)
    """
    return float(stats[0]) / (stats[0]+stats[2])

def PPV(stats):
    """Return the positive_predictive_value (PPV),
    given a 4-tuple:
    (true positives [tp], true negatives [tn],
     false positives [fp], false negatives [fn])

    PPV is defined as tp / (tp+fp) and is identical to recall
    """
    return precision(stats)

def precision(stats):
    """Return the precision, given a 4-tuple:
    (true positives [tp], true negatives [tn],
     false positives [fp], false negatives [fn])

    Precision is defined as tp / (tp+fp)
    """
    return float(stats[0]) / (stats[0]+stats[2])

def recall(stats):
    """Return the recall, given a 4-tuple:
    (true positives [tp], true negatives [tn],
     false positives [fp], false negatives [fn])

    Recall is defined as tp / (tp+fn)
    """
    return float(stats[0]) / (stats[0]+stats[3])

def sensitivity(stats):
    """Return the sensitivity, given a 4-tuple:
    (true positives [tp], true negatives [tn],
     false positives [fp], false negatives [fn])

    Sensitivity is defined as tp / (tp+fn) and is identical
    to recall.
    """
    return recall(stats)

def specificity(stats):
    """Return the specificity, given a 4-tuple:
    (true positives [tp], true negatives [tn],
     false positives [fp], false negatives [fn])

    Specificity is defined as tn / (fp+tn)
    """
    return float(stats[1]) / (stats[2]+stats[1])

def NPV(stats):
    """Return the negative_predictive_value (NPV),
    given a 4-tuple:
    (true positives [tp], true negatives [tn],
     false positives [fp], false negatives [fn])

    NPV is defined as tn / (tn+fn)
    """
    return float(stats[1]) / (stats[1]/stats[3])

def accuracy(stats):
    """Return the accuracy, given a 4-tuple:
    (true positives [tp], true negatives [tn],
     false positives [fp], false negatives [fn])

    Accuracy is defined as tp / (tp+fn)
    """
    return float(stats[0]+stats[1]) / sum(stats)

def balanced_accuracy(stats):
    """Return the balanced accuracy, given a 4-tuple:
    (true positives [tp], true negatives [tn],
     false positives [fp], false negatives [fn])

    Balanced accuracy is defined as (sensitivity+specificity) / 2
    """
    return 0.5*(sensitivity(stats)+specificity(stats))

def informedness(stats):
    """Return the informedness, given a 4-tuple:
    (true positives [tp], true negatives [tn],
     false positives [fp], false negatives [fn])

    Informedness is defined as sensitivity+specificity-1
    """
    return sensitivity(stats)+specificity(stats)-1

def PR_arithmetic_mean(stats):
    """Return the arithmetic mean of precision & recall, given a 4-tuple
    (true positives [tp], true negatives [tn],
     false positives [fp], false negatives [fn])

    The arithmetic mean of precision and recall is defined as:
    (precision * recall)/2
    """
    return (precision(stats)+recall(stats))/2

def PR_geometric_mean(stats):
    """Return the geometric mean of precision & recall, given a 4-tuple
    (true positives [tp], true negatives [tn],
     false positives [fp], false negatives [fn])

    The geometric mean of precision and recall is defined as:
    √(precision * recall)
    """
    return math.sqrt(precision(stats)*recall(stats))

def PR_harmonic_mean(stats):
    """Return the harmonic mean of precision & recall, given a 4-tuple
    (true positives [tp], true negatives [tn],
     false positives [fp], false negatives [fn])

    The geometric mean of precision and recall is defined as:
    sqrt(precision * recall)
    """
    p = precision(stats)
    r = recall(stats)
    return 2.0 * p * r / (p + r)

def PR_quadratic_mean(stats):
    """Return the quadratic mean of precision & recall, given a 4-tuple
    (true positives [tp], true negatives [tn],
     false positives [fp], false negatives [fn])

    The quadratic mean of precision and recall is defined as:
    √((precision^2 + recall^2)/2)
    """
    return math.sqrt((precision(stats)**2 + recall(stats)**2)/2)

def PR_power_mean(stats, m=2):
    """Return the power mean of precision & recall, given a 4-tuple
    (true positives [tp], true negatives [tn],
     false positives [fp], false negatives [fn])

    The m-power mean of precision and recall is defined as:
    (0.5 * (precision^m + recall^m))^(1/m)
    """
    return (0.5 * (precision(stats)**m + recall(stats)**m))**(1.0/m)

def Fbeta_score(stats, beta=1):
    """Return the F_{β} score, given a 4-tuple:
    (true positives [tp], true negatives [tn],
     false positives [fp], false negatives [fn])

    F_{β} for a positive real value β "measures the effectiveness
    of retrieval with respect to a user who attaches β times as
    much importance to recall as precision" (van Rijsbergen 1979)

    F_{β} score is defined as:
    (1 + β^2) * precision * recall / ((β^2 * precision) + recall)
    """
    p = precision(stats)
    r = recall(stats)
    return float(1 + beta**2) * p * r / ((beta**2 * p) + r)

def E_score(stats, beta=1):
    return 1-Fbeta_score(stats, beta)

def F1_score(stats):
    """Return the F_{1} score, given a 4-tuple:
    (true positives [tp], true negatives [tn],
     false positives [fp], false negatives [fn])

    F_{1} score is the harmonic mean of precision and recall:
    2*(precision*recall) / (precision+recall)
    """
    return PR_harmonic_mean(stats)

def F_measure(stats):
    """Return the F-measure, given a 4-tuple
    (true positives [tp], true negatives [tn],
     false positives [fp], false negatives [fn])

    F-measure is the harmonic mean of precision and recall:
    2*(precision*recall) / (precision+recall)
    """
    return F1_score(stats)

def G_measure(stats):
    """Return the G-measure, given a 4-tuple
    (true positives [tp], true negatives [tn],
     false positives [fp], false negatives [fn])

    G-measure is the geometric mean of precision and recall:
    √(precision * recall)
    """
    return PR_geometric_mean(stats)

