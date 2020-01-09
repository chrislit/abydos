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

"""abydos.distance._pearson_phi.

Pearson's Phi correlation
"""

from ._token_distance import _TokenDistance

__all__ = ['PearsonPhi']


class PearsonPhi(_TokenDistance):
    r"""Pearson's Phi correlation.

    For two sets X and Y and a population N, the Pearson's :math:`\phi`
    correlation :cite:`Pearson:1900,Pearson:1913,Guilford:1956` is

        .. math::

            corr_{PearsonPhi}(X, Y) =
            \frac{|X \cap Y| \cdot |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|}
            {\sqrt{|X| \cdot |Y| \cdot |N \setminus X| \cdot |N \setminus Y|}}

    This is also Pearson & Heron I similarity.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{PearsonPhi} =
            \frac{ad-bc}
            {\sqrt{(a+b)(a+c)(b+d)(c+d)}}

    Notes
    -----
    In terms of a confusion matrix, this is equivalent to the Matthews
    correlation coefficient :py:meth:`ConfusionTable.mcc`.

    .. versionadded:: 0.4.0

    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize PearsonPhi instance.

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
        super(PearsonPhi, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return Pearson's Phi correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Pearson's Phi correlation

        Examples
        --------
        >>> cmp = PearsonPhi()
        >>> cmp.corr('cat', 'hat')
        0.49743589743589745
        >>> cmp.corr('Niall', 'Neil')
        0.36069255713421955
        >>> cmp.corr('aluminum', 'Catalan')
        0.10821361655002706
        >>> cmp.corr('ATCG', 'TAGC')
        -0.006418485237483954


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        if src == tar:
            return 1.0

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        ab = self._src_card()
        ac = self._tar_card()

        num = a * d - b * c
        if num:
            return num / (ab * ac * (b + d) * (c + d)) ** 0.5
        return 0.0

    def sim(self, src, tar):
        """Return the normalized Pearson's Phi similarity of two strings.

        This is normalized to [0, 1] by adding 1 and dividing by 2.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Pearson's Phi similarity

        Examples
        --------
        >>> cmp = PearsonPhi()
        >>> cmp.sim('cat', 'hat')
        0.7487179487179487
        >>> cmp.sim('Niall', 'Neil')
        0.6803462785671097
        >>> cmp.sim('aluminum', 'Catalan')
        0.5541068082750136
        >>> cmp.sim('ATCG', 'TAGC')
        0.496790757381258


        .. versionadded:: 0.4.0

        """
        return (self.corr(src, tar) + 1.0) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
