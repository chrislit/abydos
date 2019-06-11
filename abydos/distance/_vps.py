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

"""abydos.distance._vps

Victorian Panel Study (VPS)
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._distance import _Distance

__all__ = ['VPS']


class VPS(_Distance):
    """Victorian Panel Study distance.



    .. versionadded:: 0.4.1
    """

    def dist(self, src, tar):
        """Return the Victorian Panel Study distance of two words.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The VPS distance

        Examples
        --------
        >>> cmp = VPS()
        >>> round(cmp.dist('cat', 'hat'), 12)
        1.0
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        1.0
        >>> cmp.dist('aluminum', 'Catalan')
        1.0
        >>> cmp.dist('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.1

        """
        pass


if __name__ == '__main__':
    import doctest

    doctest.testmod()
