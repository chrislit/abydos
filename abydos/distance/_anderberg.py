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

"""abydos.distance._anderberg.

Anderberg's d
"""

from ._token_distance import _TokenDistance

__all__ = ['Anderberg']


class Anderberg(_TokenDistance):
    r"""Anderberg's D.

    For two sets X and Y and a population N, Anderberg's D
    :cite:`Anderberg:1973` is

        .. math::

            t_1 = max(|X \cap Y|, |X \setminus Y|)+
            max(|Y \setminus X|, |(N \setminus X) \setminus Y|)+\\
            max(|X \cap Y|, |Y \setminus X|)+
            max(|X \setminus Y|, |(N \setminus X) \setminus Y|)\\
            \\
            t_2 = max(|Y|, |N \setminus Y|)+max(|X|, |N \setminus X|)\\
            \\
            sim_{Anderberg}(X, Y) =
            \frac{t_1-t_2}{2|N|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{Anderberg} =
            \frac{(max(a,b)+max(c,d)+max(a,c)+max(b,d))-
            (max(a+b,b+d)+max(a+b,c+d))}{2n}

    Notes
    -----
    There are various references to another "Anderberg similarity",
    :math:`sim_{Anderberg} = \frac{8a}{8a+b+c}`, but I cannot substantiate
    the claim that this appears in :cite:`Anderberg:1973`. In any case,
    if you want to use this measure, you may instatiate
    :py:class:`WeightedJaccard` with `weight=8`.

    Anderberg states that "[t]his quantity is the actual reduction in the
    error probability (also the actual increase in the correct prediction) as
    a consequence of using predictor information" :cite:`Anderberg:1973`. It
    ranges [0, 0.5] so a ``sim`` method ranging [0, 1] is provided in addition
    to ``sim_score``, which gives the value D itself.

    It is difficult to term this measure a similarity score. Identical strings
    often fail to gain high scores. Also, strings that would otherwise be
    considered quite similar often earn lower scores than those that are less
    similar.


    .. versionadded:: 0.4.0

    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Anderberg instance.

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
        super(Anderberg, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim_score(self, src, tar):
        """Return the Anderberg's D similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Anderberg similarity

        Examples
        --------
        >>> cmp = Anderberg()
        >>> cmp.sim_score('cat', 'hat')
        0.0
        >>> cmp.sim_score('Niall', 'Neil')
        0.0
        >>> cmp.sim_score('aluminum', 'Catalan')
        0.0
        >>> cmp.sim_score('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        num = (max(a, b) + max(c, d) + max(a, c) + max(b, d)) - (
            max(a + c, b + d) + max(a + b, c + d)
        )

        if num == 0.0:
            return 0.0
        return num / (2 * (a + b + c + d))

    def sim(self, src, tar):
        """Return the normalized Anderberg's D similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Anderberg similarity

        Examples
        --------
        >>> cmp = Anderberg()
        >>> cmp.sim('cat', 'hat')
        0.0
        >>> cmp.sim('Niall', 'Neil')
        0.0
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        return 2 * self.sim_score(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
