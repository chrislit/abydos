# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unicodedata

def qgrams(s, q=2):
    """Given a string s, return a list of all q-grams in that
    string for a specified value q (defaults to 2).
    
    A q-gram is here defined as all sequences of q characters.
    """
    if len(s) < q:
        return []
    return [s[i:i+q] for i in range(len(s)-(q-1))]

def _qgram_counts(s, t, q=2):
    """Given strings s and t, return a tuple of:
      the number of q-grams in s
      the number of q-grams in t
      the number of q-grams in common
    An optional argument q (defaults to 2) specifies the length of
    each q-gram.
    """
    q_s = qgrams(s, q)
    q_t = qgrams(t, q)

    s_count = len(q_s)
    t_count = len(q_t)

    for qg in q_s:
        if qg in q_t:
            q_s.remove(qg)
            q_t.remove(qg)
    return (s_count, t_count, s_count-len(q_s))

def _decompose(s):
    """Given a string s, return the string decomposed according to
    Unicode NFD normalization.
    """
    return unicodedata.normalize('NFD', s)
