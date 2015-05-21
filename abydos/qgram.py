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

"""abydos.qgram

The qgram module defines the QGrams multi-set class
"""

from __future__ import unicode_literals
from __future__ import division
from ._compat import _range
from collections import Counter


# pylint: disable=abstract-method
class QGrams(Counter):
    """A q-gram class, which functions like a bag/multiset

    A q-gram is here defined as all sequences of q characters. Q-grams are also
    known as k-grams and n-grams, but the term n-gram more typically refers to
    sequences of whitespace-delimited words in a string, where q-gram refers
    to sequences of characters in a word or string.
    """
    term = ''
    term_ss = ''
    ordered_list = []

    def __init__(self, term, qval=2, start_stop='$#'):
        """Qgrams initializer

        :param str word: a string to extract q-grams from
        :param int qval: the q-gram length (defaults to 2)
        :param str start_stop: a string of length >= 0 indicating start & stop
            symbols.
            If the string is '', q-grams will be calculated without start &
            stop symbols appended to each end.
            Otherwise, the first character of start_stop will pad the beginning
            of the string and the last character of start_stop will pad the end
            of the string before q-grams are calculated. (In the case that
            start_stop is only 1 character long, the same symbol will be used
            for both.)
        """
        self.term = term
        if len(term) < qval or qval < 1:
            return
        if start_stop and qval > 1:
            term = start_stop[0]*(qval-1) + term + start_stop[-1]*(qval-1)
        self.term_ss = term

        self.ordered_list = [term[i:i+qval] for i in
                             _range(len(term)-(qval-1))]
        super(QGrams, self).__init__(self.ordered_list)

    def count(self):
        """q-grams count

        :returns: the total count of q-grams in a QGrams object
        :rtype: int
        """
        return sum(self.values())
