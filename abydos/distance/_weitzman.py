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

"""abydos.distance._weitzman.

Weitzman distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._token_distance import _TokenDistance

__all__ = ['Weitzman']


class Weitzman(_TokenDistance):
    r"""Weitzman distance.

    Weitzman distance :cite:`Weitzman:1970`

    .. versionadded:: 0.4.1
    """

    def __init__(self, **kwargs):
        """Initialize Weitzman instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.1

        """
        super(Weitzman, self).__init__(**kwargs)

    def dist(self, src, tar):
        """Return the Weitzman distance of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Weitzman distance

        Examples
        --------
        >>> cmp = Weitzman()
        >>> cmp.dist('cat', 'hat')
        0.0
        >>> cmp.dist('Niall', 'Neil')
        0.0
        >>> cmp.dist('aluminum', 'Catalan')
        0.0
        >>> cmp.dist('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.1

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = self._population_unique_card()

        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
