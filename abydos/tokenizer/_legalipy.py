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

"""abydos.tokenizer._legalipy.

LegaliPy tokenizer class
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._tokenizer import _Tokenizer
try:
    from syllabipy.legalipy import getOnsets, LegaliPy
except ImportError:  # pragma: no cover
    # If the system lacks the SyllabiPy library, that's fine, but SyllabiPy
    # tokenization won't be supported.
    getOnsets = None
    LegaliPy = None


class LegaliPyTokenizer(_Tokenizer):
    """LegaliPy tokenizer.

    .. versionadded:: 0.4.0
    """

    def __init__(self, scaler=None):
        """Initialize Tokenizer.

        Args
        ----
        scaler : str
            Set to True to tokenize as bags/multisets or to False to tokenize
            as sets

        .. versionadded:: 0.4.0

        """
        if LegaliPy is None:
            raise TypeError('LegaliPy tokenizer requires installation of SyllabiPy package.')

        super(LegaliPyTokenizer, self).__init__(scaler)

        self._onsets = ['']

    def train_onsets(self, text, append=False):
        """Train the onsets on a text.

        Args
        ----
        text : str
            The text on which to train
        append : bool
            If true, the

        """
        if append:
            self._onsets = list(set(self._onsets + getOnsets(text)))
        else:
            self._onsets = getOnsets(text)

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
        self._dict_dirty = True  # Dirty bit (tag) for internal Counter

        self._ordered_list = LegaliPy(string, self._onsets)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
