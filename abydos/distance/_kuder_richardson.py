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

"""abydos.distance._kuder_richardson.

Kuder & Richardson correlation
"""

from ._token_distance import _TokenDistance

__all__ = ['KuderRichardson']


class KuderRichardson(_TokenDistance):
    r"""Kuder & Richardson correlation.

    For two sets X and Y and a population N, Kuder & Richardson similarity
    :cite:`Kuder:1937,Cronbach:1951` is

        .. math::

            corr_{KuderRichardson}(X, Y) =
            \frac{4(|X \cap Y| \cdot |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|)}
            {|X| \cdot |N \setminus X| +
            |Y| \cdot |N \setminus Y| +
            2(|X \cap Y| \cdot |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|)}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{KuderRichardson} =
            \frac{4(ad-bc)}{(a+b)(c+d) + (a+c)(b+d) +2(ad-bc)}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize KuderRichardson instance.

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
        super(KuderRichardson, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return the Kuder & Richardson correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Kuder & Richardson correlation

        Examples
        --------
        >>> cmp = KuderRichardson()
        >>> cmp.corr('cat', 'hat')
        0.6643835616438356
        >>> cmp.corr('Niall', 'Neil')
        0.5285677463699631
        >>> cmp.corr('aluminum', 'Catalan')
        0.19499521400246136
        >>> cmp.corr('ATCG', 'TAGC')
        -0.012919896640826873


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        admbc = a * d - b * c
        denom = (a + b) * (c + d) + (a + c) * (b + d) + 2 * admbc

        if not admbc:
            return 0.0
        elif not denom:
            return float('-inf')
        else:
            return (4 * admbc) / denom

    def sim(self, src, tar):
        """Return the Kuder & Richardson similarity of two strings.

        Since Kuder & Richardson correlation is unbounded in the negative,
        this measure is first clamped to [-1.0, 1.0].

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Kuder & Richardson similarity

        Examples
        --------
        >>> cmp = KuderRichardson()
        >>> cmp.sim('cat', 'hat')
        0.8321917808219178
        >>> cmp.sim('Niall', 'Neil')
        0.7642838731849815
        >>> cmp.sim('aluminum', 'Catalan')
        0.5974976070012307
        >>> cmp.sim('ATCG', 'TAGC')
        0.4935400516795866


        .. versionadded:: 0.4.0

        """
        score = max(-1.0, self.corr(src, tar))
        return (1.0 + score) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
