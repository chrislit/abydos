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

"""abydos.distance._unigram_subtuple.

Unigram subtuple similarity
"""

from math import log

from ._token_distance import _TokenDistance

__all__ = ['UnigramSubtuple']


class UnigramSubtuple(_TokenDistance):
    r"""Unigram subtuple similarity.

    For two sets X and Y and a population N, unigram subtuple similarity
    :cite:`Pecina:2010` is

        .. math::

            sim_{unigram~subtuple}(X, Y) =
            log(\frac{|X \cap Y| \cdot |(N \setminus X) \setminus Y|}
            {|X \setminus Y| \cdot |Y \setminus Y|}) - 3.29 \cdot
            \sqrt{\frac{1}{|X \cap Y|} + \frac{1}{|X \setminus Y|} +
            \frac{1}{|Y \setminus X|} +
            \frac{1}{|(N \setminus X) \setminus Y|}}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{unigram~subtuple} =
            log(\frac{ad}{bc}) - 3.29 \cdot
            \sqrt{\frac{1}{a} + \frac{1}{b} + \frac{1}{c} + \frac{1}{d}}


    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize UnigramSubtuple instance.

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
        super(UnigramSubtuple, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim_score(self, src, tar):
        """Return the unigram subtuple similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Unigram subtuple similarity

        Examples
        --------
        >>> cmp = UnigramSubtuple()
        >>> cmp.sim_score('cat', 'hat')
        1.9324426894059226
        >>> cmp.sim_score('Niall', 'Neil')
        1.4347242883606355
        >>> cmp.sim_score('aluminum', 'Catalan')
        -1.0866724701675263
        >>> cmp.sim_score('ATCG', 'TAGC')
        -0.461880260111438


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = max(1, self._intersection_card())
        b = max(1, self._src_only_card())
        c = max(1, self._tar_only_card())
        d = max(1, self._total_complement_card())

        return (
            log(a * d / (b * c))
            - 3.29 * (1 / a + 1 / b + 1 / c + 1 / d) ** 0.5
        )

    def sim(self, src, tar):
        """Return the unigram subtuple similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Unigram subtuple similarity

        Examples
        --------
        >>> cmp = UnigramSubtuple()
        >>> cmp.sim('cat', 'hat')
        0.6215275850074894
        >>> cmp.sim('Niall', 'Neil')
        0.39805896767519555
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        score = self.sim_score(src, tar)
        if score < 0:
            return 0.0
        return score / max(self.sim_score(src, src), self.sim_score(tar, tar))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
