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

"""abydos.distance._eyraud.

Eyraud similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['Eyraud']


class Eyraud(_TokenDistance):
    r"""Eyraud similarity.

    For two sets X and Y and a population N, the Eyraud
    similarity :cite:`Eyraud:1938` is

        .. math::

            sim_{Eyraud}(X, Y) =
            \frac{|X \cap Y| - |X| \cdot |Y|}
            {|X| \cdot |Y| \cdot |N \setminus Y| \cdot |N \setminus X|}

    For lack of access to the original, this formula is based on the concurring
    formulae presented in :cite:`Shi:1993` and :cite:`Hubalek:1982`.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{Eyraud} =
            \frac{a-(a+b)(a+c)}{(a+b)(a+c)(b+d)(c+d)}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Eyraud instance.

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
        super(Eyraud, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim_score(self, src, tar):
        """Return the Eyraud similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Eyraud similarity

        Examples
        --------
        >>> cmp = Eyraud()
        >>> cmp.sim_score('cat', 'hat')
        -1.438198553583169e-06
        >>> cmp.sim_score('Niall', 'Neil')
        -1.5399964580081465e-06
        >>> cmp.sim_score('aluminum', 'Catalan')
        -1.6354719962967386e-06
        >>> cmp.sim_score('ATCG', 'TAGC')
        -1.6478781097519779e-06


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        denom = max(1, a + b) * max(1, c + d) * max(1, a + c) * max(1, b + d)
        num = a - (a + b) * (a + c)

        return num / denom

    def sim(self, src, tar):
        """Return the normalized Eyraud similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Eyraud similarity

        Examples
        --------
        >>> cmp = Eyraud()
        >>> cmp.sim('cat', 'hat')
        1.438198553583169e-06
        >>> cmp.sim('Niall', 'Neil')
        1.5399964580081465e-06
        >>> cmp.sim('aluminum', 'Catalan')
        1.6354719962967386e-06
        >>> cmp.sim('ATCG', 'TAGC')
        1.6478781097519779e-06


        .. versionadded:: 0.4.0

        """
        return 0.0 - self.sim_score(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
