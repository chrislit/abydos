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

"""abydos.tokenizer._whitespace.

Whitespace tokenizer
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import re

from ._regexp import Regexp
from ._tokenizer import _Tokenizer

__all__ = ['Regexp']


class Whitespace(Regexp):
    """A whitespace tokenizer

    .. versionadded:: 0.4.0
    """

    def __init__(
        self, scaler=None, flags=0
    ):
        """Initialize tokenizer.

        Parameters
        ----------
        string : str
            A string to extract q-grams from
        scaler : None, str, or function


        Examples
        --------

        .. versionadded:: 0.4.0

        """
        super(Whitespace, self).__init__(scaler, regexp=r'\W+', flags=flags)

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
        self._ordered_list = self.regexp.split(self._string)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
