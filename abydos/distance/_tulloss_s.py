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

"""abydos.distance._tulloss_s.

Tulloss' S similarity
"""

from math import log2

from ._token_distance import _TokenDistance

__all__ = ['TullossS']


class TullossS(_TokenDistance):
    r"""Tulloss' S similarity.

    For two sets X and Y and a population N, Tulloss' S similarity
    :cite:`Tulloss:1997` is

        .. math::

            sim_{Tulloss_S}(X, Y) =
            \frac{1}{\sqrt{log_2(2+\frac{min(|X \setminus Y|, |Y \setminus X|)}
            {|X \cap Y|+1})}}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{Tulloss_S} =
            \frac{1}{\sqrt{log_2(2+\frac{min(b,c)}{a+1})}}

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize TullossS instance.

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
        super(TullossS, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )

    def sim(self, src, tar):
        """Return Tulloss' S similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Tulloss' S similarity

        Examples
        --------
        >>> cmp = TullossS()
        >>> cmp.sim('cat', 'hat')
        0.8406515643305636
        >>> cmp.sim('Niall', 'Neil')
        0.7943108670863427
        >>> cmp.sim('aluminum', 'Catalan')
        0.6376503816669968
        >>> cmp.sim('ATCG', 'TAGC')
        0.5968309535438173


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()

        return 1 / (log2(2 + min(b, c) / (a + 1))) ** 0.5


if __name__ == '__main__':
    import doctest

    doctest.testmod()
