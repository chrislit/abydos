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

"""abydos.tokenizer._wordpunct.

Regexp tokenizer
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import re

from ._tokenizer import _Tokenizer

__all__ = ['Regexp']


class Regexp(_Tokenizer):
    """A regexp tokenizer

    .. versionadded:: 0.4.0
    """

    def __init__(
        self, scaler=None, regexp=r'\w+', flags=0
    ):
        """Initialize tokenizer.

        Parameters
        ----------
        scaler : None, str, or function


        Examples
        --------

        .. versionadded:: 0.4.0

        """
        super(Regexp, self).__init__(scaler)

        # Save parameters
        self.regexp = re.compile(regexp, flags)

        self._string = ''
        self._ordered_list = []
        self._dict_dirty = True

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
        self._ordered_list = self.regexp.findall(self._string)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
