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

"""abydos.distance._warrens_i.

Warrens I correlation
"""

from ._token_distance import _TokenDistance

__all__ = ['WarrensI']


class WarrensI(_TokenDistance):
    r"""Warrens I correlation.

    For two sets X and Y, Warrens I correlation :math:`S_{NS1}`
    :cite:`Warrens:2008` is

        .. math::

            corr_{WarrensI}(X, Y) =
            \frac{2|X \cap Y| - |X \setminus Y| - |Y \setminus X|}
            {2|X \cap Y| + |X \setminus Y| + |Y \setminus X|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{WarrensI} =
            \frac{2a-b-c}{2a+b+c}

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize WarrensI instance.

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
        super(WarrensI, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )

    def corr(self, src, tar):
        """Return the Warrens I correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Warrens I correlation

        Examples
        --------
        >>> cmp = WarrensI()
        >>> cmp.corr('cat', 'hat')
        0.0
        >>> cmp.corr('Niall', 'Neil')
        -0.2727272727272727
        >>> cmp.corr('aluminum', 'Catalan')
        -0.7647058823529411
        >>> cmp.corr('ATCG', 'TAGC')
        -1.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()

        return (2 * a - b - c) / (2 * a + b + c)

    def sim(self, src, tar):
        """Return the Warrens I similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Warrens I similarity

        Examples
        --------
        >>> cmp = WarrensI()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.36363636363636365
        >>> cmp.sim('aluminum', 'Catalan')
        0.11764705882352944
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
