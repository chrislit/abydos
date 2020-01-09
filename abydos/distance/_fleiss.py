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

"""abydos.distance._fleiss.

Fleiss correlation
"""

from ._token_distance import _TokenDistance

__all__ = ['Fleiss']


class Fleiss(_TokenDistance):
    r"""Fleiss correlation.

    For two sets X and Y and a population N, Fleiss correlation
    :cite:`Fleiss:1975` is

        .. math::

            corr_{Fleiss}(X, Y) =
            \frac{(|X \cap Y| \cdot |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|) \cdot
            (|X| \cdot |N \setminus X| + |Y| \cdot |N \setminus Y|)}
            {2 \cdot |X| \cdot |N \setminus X| \cdot |Y| \cdot |N \setminus Y|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{Fleiss} =
            \frac{(ad-bc)((a+b)(c+d)+(a+c)(b+d))}{2(a+b)(c+d)(a+c)(b+d)}

    This is Fleiss' :math:`M(A_1)`, :math:`ad-bc` divided by the harmonic mean
    of the marginals :math:`p_1q_1 = (a+b)(c+d)` and
    :math:`p_2q_2 = (a+c)(b+d)`.

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Fleiss instance.

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
        super(Fleiss, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return the Fleiss correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Fleiss correlation

        Examples
        --------
        >>> cmp = Fleiss()
        >>> cmp.corr('cat', 'hat')
        0.49743589743589745
        >>> cmp.corr('Niall', 'Neil')
        0.3621712520061204
        >>> cmp.corr('aluminum', 'Catalan')
        0.10839724112919989
        >>> cmp.corr('ATCG', 'TAGC')
        -0.006418485237483954


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        num = (a * d - b * c) * ((a + b) * (c + d) + (a + c) * (b + d))

        if num == 0.0:
            return 0.0
        return num / (2.0 * (a + b) * (c + d) * (a + c) * (b + d))

    def sim(self, src, tar):
        """Return the Fleiss similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Fleiss similarity

        Examples
        --------
        >>> cmp = Fleiss()
        >>> cmp.sim('cat', 'hat')
        0.7487179487179487
        >>> cmp.sim('Niall', 'Neil')
        0.6810856260030602
        >>> cmp.sim('aluminum', 'Catalan')
        0.5541986205645999
        >>> cmp.sim('ATCG', 'TAGC')
        0.496790757381258


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
