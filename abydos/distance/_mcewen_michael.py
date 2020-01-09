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

"""abydos.distance._mcewen_michael.

McEwen & Michael correlation
"""

from ._token_distance import _TokenDistance

__all__ = ['McEwenMichael']


class McEwenMichael(_TokenDistance):
    r"""McEwen & Michael correlation.

    For two sets X and Y and a population N, the McEwen & Michael
    correlation :cite:`Michael:1920` is

        .. math::

            corr_{McEwenMichael}(X, Y) =
            \frac{4(|X \cap Y| \cdot |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|)}
            {(|X \cap Y| + |(N \setminus X) \setminus Y|)^2 +
            (|X \setminus Y| + |Y \setminus X|)^2}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{McEwenMichael} =
            \frac{4(ad-bc)}{(a+d)^2+(b+c)^2}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Michael instance.

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
        super(McEwenMichael, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return the McEwen & Michael correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Michael correlation

        Examples
        --------
        >>> cmp = McEwenMichael()
        >>> cmp.corr('cat', 'hat')
        0.010203544942933782
        >>> cmp.corr('Niall', 'Neil')
        0.010189175491654217
        >>> cmp.corr('aluminum', 'Catalan')
        0.0048084299262381456
        >>> cmp.corr('ATCG', 'TAGC')
        -0.00016689587032858459


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        num = a * d - b * c

        if num:
            return 4 * num / ((a + d) ** 2 + (b + c) ** 2)
        return 0.0

    def sim(self, src, tar):
        """Return the McEwen & Michael similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Michael similarity

        Examples
        --------
        >>> cmp = McEwenMichael()
        >>> cmp.sim('cat', 'hat')
        0.5051017724714669
        >>> cmp.sim('Niall', 'Neil')
        0.5050945877458272
        >>> cmp.sim('aluminum', 'Catalan')
        0.502404214963119
        >>> cmp.sim('ATCG', 'TAGC')
        0.4999165520648357


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
