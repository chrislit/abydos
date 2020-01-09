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

"""abydos.distance._consonni_todeschini_ii.

Consonni & Todeschini II similarity
"""

from math import log1p

from ._token_distance import _TokenDistance

__all__ = ['ConsonniTodeschiniII']


class ConsonniTodeschiniII(_TokenDistance):
    r"""Consonni & Todeschini II similarity.

    For two sets X and Y and a population N, Consonni & Todeschini II
    similarity :cite:`Consonni:2012` is

        .. math::

            sim_{ConsonniTodeschiniII}(X, Y) =
            \frac{log(1+|N|) - log(1+|X \setminus Y|+|Y \setminus X|}
            {log(1+|N|)}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{ConsonniTodeschiniII} =
            \frac{log(1+n)-log(1+b+c)}{log(1+n)}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize ConsonniTodeschiniII instance.

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
        super(ConsonniTodeschiniII, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Consonni & Todeschini II similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Consonni & Todeschini II similarity

        Examples
        --------
        >>> cmp = ConsonniTodeschiniII()
        >>> cmp.sim('cat', 'hat')
        0.7585487129939101
        >>> cmp.sim('Niall', 'Neil')
        0.6880377723094788
        >>> cmp.sim('aluminum', 'Catalan')
        0.5841297898633079
        >>> cmp.sim('ATCG', 'TAGC')
        0.640262668568961


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        b = self._src_only_card()
        c = self._tar_only_card()
        n = self._population_unique_card()

        return (log1p(n) - log1p(b + c)) / log1p(n)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
