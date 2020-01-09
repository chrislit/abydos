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

"""abydos.tokenizer._saps.

SAPS class
"""

from ._tokenizer import _Tokenizer


class SAPSTokenizer(_Tokenizer):
    """Syllable Alignment Pattern Searching tokenizer.

    This is the syllabifier described on p. 917 of :cite:`Ruibin:2005`.

    .. versionadded:: 0.4.0
    """

    def __init__(self, scaler=None):
        """Initialize Tokenizer.

        Parameters
        ----------
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


        .. versionadded:: 0.4.0

        """
        super(SAPSTokenizer, self).__init__(scaler)

    def tokenize(self, string):
        """Tokenize the term and store it.

        The tokenized term is stored as an ordered list and as a Counter
        object.

        Parameters
        ----------
        string : str
            The string to tokenize

        Examples
        --------
        >>> SAPSTokenizer().tokenize('seven-twelfths')
        SAPSTokenizer({'t': 2, 'se': 1, 'ven': 1, '-': 1, 'wel': 1, 'f': 1,
        'h': 1, 's': 1})

        >>> SAPSTokenizer().tokenize('character')
        SAPSTokenizer({'c': 1, 'ha': 1, 'rac': 1, 'ter': 1})


        .. versionadded:: 0.4.0

        """
        self._string = string

        self._ordered_tokens = []

        _vowels = set('aeiouyAEIOUY')

        words = self._string.split()
        for w in words:
            self._ordered_tokens = []
            i = 0
            while i < len(w):
                syll = w[i : i + 1]
                i += 1
                while w[i : i + 1] in _vowels:
                    syll += w[i : i + 1]
                    i += 1
                if syll[-1] in _vowels and (
                    (
                        len(w[i:]) > 1
                        and w[i : i + 1] not in _vowels
                        and w[i + 1 : i + 2] not in _vowels
                    )
                    or (len(w[i:]) == 1 and w[i : i + 1] not in _vowels)
                ):
                    syll += w[i : i + 1]
                    i += 1
                self._ordered_tokens.append(syll)

        super(SAPSTokenizer, self).tokenize()
        return self


if __name__ == '__main__':
    import doctest

    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
