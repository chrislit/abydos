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

    def __init__(self, scaler=None, *args, **kwargs):
        """Initialize Tokenizer.

        Args
        ----
        scaler : str
            Set to True to tokenize as bags/multisets or to False to tokenize
            as sets

        .. versionadded:: 0.4.0

        """
        super(_Tokenizer, self).__init__()

        self.scaler = scaler

        self._string = ''
        self._dict_dirty = True  # Dirty bit (tag) for internal Counter
        self._ordered_list = []

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
        self._string = string
        self._dict_dirty = True  # Dirty bit (tag) for internal Counter
        self._ordered_list = [self._string]

    def _counter_init(self):
        """Create the internal Counter from the ordered list, if needed.

        .. versionadded:: 0.4.0

        """
        if self._dict_dirty:
            super(_Tokenizer, self).__init__(self._ordered_list)
            self._dict_dirty = False

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
        self._counter_init()
        return sum(self.get_tokens_dict().values())

    def count_unique(self):
        """Return the number of unique elements.

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
        self._counter_init()
        return len(self.values())

    def get_tokens_dict(self):
        """Return the tokens as a Counter object.

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
        self._counter_init()
        if self.scaler is None:
            return dict(self)
        elif self.scaler == 'set':
            return {key: 1 for key in self.keys()}
        elif callable(self.scaler):
            return {key: self.scaler(val) for key, val in self.items()}
        raise ValueError('Unsupported scaler value.')

    def get_tokens_set(self):
        """Return the unique tokens as a set.

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
        self._counter_init()
        return set(self.keys())

    def get_tokens_list(self):
        """Return the tokens as an ordered list.

        Returns
        -------
        Counter
            The list of q-grams in the order they were added.

        Examples
        --------
        >>> tok = _Tokenizer().tokenize('term')
        >>> tok.get_tokens_list()
        ['term']

        .. versionadded:: 0.4.0

        """
        return self._ordered_list


if __name__ == '__main__':
    import doctest

    doctest.testmod()
