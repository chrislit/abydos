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

"""abydos.distance._warrens_iv.

Warrens IV similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['WarrensIV']


class WarrensIV(_TokenDistance):
    r"""Warrens IV similarity.

    For two sets X and Y and a population N, Warrens IV similarity
    :cite:`Warrens:2008` is

        .. math::

            sim_{WarrensIV}(X, Y) =
            \frac{4|X \cap Y| \cdot |(N \setminus X) \setminus Y|}
            {4|X \cap Y| \cdot |(N \setminus X) \setminus Y| +
            (|X \cap Y| + |(N \setminus X) \setminus Y|)
            (|X \setminus Y| + |Y \setminus X|)}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{WarrensIV} =
            \frac{4ad}{4ad + (a+d)(b+c)}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize WarrensIV instance.

        Parameters
        ----------
        alphabet : Counter, collection, int, or None
            This represents the alphabet of possible tokens.
            See :ref:`alphabet <alphabet>` description in
            :py:class:`_TokenDistance` for details.
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
        super(WarrensIV, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Warrens IV similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Warrens IV similarity

        Examples
        --------
        >>> cmp = WarrensIV()
        >>> cmp.sim('cat', 'hat')
        0.666095890410959
        >>> cmp.sim('Niall', 'Neil')
        0.5326918120113412
        >>> cmp.sim('aluminum', 'Catalan')
        0.21031040612607685
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        atd = a * d
        if atd:
            return (4 * atd) / (4 * atd + (a + d) * (b + c))
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
