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

"""abydos.distance._unknown_l.

Unknown L similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['UnknownL']


class UnknownL(_TokenDistance):
    r"""Unknown L similarity.

    For two sets X and Y and a population N, Unknown L similarity, which
    :cite:`SequentiX:2018` attributes to "Roux" but could not be
    located, is

        .. math::

            sim_{UnknownL}(X, Y) =
            \frac{|X \cap Y| + |(N \setminus X) \setminus Y|}
            {min(|X \setminus Y|, |Y \setminus X|) +
            min(|N|-|X \setminus Y|, |N|-|Y \setminus X|)}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{UnknownL} =
            \frac{a+d}{min(b, c) + min(n-b, n-c)}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize UnknownL instance.

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
        super(UnknownL, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Unknown L similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Unknown L similarity

        Examples
        --------
        >>> cmp = UnknownL()
        >>> cmp.sim('cat', 'hat')
        0.9948979591836735
        >>> cmp.sim('Niall', 'Neil')
        0.9923371647509579
        >>> cmp.sim('aluminum', 'Catalan')
        0.9821428571428571
        >>> cmp.sim('ATCG', 'TAGC')
        0.9872448979591837


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        if not self._src_card() or not self._tar_card():
            return 1.0

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = self._population_unique_card()

        return (a + d) / (min(b, c) + min(n - b, n - c))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
