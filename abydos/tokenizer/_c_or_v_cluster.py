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

"""abydos.tokenizer._c_or_v_cluster.

Consonant or vowel cluster tokenizer.

This tokenizer first performs wordpunct tokenization, so words are split into
separate units and non-letter characters are added as their own units.
Following this, words are further divided into strings of consonants only and
strings of vowels only.
"""

import re
import unicodedata

from ._tokenizer import _Tokenizer

__all__ = ['COrVClusterTokenizer']


class COrVClusterTokenizer(_Tokenizer):
    """A C- or V-cluster tokenizer.

    .. versionadded:: 0.4.0
    """

    def __init__(self, scaler=None, consonants=None, vowels=None):
        """Initialize tokenizer.

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
        super(COrVClusterTokenizer, self).__init__(scaler=scaler)
        if consonants:
            self._consonants = consonants
        else:
            self._consonants = set('bcdfghjklmnpqrstvwxzßBCDFGHJKLMNPQRSTVWXZ')
        if vowels:
            self._vowels = vowels
        else:
            self._vowels = set('aeiouyAEIOUY')
        self._regexp = re.compile(r'\w+|[^\w\s]+', flags=0)

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
        >>> COrVClusterTokenizer().tokenize('seven-twelfths')
        COrVClusterTokenizer({'e': 3, 's': 1, 'v': 1, 'n': 1, '-': 1,
        'tw': 1, 'lfths': 1})

        >>> COrVClusterTokenizer().tokenize('character')
        COrVClusterTokenizer({'a': 2, 'r': 2, 'ch': 1, 'ct': 1, 'e': 1})


        .. versionadded:: 0.4.0

        """
        self._string = string
        self._ordered_tokens = []
        token_list = self._regexp.findall(self._string)
        for token in token_list:
            if (
                token[0] not in self._consonants
                and token[0] not in self._vowels
            ):
                self._ordered_tokens.append(token)
            else:
                token = unicodedata.normalize('NFD', token)
                mode = 0  # 0 = starting mode, 1 = cons, 2 = vowels
                new_token = ''  # noqa: S105
                for char in token:
                    if char in self._consonants:
                        if mode == 2:
                            self._ordered_tokens.append(new_token)
                            new_token = char
                        else:
                            new_token += char
                        mode = 1
                    elif char in self._vowels:
                        if mode == 1:
                            self._ordered_tokens.append(new_token)
                            new_token = char
                        else:
                            new_token += char
                        mode = 2
                    else:  # This should cover combining marks, marks, etc.
                        new_token += char

                self._ordered_tokens.append(new_token)

        self._ordered_tokens = [
            unicodedata.normalize('NFC', token)
            for token in self._ordered_tokens
        ]
        super(COrVClusterTokenizer, self).tokenize()
        return self


if __name__ == '__main__':
    import doctest

    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
