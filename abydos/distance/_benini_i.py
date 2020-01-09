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

"""abydos.distance._benini_i.

Benini I correlation
"""

from ._token_distance import _TokenDistance

__all__ = ['BeniniI']


class BeniniI(_TokenDistance):
    r"""BeniniI correlation.

    For two sets X and Y and a population N, Benini I correlation, Benini's
    Index of Attraction, :cite:`Benini:1901` is

        .. math::

            corr_{BeniniI}(X, Y) =
            \frac{|X \cap Y| \cdot |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|}{|Y| \cdot |N \setminus X|}


    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{BeniniI} = \frac{ad-bc}{(a+c)(c+d)}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize BeniniI instance.

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
        super(BeniniI, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return the Benini I correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Benini I correlation

        Examples
        --------
        >>> cmp = BeniniI()
        >>> cmp.corr('cat', 'hat')
        0.49743589743589745
        >>> cmp.corr('Niall', 'Neil')
        0.3953727506426735
        >>> cmp.corr('aluminum', 'Catalan')
        0.11485180412371133
        >>> cmp.corr('ATCG', 'TAGC')
        -0.006418485237483954


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        num = a * d - b * c

        if num == 0.0:
            return 0.0
        return num / ((a + c) * (c + d))

    def sim(self, src, tar):
        """Return the Benini I similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Benini I similarity

        Examples
        --------
        >>> cmp = BeniniI()
        >>> cmp.sim('cat', 'hat')
        0.7487179487179487
        >>> cmp.sim('Niall', 'Neil')
        0.6976863753213367
        >>> cmp.sim('aluminum', 'Catalan')
        0.5574259020618557
        >>> cmp.sim('ATCG', 'TAGC')
        0.496790757381258


        .. versionadded:: 0.4.0

        """
        return (1 + self.corr(src, tar)) / 2


if __name__ == '__main__':
    import doctest

    doctest.testmod()
