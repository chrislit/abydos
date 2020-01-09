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

"""abydos.distance._canberra.

Canberra distance
"""

from ._token_distance import _TokenDistance

__all__ = ['Canberra']


class Canberra(_TokenDistance):
    r"""Canberra distance.

    For two sets X and Y, the Canberra distance :cite:`Lance:1966,Lance:1967b`
    is

        .. math::

            sim_{Canberra}(X, Y) = \frac{|X \triangle Y|}{|X|+|Y|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{Canberra} =
            \frac{b+c}{(a+b)+(a+c)}

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize Canberra instance.

        Parameters
        ----------
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
        super(Canberra, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )

    def dist(self, src, tar):
        """Return the Canberra distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Canberra distance

        Examples
        --------
        >>> cmp = Canberra()
        >>> cmp.dist('cat', 'hat')
        0.5
        >>> cmp.dist('Niall', 'Neil')
        0.6363636363636364
        >>> cmp.dist('aluminum', 'Catalan')
        0.8823529411764706
        >>> cmp.dist('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0

        self._tokenize(src, tar)

        return self._symmetric_difference_card() / self._total_card()


if __name__ == '__main__':
    import doctest

    doctest.testmod()
