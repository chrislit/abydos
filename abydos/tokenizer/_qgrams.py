# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

"""abydos.tokenizer._q_grams.

QGrams multi-set class
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from collections import Counter, Iterable

from six.moves import range

__all__ = ['QGrams']


class QGrams(Counter):
    """A q-gram class, which functions like a bag/multiset.

    A q-gram is here defined as all sequences of q characters. Q-grams are also
    known as k-grams and n-grams, but the term n-gram more typically refers to
    sequences of whitespace-delimited words in a string, where q-gram refers
    to sequences of characters in a word or string.
    """

    def __init__(self, term, qval=2, start_stop='$#', skip=0):
        """Initialize QGrams.

        Parameters
        ----------
        term : str
            A string to extract q-grams from
        qval : int or Iterable
            The q-gram length (defaults to 2), can be an integer, range object,
            or list
        start_stop : str
            A string of length >= 0 indicating start & stop symbols.
            If the string is '', q-grams will be calculated without start &
            stop symbols appended to each end.
            Otherwise, the first character of start_stop will pad the
            beginning of the string and the last character of start_stop
            will pad the end of the string before q-grams are calculated.
            (In the case that start_stop is only 1 character long, the same
            symbol will be used for both.)
        skip : int or Iterable
            The number of characters to skip, can be an integer, range object,
            or list

        Examples
        --------
        >>> qg = QGrams('AATTATAT')
        >>> qg
        QGrams({'AT': 3, 'TA': 2, '$A': 1, 'AA': 1, 'TT': 1, 'T#': 1})

        >>> qg = QGrams('AATTATAT', qval=1, start_stop='')
        >>> qg
        QGrams({'A': 4, 'T': 4})

        >>> qg = QGrams('AATTATAT', qval=3, start_stop='')
        >>> qg
        QGrams({'TAT': 2, 'AAT': 1, 'ATT': 1, 'TTA': 1, 'ATA': 1})

        """
        # Save the term itself
        self._term = term
        self._term_ss = term
        self._ordered_list = []

        if not isinstance(qval, Iterable):
            qval = (qval,)
        if not isinstance(skip, Iterable):
            skip = (skip,)

        for qval_i in qval:
            for skip_i in skip:
                if len(self._term) < qval_i or qval_i < 1:
                    continue

                if start_stop and qval_i > 1:
                    term = (
                        start_stop[0] * (qval_i - 1)
                        + self._term
                        + start_stop[-1] * (qval_i - 1)
                    )
                else:
                    term = self._term

                # Having appended start & stop symbols (or not), save the
                # result, but only for the longest valid qval_i
                if len(term) > len(self._term_ss):
                    self._term_ss = term

                skip_i += 1
                self._ordered_list += [
                    term[i : i + (qval_i * skip_i) : skip_i]
                    for i in range(len(term) - (qval_i - 1))
                ]

        super(QGrams, self).__init__(self._ordered_list)

    def count(self):
        """Return q-grams count.

        Returns
        -------
        int
            The total count of q-grams in a QGrams object

        Examples
        --------
        >>> qg = QGrams('AATTATAT')
        >>> qg.count()
        9

        >>> qg = QGrams('AATTATAT', qval=1, start_stop='')
        >>> qg.count()
        8

        >>> qg = QGrams('AATTATAT', qval=3, start_stop='')
        >>> qg.count()
        6

        """
        return sum(self.values())


if __name__ == '__main__':
    import doctest

    doctest.testmod()
