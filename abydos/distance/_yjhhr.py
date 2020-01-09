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

"""abydos.distance._yjhhr.

YJHHR distance
"""

from ._token_distance import _TokenDistance

__all__ = ['YJHHR']


class YJHHR(_TokenDistance):
    r"""YJHHR distance.

    For two sets X and Y and a parameter p, YJHHR distance
    :cite:`Yang:2016` is

        .. math::

            dist_{YJHHR_p}(X, Y) =
            \sqrt[p]{|X \setminus Y|^p + |Y \setminus X|^p}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            dist_{YJHHR} =
            \sqrt[p]{b^p + c^p}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        pval=1,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize YJHHR instance.

        Parameters
        ----------
        pval : int
            The :math:`p`-value of the :math:`L^p`-space
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
        super(YJHHR, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )
        self.set_params(pval=pval)

    def dist_abs(self, src, tar):
        """Return the YJHHR distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            YJHHR distance

        Examples
        --------
        >>> cmp = YJHHR()
        >>> cmp.dist_abs('cat', 'hat')
        4.0
        >>> cmp.dist_abs('Niall', 'Neil')
        7.0
        >>> cmp.dist_abs('aluminum', 'Catalan')
        15.0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        10.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0

        self._tokenize(src, tar)

        b = self._src_only_card() ** self.params['pval']
        c = self._tar_only_card() ** self.params['pval']

        return float(round((b + c) ** (1 / self.params['pval']), 14))

    def dist(self, src, tar):
        """Return the normalized YJHHR distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            normalized YJHHR distance

        Examples
        --------
        >>> cmp = YJHHR()
        >>> cmp.dist('cat', 'hat')
        0.6666666666666666
        >>> cmp.dist('Niall', 'Neil')
        0.7777777777777778
        >>> cmp.dist('aluminum', 'Catalan')
        0.9375
        >>> cmp.dist('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.0

        """
        distance = self.dist_abs(src, tar)
        union = self._union_card()
        if union == 0:
            return 0.0
        return distance / union


if __name__ == '__main__':
    import doctest

    doctest.testmod()
