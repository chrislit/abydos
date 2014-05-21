# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from ._compat import _range

def qgrams(s, q=2, start_stop='#'):
    """Returns a list of all q-grams of a string.

    Arguments:
    s -- a string to extract q-grams from
    q -- the q-gram length (defaults to 2)
    start_stop -- a string of length >= 0 indicating start & stop symbols
        If the string is '', q-grams will be calculated without start & stop
        symbols appended to each end.
        Otherwise, the first character of start_stop will pad the beginning of
        the string and the last character of start_stop will pad the end of the
        string before q-grams are calculated. (In the case that start_stop is
        only 1 character long, the same symbol will be used for both.)

    A q-gram is here defined as all sequences of q characters. Q-grams are also
    known as k-grams and n-grams, but the term n-gram more typically refers to
    sequences of whitespace-delimited words in a string, where q-gram refers
    to sequences of characters in a word or string.
    """
    if len(s) < q:
        return []
    if start_stop and q > 1:
        s = start_stop[0]*(q-1) + s + start_stop[-1]*(q-1)
    return [s[i:i+q] for i in _range(len(s)-(q-1))]


def _qgram_lists(s, t, q=2):
    """Return a tuple for the two supplied strings, consisting of:
        (q-grams in s, q-grams in t, q-grams in common).

    Arguments:
    s, t -- strings to extract q-grams from
    q -- the q-gram length (defaults to 2)
    """
    q_s = qgrams(s, q)
    q_t = qgrams(t, q)
    q_common = []
    q_t_save = list(q_t)

    for qg in q_s:
        if qg in q_t:
            q_t.remove(qg)
            q_common.append(qg)
    return (q_s, q_t_save, q_common)


def _qgram_counts(s, t, q=2):
    """Return a tuple for the two supplied strings, consisting of:
        (|q-grams in s|, |q-grams in t|, |q-grams in common|).
    These are the number of q-grams in each set.

    Arguments:
    s, t -- strings to extract q-grams from
    q -- the q-gram length (defaults to 2)
    """
    return tuple([len(elt) for elt in _qgram_lists(s, t, q)])
