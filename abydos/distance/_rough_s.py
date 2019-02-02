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

"""abydos.distance._rough_s.

Rough-S similarity
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._distance import _Distance
from ..tokenizer import QSkipgrams
from ..util._ncr import _ncr

__all__ = ['RoughS']


class RoughS(_Distance):
    r"""Rough-S similarity.

    Rough-S similarity :cite:`Lin:2004`, operating on character-level skipgrams

    .. versionadded:: 0.4.0
    """

    def __init__(self, qval=2, **kwargs):
        """Initialize RoughS instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(RoughS, self).__init__(**kwargs)
        self._qval = qval
        self._tokenizer = QSkipgrams(qval=qval)

    def sim(self, src, tar, beta=8):
        """Return the Rough-S similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        beta : int or float
            A weighting factor to prejudice similarity towards src

        Returns
        -------
        float
            Rough-S similarity

        Examples
        --------
        >>> cmp = RoughS()
        >>> cmp.sim('cat', 'hat')
        0.0
        >>> cmp.sim('Niall', 'Neil')
        0.0
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        qsg_src = self._tokenizer.tokenize(src)
        qsg_tar = self._tokenizer.tokenize(tar)
        intersection = qsg_src & qsg_tar

        r_skip = intersection / _ncr(len(src), self._qval)
        p_skip = intersection / _ncr(len(tar), self._qval)
        beta_sq = beta * beta

        return (1 + beta_sq) * r_skip * p_skip / (r_skip + beta_sq * p_skip)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
