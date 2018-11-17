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

"""abydos.distance._monge_elkan.

Monge-Elkan similarity & distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._distance import _Distance
from ._levenshtein import sim_levenshtein
from ..tokenizer import QGrams

__all__ = ['MongeElkan', 'dist_monge_elkan', 'sim_monge_elkan']


class MongeElkan(_Distance):
    """Monge-Elkan similarity.

    Monge-Elkan is defined in :cite:`Monge:1996`.

    Note: Monge-Elkan is NOT a symmetric similarity algorithm. Thus, the
    similarity of src to tar is not necessarily equal to the similarity of
    tar to src. If the symmetric argument is True, a symmetric value is
    calculated, at the cost of doubling the computation time (since
    :math:`sim_{Monge-Elkan}(src, tar)` and :math:`sim_{Monge-Elkan}(tar, src)`
    are both calculated and then averaged).
    """

    def sim(self, src, tar, sim_func=sim_levenshtein, symmetric=False):
        """Return the Monge-Elkan similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        sim_func : function
            The internal similarity metric to employ
        symmetric : bool
            Return a symmetric similarity measure

        Returns
        -------
        float
            Monge-Elkan similarity

        Examples
        --------
        >>> cmp = MongeElkan()
        >>> cmp.sim('cat', 'hat')
        0.75
        >>> round(cmp.sim('Niall', 'Neil'), 12)
        0.666666666667
        >>> round(cmp.sim('aluminum', 'Catalan'), 12)
        0.388888888889
        >>> cmp.sim('ATCG', 'TAGC')
        0.5

        """
        if src == tar:
            return 1.0

        q_src = sorted(QGrams(src).elements())
        q_tar = sorted(QGrams(tar).elements())

        if not q_src or not q_tar:
            return 0.0

        sum_of_maxes = 0
        for q_s in q_src:
            max_sim = float('-inf')
            for q_t in q_tar:
                max_sim = max(max_sim, sim_func(q_s, q_t))
            sum_of_maxes += max_sim
        sim_em = sum_of_maxes / len(q_src)

        if symmetric:
            sim_em = (sim_em + self.sim(tar, src, sim_func, False)) / 2

        return sim_em


def sim_monge_elkan(src, tar, sim_func=sim_levenshtein, symmetric=False):
    """Return the Monge-Elkan similarity of two strings.

    This is a wrapper for :py:meth:`MongeElkan.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    sim_func : function
        Rhe internal similarity metric to employ
    symmetric : bool
        Return a symmetric similarity measure

    Returns
    -------
    float
        Monge-Elkan similarity

    Examples
    --------
    >>> sim_monge_elkan('cat', 'hat')
    0.75
    >>> round(sim_monge_elkan('Niall', 'Neil'), 12)
    0.666666666667
    >>> round(sim_monge_elkan('aluminum', 'Catalan'), 12)
    0.388888888889
    >>> sim_monge_elkan('ATCG', 'TAGC')
    0.5

    """
    return MongeElkan().sim(src, tar, sim_func, symmetric)


def dist_monge_elkan(src, tar, sim_func=sim_levenshtein, symmetric=False):
    """Return the Monge-Elkan distance between two strings.

    This is a wrapper for :py:meth:`MongeElkan.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    sim_func : function
        The internal similarity metric to employ
    symmetric : bool
        Return a symmetric similarity measure

    Returns
    -------
    float
        Monge-Elkan distance

    Examples
    --------
    >>> dist_monge_elkan('cat', 'hat')
    0.25
    >>> round(dist_monge_elkan('Niall', 'Neil'), 12)
    0.333333333333
    >>> round(dist_monge_elkan('aluminum', 'Catalan'), 12)
    0.611111111111
    >>> dist_monge_elkan('ATCG', 'TAGC')
    0.5

    """
    return MongeElkan().dist(src, tar, sim_func, symmetric)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
