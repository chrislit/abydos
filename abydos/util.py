# -*- coding: utf-8 -*-

from __future__ import unicode_literals

def qgrams(s, q=2):
    """Returns a list of all q-grams of a string.

    Arguments:
    s -- a string to extract q-grams from
    q -- the q-gram length (defaults to 2)

    A q-gram is here defined as all sequences of q characters. Q-grams are also
    known as k-grams and n-grams, but the term n-gram more typically refers to
    sequences of whitespace-delimited words in a string, where q-gram refers
    to sequences of characters in a word or string.
    """
    if len(s) < q:
        return []
    return [s[i:i+q] for i in range(len(s)-(q-1))]


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
    q_s_save = list(q_s)
    q_t_save = list(q_t)

    for qg in q_s:
        if qg in q_t:
            q_s.remove(qg)
            q_t.remove(qg)
            q_common.append(qg)
    return (q_s_save, q_t_save, q_common)


def _qgram_counts(s, t, q=2):
    """Return a tuple for the two supplied strings, consisting of:
        (|q-grams in s|, |q-grams in t|, |q-grams in common|).
    These are the number of q-grams in each set.

    Arguments:
    s, t -- strings to extract q-grams from
    q -- the q-gram length (defaults to 2)
    """
    return tuple([len(elt) for elt in _qgram_lists(s, t, q)])
