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

"""abydos.distance._raup_crick.

Raup-Crick similarity
"""

from math import factorial

from ._token_distance import _TokenDistance

__all__ = ['RaupCrick']


class RaupCrick(_TokenDistance):
    r"""Raup-Crick similarity.

    For two sets X and Y and a population N, Raup-Crick similarity
    :cite:`Raup:1979` is:

    .. math:

        sim_{Raup-Crick}(X, Y) = \sum_{i=0}^{|X \cap Y|}
        \frac{|X|! |Y|! (|N| - |X|)!
        (|N|- |Y|)!}{|N|! |X \cap Y|! (|X| - i)!
        (|Y| - i)! (|N| - |X| - |Y| + i)!}

    Notes
    -----
    Observe that Raup-Crick similarity is related to Henderson-Heron similarity
    in that the former is the sum of all Henderson-Heron similarities for an
    intersection size ranging from 0 to the true intersection size.

    .. versionadded:: 0.4.1
    """

    def __init__(self, **kwargs):
        """Initialize RaupCrick instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.1

        """
        super(RaupCrick, self).__init__(**kwargs)

    def sim(self, src, tar):
        """Return the Raup-Crick similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Raup-Crick similarity

        Examples
        --------
        >>> cmp = RaupCrick()
        >>> cmp.sim('cat', 'hat')
        0.9999998002120004
        >>> cmp.sim('Niall', 'Neil')
        0.9999975146378747
        >>> cmp.sim('aluminum', 'Catalan')
        0.9968397599851411
        >>> cmp.sim('ATCG', 'TAGC')
        0.9684367974410505


        .. versionadded:: 0.4.1

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        ab = self._src_card()
        ac = self._tar_card()
        n = self._population_unique_card()

        def _henderson_heron(ab, ac, a, n):
            return (
                factorial(ab)
                * factorial(ac)
                * factorial(n - ab)
                * factorial(n - ac)
                / (
                    factorial(n)
                    * factorial(a)
                    * factorial(ab - a)
                    * factorial(ac - a)
                    * factorial((n - ac - ab + a))
                )
            )

        return sum(_henderson_heron(ab, ac, i, n) for i in range(0, a + 1))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
