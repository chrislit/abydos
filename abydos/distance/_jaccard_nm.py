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

"""abydos.distance._jaccard_nm.

Jaccard-NM similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['JaccardNM']


class JaccardNM(_TokenDistance):
    r"""Jaccard-NM similarity.

    For two sets X and Y and a population N, Jaccard-NM similarity
    :cite:`Naseem:2011` is

        .. math::

            sim_{JaccardNM}(X, Y) =
            \frac{|X \cap Y|}
            {|N| + |X \cap Y| + |X \setminus Y| + |Y \setminus X|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{JaccardNM} =
            \frac{a}{2(a+b+c)+d}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize JaccardNM instance.

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
        super(JaccardNM, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim_score(self, src, tar):
        """Return the Jaccard-NM similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Jaccard-NM similarity

        Examples
        --------
        >>> cmp = JaccardNM()
        >>> cmp.sim_score('cat', 'hat')
        0.002531645569620253
        >>> cmp.sim_score('Niall', 'Neil')
        0.0025220680958385876
        >>> cmp.sim_score('aluminum', 'Catalan')
        0.0012484394506866417
        >>> cmp.sim_score('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        if not src or not tar:
            return 0.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        n = self._population_unique_card()

        return a / (a + b + c + n)

    def sim(self, src, tar):
        """Return the Jaccard-NM similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Jaccard-NM similarity

        Examples
        --------
        >>> cmp = JaccardNM()
        >>> cmp.sim('cat', 'hat')
        0.005063291139240506
        >>> cmp.sim('Niall', 'Neil')
        0.005044136191677175
        >>> cmp.sim('aluminum', 'Catalan')
        0.0024968789013732834
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        return 2 * self.sim_score(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
