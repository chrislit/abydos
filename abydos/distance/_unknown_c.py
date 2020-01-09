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

"""abydos.distance._unknown_c.

Unknown C similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['UnknownC']


class UnknownC(_TokenDistance):
    r"""Unknown C similarity.

    For two sets X and Y and a population N, Unknown C similarity, which
    :cite:`Morris:2012` attributes to :cite:`Gower:1971` but could not be
    located in that source, is

        .. math::

            sim_{UnknownC}(X, Y) =
            \frac{|X \cap Y| + |(N \setminus X) \setminus Y|}
            {\sqrt{|X| \cdot |Y| \cdot |N \setminus X| \cdot |N \setminus Y|}}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{UnknownC} =
            \frac{a+d}{\sqrt{(a+b)(a+c)(b+d)(c+d)}}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize UnknownC instance.

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
        super(UnknownC, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Unknown C similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Unknown C similarity

        Examples
        --------
        >>> cmp = UnknownC()
        >>> cmp.sim('cat', 'hat')
        0.25
        >>> cmp.sim('Niall', 'Neil')
        0.18222244271345164
        >>> cmp.sim('aluminum', 'Catalan')
        0.11686463498390019
        >>> cmp.sim('ATCG', 'TAGC')
        0.1987163029525032


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        num = a + d
        if num:
            return (
                num
                / (
                    max(1, a + b)
                    * max(1, a + c)
                    * max(1, b + d)
                    * max(1, c + d)
                )
                ** 0.5
            )
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
