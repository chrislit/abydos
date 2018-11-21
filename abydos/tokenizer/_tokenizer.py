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

from collections import Counter


class _Tokenizer(Counter):
    """Abstract _Tokenizer class.

    .. versionadded:: 0.4.0
    """

    def __init__(self, bag_mode=True, *args, **kwargs):
        """Initialize Tokenizer.

        Args
        ----
        bag_mode : str
            Set to True to tokenize as bags/multisets or to False to tokenize
            as sets

        .. versionadded:: 0.4.0

        """
        self._string = ''
        self._ordered_list = []
        self.bag_mode = bag_mode

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
        self._ordered_list = [string]

        super(_Tokenizer, self).__init__(self._ordered_list)

        return self

    def count(self):
        """Return token count.

        Returns
        -------
        int
            The total count of tokens

        Examples
        --------
        >>> tok = _Tokenizer().tokenize('term')
        >>> tok.count()
        1

        .. versionadded:: 0.4.0

        """
        return sum(self.values()) if self.bag_mode else self.count_unique()

    def count_unique(self):
        """Returns the number of unique elements.

        Returns
        -------
        int
            The number of unique tokens

        Examples
        --------
        >>> tok = _Tokenizer().tokenize('term')
        >>> tok.count_unique()
        1

        .. versionadded:: 0.4.0

        """
        return len(self.values())

    def get_tokens_dict(self):
        """Returns the tokens as a Counter object.

        Returns
        -------
        Counter
            The Counter of tokens

        Examples
        --------
        >>> tok = _Tokenizer().tokenize('term')
        >>> tok.get_tokens_dict()
        {'term': 1}

        .. versionadded:: 0.4.0

        """
        return dict(self) if self.bag_mode else {key: 1 for key in self.keys()}

    def get_tokens_set(self):
        """Returns the unique tokens as a set.

        Returns
        -------
        Counter
            The set of tokens

        Examples
        --------
        >>> tok = _Tokenizer().tokenize('term')
        >>> tok.get_tokens_set()
        {'term'}

        .. versionadded:: 0.4.0

        """
        return set(self.keys())

    def get_tokens_list(self):
        """Returns the tokens as an ordered list.

        Returns
        -------
        Counter
            The list of q-grams in the order they were added.

        Examples
        --------
        >>> tok = _Tokenizer().tokenize('term')
        >>> tok.get_tokens_set()
        ['term']

        .. versionadded:: 0.4.0

        """
        return self._ordered_list


if __name__ == '__main__':
    import doctest

    doctest.testmod()
