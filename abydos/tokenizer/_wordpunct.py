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

Wordpunct tokenizer (analogous to NLTK's workpunct tokenizer)
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._regexp import RegexpTokenizer

__all__ = ['WordpunctTokenizer']


class WordpunctTokenizer(RegexpTokenizer):
    """A wordpunct tokenizer.

    .. versionadded:: 0.4.0
    """

    def __init__(self, scaler=None, flags=0):
        """Initialize tokenizer.

        Parameters
        ----------
        scaler : None, str, or function
            A scaling function for the Counter:

                None : no scaling
                'set' : All non-zero values are set to 1.
                a callable function : The function is applied to each value
                    in the Counter. Some useful functions include math.exp,
                    math.log1p, math.sqrt, and indexes into interesting integer
                    sequences such as the Fibonacci sequence.

        .. versionadded:: 0.4.0

        """
        super(WordpunctTokenizer, self).__init__(
            scaler, regexp=r'\w+|[^\w\s]+', flags=flags
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()