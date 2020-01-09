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

"""abydos.distance._consonni_todeschini_i.

Consonni & Todeschini I similarity
"""

from math import log1p

from ._token_distance import _TokenDistance

__all__ = ['ConsonniTodeschiniI']


class ConsonniTodeschiniI(_TokenDistance):
    r"""Consonni & Todeschini I similarity.

    For two sets X and Y and a population N, Consonni & Todeschini I similarity
    :cite:`Consonni:2012` is

        .. math::

            sim_{ConsonniTodeschiniI}(X, Y) =
            \frac{log(1+|X \cap Y|+|(N \setminus X) \setminus Y|)}
            {log(1+|N|)}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{ConsonniTodeschiniI} =
            \frac{log(1+a+d)}{log(1+n)}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize ConsonniTodeschiniI instance.

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
        super(ConsonniTodeschiniI, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Consonni & Todeschini I similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Consonni & Todeschini I similarity

        Examples
        --------
        >>> cmp = ConsonniTodeschiniI()
        >>> cmp.sim('cat', 'hat')
        0.9992336018090547
        >>> cmp.sim('Niall', 'Neil')
        0.998656222829757
        >>> cmp.sim('aluminum', 'Catalan')
        0.9971098629456009
        >>> cmp.sim('ATCG', 'TAGC')
        0.9980766131469967


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        d = self._total_complement_card()
        n = self._population_unique_card()

        return log1p(a + d) / log1p(n)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
