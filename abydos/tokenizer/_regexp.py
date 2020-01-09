# Copyright 2018-2020 by Christopher C. Little.
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

"""abydos.tokenizer._wordpunct.

Regexp tokenizer
"""

import re

from ._tokenizer import _Tokenizer

__all__ = ['RegexpTokenizer']


class RegexpTokenizer(_Tokenizer):
    """A regexp tokenizer.

    .. versionadded:: 0.4.0
    """

    def __init__(self, scaler=None, regexp=r'\w+', flags=0):
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
        super(RegexpTokenizer, self).__init__(scaler)

        # Save parameters
        self._regexp = re.compile(regexp, flags)

        self._string = ''
        self._ordered_tokens = []

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
        >>> RegexpTokenizer(regexp=r'[^-]+').tokenize('AA-CT-AG-AA-CD')
        RegexpTokenizer({'AA': 2, 'CT': 1, 'AG': 1, 'CD': 1})

        .. versionadded:: 0.4.0

        """
        self._string = string
        self._ordered_tokens = self._regexp.findall(self._string)
        super(RegexpTokenizer, self).tokenize()
        return self


if __name__ == '__main__':
    import doctest

    doctest.testmod()
