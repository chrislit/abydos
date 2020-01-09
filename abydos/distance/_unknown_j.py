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

"""abydos.distance._unknown_j.

Unknown J similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['UnknownJ']


class UnknownJ(_TokenDistance):
    r"""Unknown J similarity.

    For two sets X and Y and a population N, Unknown J similarity, which
    :cite:`SequentiX:2018` attributes to "Kocher & Wang" but could not be
    located, is

        .. math::

            sim_{UnknownJ}(X, Y) =
            |X \cap Y| \cdot \frac{|N|}{|X| \cdot |N \setminus X|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{UnknownJ} =
            a \cdot \frac{n}{(a+b)(c+d)}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize UnknownJ instance.

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
        super(UnknownJ, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim_score(self, src, tar):
        """Return the Unknown J similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Unknown J similarity

        Examples
        --------
        >>> cmp = UnknownJ()
        >>> cmp.sim_score('cat', 'hat')
        0.5025641025641026
        >>> cmp.sim_score('Niall', 'Neil')
        0.33590402742073694
        >>> cmp.sim_score('aluminum', 'Catalan')
        0.11239977090492555
        >>> cmp.sim_score('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = max(1.0, self._total_complement_card())
        n = a + b + c + d

        an = a * n
        if an:
            return a * n / ((a + b) * (c + d))
        return 0.0

    def sim(self, src, tar):
        """Return the normalized Unknown J similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Unknown J similarity

        Examples
        --------
        >>> cmp = UnknownJ()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.33333333333333337
        >>> cmp.sim('aluminum', 'Catalan')
        0.11111111111111112
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        score = self.sim_score(src, tar)
        if score:
            return score / max(
                self.sim_score(src, src), self.sim_score(tar, tar)
            )
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
