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

"""abydos.distance._gower_legendre.

Gower & Legendre similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['GowerLegendre']


class GowerLegendre(_TokenDistance):
    r"""Gower & Legendre similarity.

    For two sets X and Y and a population N, the Gower & Legendre similarity
    :cite:`Gower:1986` is

        .. math::

            sim_{GowerLegendre}(X, Y) =
            \frac{|X \cap Y| + |(N \setminus X) \setminus Y|}
            {|X \cap Y| + |(N \setminus X) \setminus Y| +
            \theta \cdot |X \triangle Y|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{GowerLegendre} =
            \frac{a+d}{a+\theta(b+c)+d}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        theta=0.5,
        **kwargs
    ):
        """Initialize GowerLegendre instance.

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
        theta : float
            The weight to place on the symmetric difference.
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
        self.theta = theta
        super(GowerLegendre, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Gower & Legendre similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Gower & Legendre similarity

        Examples
        --------
        >>> cmp = GowerLegendre()
        >>> cmp.sim('cat', 'hat')
        0.9974424552429667
        >>> cmp.sim('Niall', 'Neil')
        0.9955156950672646
        >>> cmp.sim('aluminum', 'Catalan')
        0.9903536977491961
        >>> cmp.sim('ATCG', 'TAGC')
        0.993581514762516


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        apd = self._intersection_card() + self._total_complement_card()
        bpc = self._src_only_card() + self._tar_only_card()

        return apd / (apd + self.theta * bpc)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
