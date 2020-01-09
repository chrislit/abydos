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

"""abydos.distance._gilbert_wells.

Gilbert & Wells similarity
"""

from math import factorial, log, pi
from sys import float_info

from ._token_distance import _TokenDistance

__all__ = ['GilbertWells']

_epsilon = float_info.epsilon


class GilbertWells(_TokenDistance):
    r"""Gilbert & Wells similarity.

    For two sets X and Y and a population N, the Gilbert & Wells
    similarity :cite:`Gilbert:1966` is

        .. math::

            sim_{GilbertWells}(X, Y) =
            ln \frac{|N|^3}{2\pi |X| \cdot |Y| \cdot
            |N \setminus Y| \cdot |N \setminus X|} + 2ln
            \frac{|N|! \cdot |X \cap Y|! \cdot |X \setminus Y|! \cdot
            |Y \setminus X|! \cdot |(N \setminus X) \setminus Y|!}
            {|X|! \cdot |Y|! \cdot |N \setminus Y|! \cdot |N \setminus X|!}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{GilbertWells} =
            ln \frac{n^3}{2\pi (a+b)(a+c)(b+d)(c+d)} +
            2ln \frac{n!a!b!c!d!}{(a+b)!(a+c)!(b+d)!(c+d)!}

    Notes
    -----
    Most lists of similarity & distance measures, including
    :cite:`Hubalek:1982,Choi:2010,Morris:2012` have a quite different formula,
    which would be :math:`ln~a - ln~b - ln \frac{a+b}{n} - ln \frac{a+c}{n} =
    ln\frac{an}{(a+b)(a+c)}`. However, neither this formula nor anything
    similar or equivalent to it appears anywhere within the cited work,
    :cite:`Gilbert:1966`. See :class:``UnknownF`` for this, alternative,
    measure.


    .. versionadded:: 0.4.0

    """

    def __init__(self, alphabet=None, tokenizer=None, **kwargs):
        """Initialize GilbertWells instance.

        Parameters
        ----------
        alphabet : Counter, collection, int, or None
            This represents the alphabet of possible tokens.
            See :ref:`alphabet <alphabet>` description in
            :py:class:`_TokenDistance` for details.
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        **kwargs
            Arbitrary keyword arguments

        Other Parameters
        ----------------
        qval : int
            The length of each q-gram. Using this parameter and tokenizer=None
            will cause the instance to use the QGram tokenizer with this
            q value.


        .. versionadded:: 0.4.0

        """
        super(GilbertWells, self).__init__(
            alphabet=alphabet, tokenizer=tokenizer, **kwargs
        )

    def sim_score(self, src, tar):
        """Return the Gilbert & Wells similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Gilbert & Wells similarity

        Examples
        --------
        >>> cmp = GilbertWells()
        >>> cmp.sim_score('cat', 'hat')
        20.17617447734673
        >>> cmp.sim_score('Niall', 'Neil')
        16.717742356982733
        >>> cmp.sim_score('aluminum', 'Catalan')
        5.495096667524002
        >>> cmp.sim_score('ATCG', 'TAGC')
        1.6845961909440712


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()
        n = self._population_unique_card()

        return log(
            max(
                _epsilon,
                n ** 3
                / (
                    2
                    * pi
                    * max(_epsilon, a + b)
                    * max(_epsilon, a + c)
                    * max(_epsilon, b + d)
                    * max(_epsilon, c + d)
                ),
            )
        ) + 2 * (
            log(factorial(n))
            + log(factorial(a))
            + log(factorial(b))
            + log(factorial(c))
            + log(factorial(d))
            - log(factorial(a + b))
            - log(factorial(a + c))
            - log(factorial(b + d))
            - log(factorial(c + d))
        )

    def sim(self, src, tar):
        """Return the normalized Gilbert & Wells similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Gilbert & Wells similarity

        Examples
        --------
        >>> cmp = GilbertWells()
        >>> cmp.sim('cat', 'hat')
        0.4116913723876516
        >>> cmp.sim('Niall', 'Neil')
        0.2457247406857589
        >>> cmp.sim('aluminum', 'Catalan')
        0.05800001636414742
        >>> cmp.sim('ATCG', 'TAGC')
        0.028716013247135602


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0
        norm = max(self.sim_score(src, src), self.sim_score(tar, tar))
        return self.sim_score(src, tar) / norm


if __name__ == '__main__':
    import doctest

    doctest.testmod()
