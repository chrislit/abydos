# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.distance._lig3.

LIG3 similarity
"""

from ._distance import _Distance
from ._levenshtein import Levenshtein

__all__ = ['LIG3']


class LIG3(_Distance):
    r"""LIG3 similarity.

    :cite:`Snae:2002` proposes three Levenshtein-ISG-Guth hybrid similarity
    measures: LIG1, LIG2, and LIG3. Of these, LIG1 is identical to ISG and LIG2
    is identical to normalized Levenshtein similarity. Only LIG3 is a novel
    measure, defined as:

        .. math::

            sim_{LIG3}(X, Y) = \frac{2I}{2I+C}

    Here, I is the number of exact matches between the two words, truncated to
    the length of the shorter word, and C is the Levenshtein distance between
    the two words.

    .. versionadded:: 0.4.1
    """

    _lev = Levenshtein()

    def sim(self, src, tar):
        """Return the LIG3 similarity of two words.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The LIG3 similarity

        Examples
        --------
        >>> cmp = LIG3()
        >>> cmp.sim('cat', 'hat')
        0.8
        >>> cmp.sim('Niall', 'Neil')
        0.5714285714285714
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.1

        """
        if src == tar:
            return 1.0

        matches = 2 * sum(
            src[pos] == tar[pos] for pos in range(min(len(src), len(tar)))
        )
        cost = self._lev.dist_abs(src, tar)

        return matches / (matches + cost)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
