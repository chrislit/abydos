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

"""abydos.distance._unknown_i.

Unknown I similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['UnknownI']


class UnknownI(_TokenDistance):
    r"""Unknown I similarity.

    For two sets X and Y, the Unknown I similarity is based on
    Mountford similarity :cite:`Mountford:1962` :class:`Mountford`.

        .. math::

            sim_{UnknownI}(X, Y) =
            \frac{2(|X \cap Y|+1)}{2((|X|+2)\cdot(|Y|+2))-
            (|X|+|Y|+4)\cdot(|X \cap Y|+1)}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{UnknownI} =
            \frac{2(a+1)}{2(a+b+2)(a+c+2)-(2a+b+c+4)(a+1)}

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize UnknownI instance.

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
        super(UnknownI, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )

    def sim(self, src, tar):
        """Return the Unknown I similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Unknown I similarity

        Examples
        --------
        >>> cmp = UnknownI()
        >>> cmp.sim('cat', 'hat')
        0.16666666666666666
        >>> cmp.sim('Niall', 'Neil')
        0.08955223880597014
        >>> cmp.sim('aluminum', 'Catalan')
        0.02247191011235955
        >>> cmp.sim('ATCG', 'TAGC')
        0.023809523809523808


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card() + 1
        b = self._src_only_card() + 1
        c = self._tar_only_card() + 1

        return 2.0 * a / (c * (a + 2.0 * b) + a * b)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
