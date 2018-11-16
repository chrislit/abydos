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

"""abydos.distance._ncd_arith.

NCD using Arithmetic Coding
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._distance import _Distance
from ..compression import Arithmetic

__all__ = ['NCDarith', 'dist_ncd_arith', 'sim_ncd_arith']


class NCDarith(_Distance):
    """Normalized Compression Distance using arithmetic coding.

    Cf. https://en.wikipedia.org/wiki/Arithmetic_coding

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.
    """

    _coder = None

    def __init__(self):
        """Initialize the arithmetic coder object."""
        self._coder = Arithmetic()

    def dist(self, src, tar, probs=None):
        """Return the NCD between two strings using arithmetic coding.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        probs : dict
            A dictionary trained with :py:meth:`Arithmetic.train`

        Returns
        -------
        float
            Compression distance

        Examples
        --------
        >>> cmp = NCDarith()
        >>> cmp.dist('cat', 'hat')
        0.5454545454545454
        >>> cmp.dist('Niall', 'Neil')
        0.6875
        >>> cmp.dist('aluminum', 'Catalan')
        0.8275862068965517
        >>> cmp.dist('ATCG', 'TAGC')
        0.6923076923076923

        """
        if src == tar:
            return 0.0

        if probs is None:
            # lacking a reasonable dictionary, train on the strings themselves
            self._coder.train(src + tar)
        else:
            self._coder.set_probs(probs)

        src_comp = self._coder.encode(src)[1]
        tar_comp = self._coder.encode(tar)[1]
        concat_comp = self._coder.encode(src + tar)[1]
        concat_comp2 = self._coder.encode(tar + src)[1]

        return (
            min(concat_comp, concat_comp2) - min(src_comp, tar_comp)
        ) / max(src_comp, tar_comp)


def dist_ncd_arith(src, tar, probs=None):
    """Return the NCD between two strings using arithmetic coding.

    This is a wrapper for :py:meth:`NCDarith.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    probs : dict
        A dictionary trained with :py:meth:`Arithmetic.train`

    Returns
    -------
    float
        Compression distance

    Examples
    --------
    >>> dist_ncd_arith('cat', 'hat')
    0.5454545454545454
    >>> dist_ncd_arith('Niall', 'Neil')
    0.6875
    >>> dist_ncd_arith('aluminum', 'Catalan')
    0.8275862068965517
    >>> dist_ncd_arith('ATCG', 'TAGC')
    0.6923076923076923

    """
    return NCDarith().dist(src, tar, probs)


def sim_ncd_arith(src, tar, probs=None):
    """Return the NCD similarity between two strings using arithmetic coding.

    This is a wrapper for :py:meth:`NCDarith.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    probs : dict
        A dictionary trained with :py:meth:`Arithmetic.train`

    Returns
    -------
    float
        Compression similarity

    Examples
    --------
    >>> sim_ncd_arith('cat', 'hat')
    0.4545454545454546
    >>> sim_ncd_arith('Niall', 'Neil')
    0.3125
    >>> sim_ncd_arith('aluminum', 'Catalan')
    0.1724137931034483
    >>> sim_ncd_arith('ATCG', 'TAGC')
    0.3076923076923077

    """
    return NCDarith().sim(src, tar, probs)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
