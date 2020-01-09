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

"""abydos.distance._sokal_michener.

Sokal & Michener similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['SokalMichener']


class SokalMichener(_TokenDistance):
    r"""Sokal & Michener similarity.

    For two sets X and Y and a population N, the Sokal & Michener's
    simple matching coefficient :cite:`Sokal:1958`, equivalent to the Rand
    index :cite:`Rand:1971` is

        .. math::

            sim_{SokalMichener}(X, Y) =
            \frac{|X \cap Y| + |(N \setminus X) \setminus Y|}{|N|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{SokalMichener} =
            \frac{a+d}{n}

    Notes
    -----
    The associated distance metric is the mean Manhattan distance and 4 times
    the value of the variance dissimilarity of :cite:`IBM:2017`.

    In terms of a confusion matrix, this is equivalent to accuracy
    :py:meth:`ConfusionTable.accuracy`.

    .. versionadded:: 0.4.0

    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize SokalMichener instance.

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
        super(SokalMichener, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Sokal & Michener similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Sokal & Michener similarity

        Examples
        --------
        >>> cmp = SokalMichener()
        >>> cmp.sim('cat', 'hat')
        0.9948979591836735
        >>> cmp.sim('Niall', 'Neil')
        0.9910714285714286
        >>> cmp.sim('aluminum', 'Catalan')
        0.9808917197452229
        >>> cmp.sim('ATCG', 'TAGC')
        0.9872448979591837


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        d = self._total_complement_card()
        n = self._population_unique_card()

        return (a + d) / n


if __name__ == '__main__':
    import doctest

    doctest.testmod()
