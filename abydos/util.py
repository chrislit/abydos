# -*- coding: utf-8 -*-
"""abydos.util

The util module defines various utility functions for other modules within
Abydos, including:
    q-gram functions


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
from ._compat import _range


def qgrams(src, qval=2, start_stop='$#'):
    """Returns a list of all q-grams of a string.

    Arguments:
    src -- a string to extract q-grams from
    qval -- the q-gram length (defaults to 2)
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
    if len(src) < qval:
        return []
    if start_stop and qval > 1:
        src = start_stop[0]*(qval-1) + src + start_stop[-1]*(qval-1)
    return [src[i:i+qval] for i in _range(len(src)-(qval-1))]


def _qgram_lists(src, tar, qval=2, start_stop='$#'):
    """Return a tuple for the two supplied strings, consisting of:
        (q-grams in src, q-grams in tar, q-grams in common).

    Arguments:
    src, tar -- strings to extract q-grams from
    qval -- the q-gram length (defaults to 2)
    start_stop -- a string of length >= 0 indicating start & stop symbols
        If the string is '', q-grams will be calculated without start & stop
        symbols appended to each end.
        Otherwise, the first character of start_stop will pad the beginning of
        the string and the last character of start_stop will pad the end of the
        string before q-grams are calculated. (In the case that start_stop is
        only 1 character long, the same symbol will be used for both.)
    """
    q_src = qgrams(src, qval, start_stop)
    q_tar = qgrams(tar, qval, start_stop)
    q_common = []
    q_tar_save = list(q_tar)

    for qgram in q_src:
        if qgram in q_tar:
            q_tar.remove(qgram)
            q_common.append(qgram)
    return (q_src, q_tar_save, q_common)


def _qgram_counts(src, tar, qval=2, start_stop='$#'):
    """Return a tuple for the two supplied strings, consisting of:
        (|q-grams in src|, |q-grams in tar|, |q-grams in common|).
    These are the number of q-grams in each set.

    Arguments:
    src, tar -- strings to extract q-grams from
    qval -- the q-gram length (defaults to 2)
    start_stop -- a string of length >= 0 indicating start & stop symbols
        If the string is '', q-grams will be calculated without start & stop
        symbols appended to each end.
        Otherwise, the first character of start_stop will pad the beginning of
        the string and the last character of start_stop will pad the end of the
        string before q-grams are calculated. (In the case that start_stop is
        only 1 character long, the same symbol will be used for both.)
    """
    return tuple([len(elt) for elt in _qgram_lists(src, tar, qval, start_stop)])
