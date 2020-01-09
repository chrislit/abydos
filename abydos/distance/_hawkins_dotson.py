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

"""abydos.distance._hawkins_dotson.

Hawkins & Dotson similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['HawkinsDotson']


class HawkinsDotson(_TokenDistance):
    r"""Hawkins & Dotson similarity.

    For two sets X and Y and a population N, Hawkins & Dotson similarity
    :cite:`Hawkins:1973` is the mean of the occurrence agreement and
    non-occurrence agreement

        .. math::

            sim_{HawkinsDotson}(X, Y) =
            \frac{1}{2}\cdot\Big(
            \frac{|X \cap Y|}{|X \cup Y|}+
            \frac{|(N \setminus X) \setminus Y|}{|N \setminus (X \cap Y)|}
            \Big)

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{HawkinsDotson} =
            \frac{1}{2}\cdot\Big(\frac{a}{a+b+c}+\frac{d}{b+c+d}\Big)

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize HawkinsDotson instance.

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
        super(HawkinsDotson, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Hawkins & Dotson similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Hawkins & Dotson similarity

        Examples
        --------
        >>> cmp = HawkinsDotson()
        >>> cmp.sim('cat', 'hat')
        0.6641091219096334
        >>> cmp.sim('Niall', 'Neil')
        0.606635407786303
        >>> cmp.sim('aluminum', 'Catalan')
        0.5216836734693877
        >>> cmp.sim('ATCG', 'TAGC')
        0.49362244897959184


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        score = 0.0
        if a:
            score += a / (a + b + c)
        if d:
            score += d / (b + c + d)
        return score / 2


if __name__ == '__main__':
    import doctest

    doctest.testmod()
