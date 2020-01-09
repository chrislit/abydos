# Copyright 2018-2020 by Christopher C. Little.
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

"""abydos.distance._mountford.

Mountford similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['Mountford']


class Mountford(_TokenDistance):
    r"""Mountford similarity.

    For two sets X and Y, the Mountford similarity :cite:`Mountford:1962` is

        .. math::

            sim_{Mountford}(X, Y) =
            \frac{2|X \cap Y|}{2|X|\cdot|Y|-(|X|+|Y|)\cdot|X \cap Y|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{Mountford} =
            \frac{2a}{2(a+b)(a+c)-(2a+b+c)a}

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize Mountford instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        intersection_type : str
            Specifies the intersection type, and set type as a result:
            See :ref:`intersection_type <intersection_type>` description in
            :py:class:`_TokenDistance` for details.
        **kwargs
            Arbitrary keyword arguments

        Other Parameters
        ----------------
        qval : int
            The length of each q-gram. Using this parameter and tokenizer=None
            will cause the instance to use the QGram tokenizer with this
            q value.
        metric : _Distance
            A string distance measure class for use in the ``soft`` and
            ``fuzzy`` variants.
        threshold : float
            A threshold value, similarities above which are counted as
            members of the intersection for the ``fuzzy`` variant.


        .. versionadded:: 0.4.0

        """
        super(Mountford, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )

    def sim(self, src, tar):
        """Return the Mountford similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Mountford similarity

        Examples
        --------
        >>> cmp = Mountford()
        >>> cmp.sim('cat', 'hat')
        0.25
        >>> cmp.sim('Niall', 'Neil')
        0.10526315789473684
        >>> cmp.sim('aluminum', 'Catalan')
        0.015748031496062992
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()

        if not b:
            b = 1
        if not c:
            c = 1

        if a:
            return 2.0 * a / (c * (a + 2.0 * b) + a * b)
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
