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

"""abydos.tokenizer._tokenize.

_Tokenizer base class
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._tokenizer import _Tokenizer


class NLTKTokenizer(_Tokenizer):
    """NLTK tokenizer wrapper class.

    .. versionadded:: 0.4.0
    """

    def __init__(self, scaler=None, nltk_tokenizer=None):
        """Initialize Tokenizer.

        Args
        ----
        scaler : str
            Set to True to tokenize as bags/multisets or to False to tokenize
            as sets

        .. versionadded:: 0.4.0

        """
        self._string = ''
        self._ordered_list = []
        self.scaler = scaler
        if 'nltk.tokenize' in str(type(nltk_tokenizer)) and hasattr(nltk_tokenizer, 'tokenize'):
            self.nltk_tokenizer = nltk_tokenizer
        else:
            raise TypeError('nltk_tokenizer must be an initialized tokenizer from the NLTK package (e.g. TweetTokenizer()).')

        super(_Tokenizer, self).__init__()

    def tokenize(self, string):
        """Tokenize the term and store it.

        The tokenized term is stored as an ordered list and as a Counter
        object.

        Args
        ----
        string : str
            The string to tokenize

        .. versionadded:: 0.4.0

        """
        # Save the string itself
        self._string = string
        self._ordered_list = self.nltk_tokenizer(string)

        super(_Tokenizer, self).__init__(self._ordered_list)

        return self


if __name__ == '__main__':
    import doctest

    doctest.testmod()
