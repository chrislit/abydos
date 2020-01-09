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

"""abydos.distance._clement.

Clement similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['Clement']


class Clement(_TokenDistance):
    r"""Clement similarity.

    For two sets X and Y and a population N, Clement similarity
    :cite:`Clement:1976` is defined as

        .. math::

            sim_{Clement}(X, Y) =
            \frac{|X \cap Y|}{|X|}\Big(1-\frac{|X|}{|N|}\Big) +
            \frac{|(N \setminus X) \setminus Y|}{|N \setminus X|}
            \Big(1-\frac{|N \setminus X|}{|N|}\Big)

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{Clement} =
            \frac{a}{a+b}\Big(1 - \frac{a+b}{n}\Big) +
            \frac{d}{c+d}\Big(1 - \frac{c+d}{n}\Big)

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Clement instance.

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
        super(Clement, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Clement similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Clement similarity

        Examples
        --------
        >>> cmp = Clement()
        >>> cmp.sim('cat', 'hat')
        0.5025379382522239
        >>> cmp.sim('Niall', 'Neil')
        0.33840586363079933
        >>> cmp.sim('aluminum', 'Catalan')
        0.12119877280918714
        >>> cmp.sim('ATCG', 'TAGC')
        0.006336616803332366


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = self._population_unique_card()

        score = 0.0
        if a + b:
            score += (a / (a + b)) * (1 - (a + b) / n)
        if c + d:
            score += (d / (c + d)) * (1 - (c + d) / n)

        return score


if __name__ == '__main__':
    import doctest

    doctest.testmod()
