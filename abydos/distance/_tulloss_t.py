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

"""abydos.distance._tulloss_t.

Tulloss' T similarity
"""

from ._token_distance import _TokenDistance
from ._tulloss_r import TullossR
from ._tulloss_s import TullossS
from ._tulloss_u import TullossU

__all__ = ['TullossT']


class TullossT(_TokenDistance):
    r"""Tulloss' T similarity.

    For two sets X and Y and a population N, Tulloss' T similarity
    :cite:`Tulloss:1997` is

        .. math::

            \begin{array}{l}
            sim_{Tulloss_T}(X, Y) = \sqrt{sim_{Tulloss_U}(X, Y) \cdot
            sim_{Tulloss_S}(X, Y) \cdot sim_{Tulloss_R}(X, Y)}

            = \sqrt{
            log_2(1+\frac{min(|X \setminus Y|, |Y \setminus X|)+|X \cap Y|}
            {max(|X \setminus Y|, |Y \setminus X|)+|X \cap Y|}) \cdot
            \frac{1}{\sqrt{log_2(2+\frac{min(|X \setminus Y|, |Y \setminus X|)}
            {|X \cap Y|+1})}} \cdot
            \frac{log(1+\frac{|X \cap Y|}{|X|}) \cdot log(1+\frac{|X \cap Y|}
            {|Y|})}{log^2(2)}}
            \end{array}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{Tulloss_T} = \sqrt{
            log_2\Big(1+\frac{min(b, c)+a}{max(b, c)+a}\Big) \cdot
            \frac{1}{\sqrt{log_2(2+\frac{min(b,c)}{a+1})}} \cdot
            \frac{log(1+\frac{a}{a+b}) \cdot log(1+\frac{a}{a+c})}{log^2(2)}}

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize TullossT instance.

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
        super(TullossT, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )
        self._r = TullossR()
        self._s = TullossS()
        self._u = TullossU()

    def sim(self, src, tar):
        """Return Tulloss' T similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Tulloss' T similarity

        Examples
        --------
        >>> cmp = TullossT()
        >>> cmp.sim('cat', 'hat')
        0.5363348766461724
        >>> cmp.sim('Niall', 'Neil')
        0.3740873705689327
        >>> cmp.sim('aluminum', 'Catalan')
        0.1229300783095269
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        r = self._r.sim(src, tar)
        s = self._s.sim(src, tar)
        u = self._u.sim(src, tar)

        return (r * s * u) ** 0.5


if __name__ == '__main__':
    import doctest

    doctest.testmod()
