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

"""abydos.distance._dennis.

Dennis similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['Dennis']


class Dennis(_TokenDistance):
    r"""Dennis similarity.

    For two sets X and Y and a population N, Dennis similarity
    :cite:`Dennis:1965` is

        .. math::

            sim_{Dennis}(X, Y) =
            \frac{|X \cap Y| - \frac{|X| \cdot |Y|}{|N|}}
            {\sqrt{\frac{|X|\cdot|Y|}{|N|}}}

    This is the fourth of Dennis' association measures, and that which she
    claims is the best of the four.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{Dennis} =
            \frac{a-\frac{(a+b)(a+c)}{n}}{\sqrt{\frac{(a+b)(a+c)}{n}}}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Dennis instance.

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
        super(Dennis, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim_score(self, src, tar):
        """Return the Dennis similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Dennis similarity

        Examples
        --------
        >>> cmp = Dennis()
        >>> cmp.sim_score('cat', 'hat')
        13.857142857142858
        >>> cmp.sim_score('Niall', 'Neil')
        10.028539207654113
        >>> cmp.sim_score('aluminum', 'Catalan')
        2.9990827802847835
        >>> cmp.sim_score('ATCG', 'TAGC')
        -0.17857142857142858


        .. versionadded:: 0.4.0

        """
        if not src and not tar:
            return 0.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        abacn = (
            self._src_card()
            * self._tar_card()
            / self._population_unique_card()
        )

        num = a - abacn
        if num == 0:
            return 0.0

        return num / abacn ** 0.5

    def corr(self, src, tar):
        """Return the Dennis correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Dennis correlation

        Examples
        --------
        >>> cmp = Dennis()
        >>> cmp.corr('cat', 'hat')
        0.494897959183673
        >>> cmp.corr('Niall', 'Neil')
        0.358162114559075
        >>> cmp.corr('aluminum', 'Catalan')
        0.107041854561785
        >>> cmp.corr('ATCG', 'TAGC')
        -0.006377551020408


        .. versionadded:: 0.4.0

        """
        score = self.sim_score(src, tar)
        if score == 0.0:
            return 0.0
        return round(score / self._population_unique_card() ** 0.5, 15)

    def sim(self, src, tar):
        """Return the normalized Dennis similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Dennis similarity

        Examples
        --------
        >>> cmp = Dennis()
        >>> cmp.sim('cat', 'hat')
        0.6632653061224487
        >>> cmp.sim('Niall', 'Neil')
        0.5721080763727167
        >>> cmp.sim('aluminum', 'Catalan')
        0.4046945697078567
        >>> cmp.sim('ATCG', 'TAGC')
        0.32908163265306134


        .. versionadded:: 0.4.0

        """
        return (0.5 + self.corr(src, tar)) / 1.5


if __name__ == '__main__':
    import doctest

    doctest.testmod()
