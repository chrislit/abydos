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

from collections.abc import Iterable
from itertools import combinations
from typing import Callable, Iterable as TIterable, Optional, Union

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

    def __init__(
        self,
        qval: Union[int, TIterable[int]] = 2,
        start_stop: str = '$#',
        scaler: Optional[Union[str, Callable[[float], float]]] = None,
        ssk_lambda: Union[float, TIterable[float]] = 0.9,
    ) -> None:
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
        QSkipgrams({'$A': 3, '$T': 3, '$#': 1, 'AA': 3, 'AT': 7, 'A#': 3,
        'TT': 3, 'TA': 2, 'T#': 3})

        >>> QSkipgrams(qval=1, start_stop='').tokenize('AATTAT')
        QSkipgrams({'A': 3, 'T': 3})

        >>> QSkipgrams(qval=3, start_stop='').tokenize('AATTAT')
        QSkipgrams({'AAT': 5, 'AAA': 1, 'ATT': 6, 'ATA': 4, 'TTA': 1, 'TTT': 1,
        'TAT': 2})

        >>> QSkipgrams(start_stop='').tokenize('ABCD')
        QSkipgrams({'AB': 1, 'AC': 1, 'AD': 1, 'BC': 1, 'BD': 1, 'CD': 1})

        >>> QSkipgrams().tokenize('Colin')
        QSkipgrams({'$C': 1, '$o': 1, '$l': 1, '$i': 1, '$n': 1, '$#': 1,
        'Co': 1, 'Cl': 1, 'Ci': 1, 'Cn': 1, 'C#': 1, 'ol': 1, 'oi': 1, 'on': 1,
        'o#': 1, 'li': 1, 'ln': 1, 'l#': 1, 'in': 1, 'i#': 1, 'n#': 1})

        >>> QSkipgrams(qval=3).tokenize('AACTAGAAC')
        QSkipgrams({'$$A': 5, '$$C': 2, '$$T': 1, '$$G': 1, '$$#': 2,
        '$AA': 20, '$AC': 14, '$AT': 4, '$AG': 6, '$A#': 20, '$CT': 2,
        '$CA': 6, '$CG': 2, '$CC': 2, '$C#': 8, '$TA': 6, '$TG': 2, '$TC': 2,
        '$T#': 4, '$GA': 4, '$GC': 2, '$G#': 4, '$##': 2, 'AAC': 11, 'AAT': 1,
        'AAA': 10, 'AAG': 3, 'AA#': 20, 'ACT': 2, 'ACA': 6, 'ACG': 2, 'ACC': 2,
        'AC#': 14, 'ATA': 6, 'ATG': 2, 'ATC': 2, 'AT#': 4, 'AGA': 6, 'AGC': 3,
        'AG#': 6, 'A##': 5, 'CTA': 3, 'CTG': 1, 'CTC': 1, 'CT#': 2, 'CAG': 1,
        'CAA': 3, 'CAC': 3, 'CA#': 6, 'CGA': 2, 'CGC': 1, 'CG#': 2, 'CC#': 2,
        'C##': 2, 'TAG': 1, 'TAA': 3, 'TAC': 3, 'TA#': 6, 'TGA': 2, 'TGC': 1,
        'TG#': 2, 'TC#': 2, 'T##': 1, 'GAA': 1, 'GAC': 2, 'GA#': 4, 'GC#': 2,
        'G##': 1})

        QSkipgrams may also be used to produce weights in accordance with the
        substring kernel rules of :cite:`Lodhi:2002` by passing the scaler
        value ``'SSK'``:

        >>> QSkipgrams(scaler='SSK').tokenize('AACTAGAAC')
        QSkipgrams(, {'$A': 2.8883286990000006, '$C': 1.0047784401000002,
        '$T': 0.5904900000000001, '$G': 0.4782969000000001,
        '$#': 0.31381059609000006, 'AA': 6.170192010000001, 'AC': 4.486377699,
        'AT': 1.3851, 'AG': 1.931931, 'A#': 2.6526399291000002, 'CT': 0.81,
        'CA': 1.850931, 'CG': 0.6561, 'CC': 0.4782969000000001,
        'C#': 1.2404672100000003, 'TA': 2.05659, 'TG': 0.7290000000000001,
        'TC': 0.531441, 'T#': 0.4782969000000001, 'GA': 1.5390000000000001,
        'GC': 0.6561, 'G#': 0.5904900000000001})

        .. versionadded:: 0.4.0

        """
        super().__init__(scaler)

        # Save parameters
        self.qval = qval
        self.start_stop = start_stop
        if qval == 1:
            self.start_stop = ''

        self._string_ss = self._string
        if isinstance(ssk_lambda, float):
            self._lambda = (ssk_lambda,)  # type: TIterable[float]
        else:
            self._lambda = tuple(ssk_lambda)

    def tokenize(self, string: str) -> 'QSkipgrams':
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
            self._ordered_tokens += [''.join(lt[1] for lt in t) for t in combs]

            if self._scaler == 'SSK':
                self._ordered_weights += [
                    sum(
                        lt ** (t[-1][0] - t[0][0] + len(t) - 1)
                        for lt in self._lambda
                    )
                    for t in combs
                ]
            else:
                self._ordered_weights += [1] * len(combs)

        self._scale_and_counterize()
        return self


if __name__ == '__main__':
    import doctest

    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
