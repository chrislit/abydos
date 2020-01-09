# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.tokenizer._q_skipgrams.

Q-Skipgrams multi-set class
"""

from collections import Iterable
from itertools import combinations

from ._tokenizer import _Tokenizer

__all__ = ['QSkipgrams']


class QSkipgrams(_Tokenizer):
    """A q-skipgram class, which functions like a bag/multiset.

    A q-gram is here defined as all sequences of q characters. Q-grams are also
    known as k-grams and n-grams, but the term n-gram more typically refers to
    sequences of whitespace-delimited words in a string, where q-gram refers
    to sequences of characters in a word or string.

    .. versionadded:: 0.4.0
    """

    def __init__(self, qval=2, start_stop='$#', scaler=None, ssk_lambda=0.9):
        """Initialize QSkipgrams.

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
                - 'SSK' : Applies weighting according to the substring kernel
                  rules of :cite:`Lodhi:2002`.
        ssk_lambda : float or Iterable
            A value in the range (0.0, 1.0) used for discouting gaps between
            characters according to the method described in :cite:`Lodhi:2002`.
            To supply multiple values of lambda, provide an Iterable of numeric
            values, such as (0.5, 0.05) or np.arange(0.05, 0.5, 0.05)

        Raises
        ------
        ValueError
            Use WhitespaceTokenizer instead of qval=0.

        Examples
        --------
        >>> QSkipgrams().tokenize('AATTAT')
        QSkipgrams({'AT': 7, '$A': 3, '$T': 3, 'AA': 3, 'A#': 3, 'TT': 3,
        'T#': 3, 'TA': 2, '$#': 1})

        >>> QSkipgrams(qval=1, start_stop='').tokenize('AATTAT')
        QSkipgrams({'A': 3, 'T': 3})

        >>> QSkipgrams(qval=3, start_stop='').tokenize('AATTAT')
        QSkipgrams({'ATT': 6, 'AAT': 5, 'ATA': 4, 'TAT': 2, 'AAA': 1,
        'TTA': 1, 'TTT': 1})

        >>> QSkipgrams(start_stop='').tokenize('ABCD')
        QSkipgrams({'AB': 1, 'AC': 1, 'AD': 1, 'BC': 1, 'BD': 1, 'CD': 1})

        >>> QSkipgrams().tokenize('Colin')
        QSkipgrams({'$C': 1, '$o': 1, '$l': 1, '$i': 1, '$n': 1, '$#': 1,
        'Co': 1, 'Cl': 1, 'Ci': 1, 'Cn': 1, 'C#': 1, 'ol': 1, 'oi': 1, 'on': 1,
        'o#': 1, 'li': 1, 'ln': 1, 'l#': 1, 'in': 1, 'i#': 1, 'n#': 1})

        >>> QSkipgrams(qval=3).tokenize('AACTAGAAC')
        QSkipgrams({'$AA': 20, '$A#': 20, 'AA#': 20, '$AC': 14, 'AC#': 14,
        'AAC': 11, 'AAA': 10, '$C#': 8, '$AG': 6, '$CA': 6, '$TA': 6, 'ACA': 6,
        'ATA': 6, 'AGA': 6, 'AG#': 6, 'CA#': 6, 'TA#': 6, '$$A': 5, 'A##': 5,
        '$AT': 4, '$T#': 4, '$GA': 4, '$G#': 4, 'AT#': 4, 'GA#': 4, 'AAG': 3,
        'AGC': 3, 'CTA': 3, 'CAA': 3, 'CAC': 3, 'TAA': 3, 'TAC': 3, '$$C': 2,
        '$$#': 2, '$CT': 2, '$CG': 2, '$CC': 2, '$TG': 2, '$TC': 2, '$GC': 2,
        '$##': 2, 'ACT': 2, 'ACG': 2, 'ACC': 2, 'ATG': 2, 'ATC': 2, 'CT#': 2,
        'CGA': 2, 'CG#': 2, 'CC#': 2, 'C##': 2, 'TGA': 2, 'TG#': 2, 'TC#': 2,
        'GAC': 2, 'GC#': 2, '$$T': 1, '$$G': 1, 'AAT': 1, 'CTG': 1, 'CTC': 1,
        'CAG': 1, 'CGC': 1, 'TAG': 1, 'TGC': 1, 'T##': 1, 'GAA': 1, 'G##': 1})

        QSkipgrams may also be used to produce weights in accordance with the
        substring kernel rules of :cite:`Lodhi:2002` by passing the scaler
        value ``'SSK'``:

        >>> QSkipgrams(scaler='SSK').tokenize('AACTAGAAC')
        QSkipgrams({'AA': 6.170192010000001, 'AC': 4.486377699,
        '$A': 2.8883286990000006, 'A#': 2.6526399291000002, 'TA': 2.05659,
        'AG': 1.931931, 'CA': 1.850931, 'GA': 1.5390000000000001, 'AT': 1.3851,
        'C#': 1.2404672100000003, '$C': 1.0047784401000002, 'CT': 0.81,
        'TG': 0.7290000000000001, 'CG': 0.6561, 'GC': 0.6561,
        '$T': 0.5904900000000001, 'G#': 0.5904900000000001, 'TC': 0.531441,
        '$G': 0.4782969000000001, 'CC': 0.4782969000000001,
        'T#': 0.4782969000000001, '$#': 0.31381059609000006})

        .. versionadded:: 0.4.0

        """
        super(QSkipgrams, self).__init__(scaler)

        # Save parameters
        self.qval = qval
        self.start_stop = start_stop
        if qval == 1:
            self.start_stop = ''

        self._string_ss = self._string
        if isinstance(ssk_lambda, float):
            self._lambda = (ssk_lambda,)
        else:
            self._lambda = tuple(ssk_lambda)

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
        self._ordered_weights = []

        if not isinstance(self.qval, Iterable):
            self.qval = (self.qval,)

        for qval_i in self.qval:
            if qval_i < 1:
                continue

            if self.start_stop and self._string:
                string = (
                    self.start_stop[0] * (qval_i - 1)
                    + self._string
                    + self.start_stop[-1] * (qval_i - 1)
                )
            else:
                string = self._string

            if len(string) < qval_i:
                continue

            # Having appended start & stop symbols (or not), save the
            # result, but only for the longest valid qval_i
            if len(string) > len(self._string_ss):
                self._string_ss = string

            combs = list(combinations(enumerate(string), qval_i))
            self._ordered_tokens += [''.join(l[1] for l in t) for t in combs]

            if self._scaler == 'SSK':
                self._ordered_weights += [
                    sum(
                        l ** (t[-1][0] - t[0][0] + len(t) - 1)
                        for l in self._lambda
                    )
                    for t in combs
                ]
            else:
                self._ordered_weights += [1] * len(combs)

        super(QSkipgrams, self).tokenize()
        return self


if __name__ == '__main__':
    import doctest

    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
