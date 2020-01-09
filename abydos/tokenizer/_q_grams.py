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

"""abydos.tokenizer._q_grams.

QGrams multi-set class
"""

from collections import Iterable

from ._tokenizer import _Tokenizer

__all__ = ['QGrams']


class QGrams(_Tokenizer):
    """A q-gram class, which functions like a bag/multiset.

    A q-gram is here defined as all sequences of q characters. Q-grams are also
    known as k-grams and n-grams, but the term n-gram more typically refers to
    sequences of whitespace-delimited words in a string, where q-gram refers
    to sequences of characters in a word or string.

    .. versionadded:: 0.1.0
    """

    def __init__(self, qval=2, start_stop='$#', skip=0, scaler=None):
        """Initialize QGrams.

        Parameters
        ----------
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
        scaler : None, str, or function
            A scaling function for the Counter:

                - None : no scaling
                - 'set' : All non-zero values are set to 1.
                - 'length' : Each token has weight equal to its length.
                - 'length-log' : Each token has weight equal to the log of its
                   length + 1.
                - 'length-exp' : Each token has weight equal to e raised to its
                   length.
                - a callable function : The function is applied to each value
                  in the Counter. Some useful functions include math.exp,
                  math.log1p, math.sqrt, and indexes into interesting integer
                  sequences such as the Fibonacci sequence.

        Raises
        ------
        ValueError
            Use WhitespaceTokenizer instead of qval=0.

        Examples
        --------
        >>> qg = QGrams().tokenize('AATTATAT')
        >>> qg
        QGrams({'AT': 3, 'TA': 2, '$A': 1, 'AA': 1, 'TT': 1, 'T#': 1})

        >>> qg = QGrams(qval=1, start_stop='').tokenize('AATTATAT')
        >>> qg
        QGrams({'A': 4, 'T': 4})

        >>> qg = QGrams(qval=3, start_stop='').tokenize('AATTATAT')
        >>> qg
        QGrams({'TAT': 2, 'AAT': 1, 'ATT': 1, 'TTA': 1, 'ATA': 1})

        >>> QGrams(qval=2, start_stop='$#').tokenize('interning')
        QGrams({'in': 2, '$i': 1, 'nt': 1, 'te': 1, 'er': 1, 'rn': 1,
        'ni': 1, 'ng': 1, 'g#': 1})

        >>> QGrams(start_stop='', skip=1).tokenize('AACTAGAAC')
        QGrams({'AC': 2, 'AT': 1, 'CA': 1, 'TG': 1, 'AA': 1, 'GA': 1, 'A': 1})

        >>> QGrams(start_stop='', skip=[0, 1]).tokenize('AACTAGAAC')
        QGrams({'AC': 4, 'AA': 3, 'GA': 2, 'CT': 1, 'TA': 1, 'AG': 1,
        'AT': 1, 'CA': 1, 'TG': 1, 'A': 1})

        >>> QGrams(qval=range(3), skip=[0, 1]).tokenize('interdisciplinarian')
        QGrams({'i': 10, 'n': 7, 'r': 4, 'a': 4, 'in': 3, 't': 2, 'e': 2,
        'd': 2, 's': 2, 'c': 2, 'p': 2, 'l': 2, 'ri': 2, 'ia': 2, '$i': 1,
        'nt': 1, 'te': 1, 'er': 1, 'rd': 1, 'di': 1, 'is': 1, 'sc': 1, 'ci': 1,
        'ip': 1, 'pl': 1, 'li': 1, 'na': 1, 'ar': 1, 'an': 1, 'n#': 1, '$n': 1,
        'it': 1, 'ne': 1, 'tr': 1, 'ed': 1, 'ds': 1, 'ic': 1, 'si': 1, 'cp': 1,
        'il': 1, 'pi': 1, 'ln': 1, 'nr': 1, 'ai': 1, 'ra': 1, 'a#': 1})

        .. versionadded:: 0.1.0
        .. versionchanged:: 0.4.0
            Broke tokenization functions out into tokenize method

        """
        if qval == 0:
            raise ValueError('Use WhitespaceTokenizer instead of qval=0.')
        super(QGrams, self).__init__(scaler)

        # Save parameters
        self.qval = qval
        self.start_stop = start_stop
        if qval == 1:
            self.start_stop = ''
        self.skip = skip

        self._string_ss = self._string

    def tokenize(self, string):
        """Tokenize the term and store it.

        The tokenized term is stored as an ordered list and as a Counter
        object.

        Parameters
        ----------
        string : str
            The string to tokenize


        .. versionadded:: 0.4.0

        """
        self._string = string
        self._ordered_tokens = []

        if not isinstance(self.qval, Iterable):
            self.qval = (self.qval,)
        if not isinstance(self.skip, Iterable):
            self.skip = (self.skip,)

        if string:
            for qval_i in self.qval:
                for skip_i in self.skip:
                    if qval_i < 1:
                        continue

                    if self.start_stop:
                        string = (
                            self.start_stop[0] * (qval_i - 1)
                            + self._string
                            + self.start_stop[-1] * (qval_i - 1)
                        )
                    else:
                        string = self._string

                    if qval_i > 1 and len(string) < qval_i:
                        continue

                    # Having appended start & stop symbols (or not), save the
                    # result, but only for the longest valid qval_i
                    if len(string) > len(self._string_ss):
                        self._string_ss = string

                    skip_i += 1
                    self._ordered_tokens += [
                        string[i : i + (qval_i * skip_i) : skip_i]
                        for i in range(len(string) - (qval_i - 1))
                    ]

        super(QGrams, self).tokenize()
        return self


if __name__ == '__main__':
    import doctest

    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
