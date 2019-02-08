# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.distance._positional_q_gram_overlap.

Positional Q-Gram Overlap distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._distance import _Distance

__all__ = ['PositionalQGramOverlap']


class PositionalQGramOverlap(_Distance):
    r"""Positional Q-Gram Overlap distance.

    Positional Q-Gram Overlap distance :cite:`CITATION`

    .. versionadded:: 0.4.0
    """

    def __init__(self, **kwargs):
        """Initialize PositionalQGramOverlap instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(PositionalQGramOverlap, self).__init__(**kwargs)

    def dist(self, src, tar):
        """Return the Positional Q-Gram Overlap distance of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Positional Q-Gram Overlap distance

        Examples
        --------
        >>> cmp = PositionalQGramOverlap()
        >>> cmp.dist('cat', 'hat')
        0.0
        >>> cmp.dist('Niall', 'Neil')
        0.0
        >>> cmp.dist('aluminum', 'Catalan')
        0.0
        >>> cmp.dist('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """

        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
