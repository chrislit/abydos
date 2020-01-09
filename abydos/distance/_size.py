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

"""abydos.distance._size_difference.

Penrose's size difference
"""

from ._token_distance import _TokenDistance

__all__ = ['Size']


class Size(_TokenDistance):
    r"""Penrose's size difference.

    For two sets X and Y and a population N, the Penrose's size difference
    :cite:`Penrose:1952` is

        .. math::

            sim_{Size}(X, Y) =
            \frac{(|X \triangle Y|)^2}{|N|^2}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{Size} =
            \frac{(b+c)^2}{n^2}

    In :cite:`IBM:2017`, the formula is instead :math:`\frac{(b-c)^2}{n^2}`,
    but it is clear from :cite:`Penrose:1952` that this should not be an
    assymmetric value with respect two the ordering of the two sets. Meanwhile,
    :cite:`Deza:2016` gives a formula that is equivalent to
    :math:`\sqrt{n}\cdot(b+c)`.

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Size instance.

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
        super(Size, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def dist(self, src, tar):
        """Return the Penrose's size difference of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Size difference

        Examples
        --------
        >>> cmp = Size()
        >>> cmp.sim('cat', 'hat')
        0.9999739691795085
        >>> cmp.sim('Niall', 'Neil')
        0.9999202806122449
        >>> cmp.sim('aluminum', 'Catalan')
        0.9996348736257049
        >>> cmp.sim('ATCG', 'TAGC')
        0.9998373073719283


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0

        self._tokenize(src, tar)

        return (
            self._symmetric_difference_card()
        ) ** 2 / self._population_unique_card() ** 2


if __name__ == '__main__':
    import doctest

    doctest.testmod()
