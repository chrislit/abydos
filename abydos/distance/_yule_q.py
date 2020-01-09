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

"""abydos.distance._yule_q.

Yule's Q correlation
"""

from ._token_distance import _TokenDistance

__all__ = ['YuleQ']


class YuleQ(_TokenDistance):
    r"""Yule's Q correlation.

    For two sets X and Y and a population N, Yule's Q correlation
    :cite:`Yule:1912` is

        .. math::

            corr_{Yule_Q}(X, Y) =
            \frac{|X \cap Y| \cdot |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|}
            {|X \cap Y| \cdot |(N \setminus X) \setminus Y| +
            |X \setminus Y| \cdot |Y \setminus X|}

    Yule himself terms this the coefficient of association.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{Yule_Q} =
            \frac{ad-bc}{ad+bc}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize YuleQ instance.

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
        super(YuleQ, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return Yule's Q correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Yule's Q correlation

        Examples
        --------
        >>> cmp = YuleQ()
        >>> cmp.corr('cat', 'hat')
        0.9948717948717949
        >>> cmp.corr('Niall', 'Neil')
        0.9846350832266325
        >>> cmp.corr('aluminum', 'Catalan')
        0.8642424242424243
        >>> cmp.corr('ATCG', 'TAGC')
        -1.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        admbc = a * d - b * c
        if admbc:
            return admbc / (a * d + b * c)
        return 0.0

    def sim(self, src, tar):
        """Return Yule's Q similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Yule's Q similarity

        Examples
        --------
        >>> cmp = YuleQ()
        >>> cmp.sim('cat', 'hat')
        0.9974358974358974
        >>> cmp.sim('Niall', 'Neil')
        0.9923175416133163
        >>> cmp.sim('aluminum', 'Catalan')
        0.9321212121212121
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
