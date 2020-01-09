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

"""abydos.distance._pattern.

Pattern difference
"""

from ._token_distance import _TokenDistance

__all__ = ['Pattern']


class Pattern(_TokenDistance):
    r"""Pattern difference.

    For two sets X and Y and a population N, the pattern difference
    :cite:`Batagelj:1995`, Batagelj & Bren's :math:`- bc -` is

        .. math::

            dist_{pattern}(X, Y) =
            \frac{4 \cdot |X \setminus Y| \cdot |Y \setminus X|}
            {|N|^2}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            dist_{pattern} =
            \frac{4bc}{n^2}

    In :cite:`IBM:2017`, the formula omits the 4 in the numerator:
    :math:`\frac{bc}{n^2}`.

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Pattern instance.

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
        super(Pattern, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def dist(self, src, tar):
        """Return the Pattern difference of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Pattern difference

        Examples
        --------
        >>> cmp = Pattern()
        >>> cmp.dist('cat', 'hat')
        2.6030820491461892e-05
        >>> cmp.dist('Niall', 'Neil')
        7.809246147438568e-05
        >>> cmp.dist('aluminum', 'Catalan')
        0.0003635035904093472
        >>> cmp.dist('ATCG', 'TAGC')
        0.0001626926280716368


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        b = self._src_only_card()
        c = self._tar_only_card()
        n = self._population_unique_card()

        num = b * c
        if num:
            return 4 * b * c / n ** 2
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
