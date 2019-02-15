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

"""abydos.distance._ncd_ppmd.

NCD using PPMd
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._distance import _Distance
from ..compression import PPMd


__all__ = ['NCDppmd']


class NCDppmd(_Distance):
    """Normalized Compression Distance using PPMd compression.

    Cf. https://en.wikipedia.org/wiki/Prediction_by_partial_matching

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    .. versionadded:: 0.4.0
    """

    def __init__(self, probs=None, **kwargs):
        """Initialize the arithmetic coder object.

        Parameters
        ----------
        probs : dict
            A dictionary trained with :py:meth:`Arithmetic.train`


        .. versionadded:: 0.4.0

        """
        super(NCDppmd, self).__init__(**kwargs)
        self._ppmd = PPMd()

    def dist(self, src, tar):
        """Return the NCD between two strings using PPMd compression.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Compression distance

        Examples
        --------
        >>> cmp = NCDppmd()
        >>> cmp.dist('cat', 'hat')
        0.08695652173913043
        >>> cmp.dist('Niall', 'Neil')
        0.16
        >>> cmp.dist('aluminum', 'Catalan')
        0.16
        >>> cmp.dist('ATCG', 'TAGC')
        0.08695652173913043


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0

        src = src.encode('utf-8')
        tar = tar.encode('utf-8')

        src_comp = self._ppmd.compress(src)
        tar_comp = self._ppmd.compress(tar)
        concat_comp = self._ppmd.compress(src + tar)
        concat_comp2 = self._ppmd.compress(tar + src)

        return (
            min(len(concat_comp), len(concat_comp2))
            - min(len(src_comp), len(tar_comp))
        ) / max(len(src_comp), len(tar_comp))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
