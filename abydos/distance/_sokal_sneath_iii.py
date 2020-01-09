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

"""abydos.distance._sokal_sneath_iii.

Sokal & Sneath III similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['SokalSneathIII']


class SokalSneathIII(_TokenDistance):
    r"""Sokal & Sneath III similarity.

    For two sets X and Y and a population N, Sokal & Sneath III similarity
    :cite:`Sokal:1963` is

        .. math::

            sim_{SokalSneathIII}(X, Y) =
            \frac{|X \cap Y| + |(N \setminus X) \setminus Y|}
            {|X \triangle Y|}

    This is the third of five "Unnamed coefficients" presented in
    :cite:`Sokal:1963`. It corresponds to the "Unmatched pairs only in the
    Denominator" with "Negative Matches in Numerator Excluded".
    "Negative Matches in Numerator Included" corresponds to the Kulczynski I
    coefficient, :class:`.KulczynskiI`.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{SokalSneathIII} =
            \frac{a+d}{b+c}

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize SokalSneathIII instance.

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
        super(SokalSneathIII, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )

    def sim_score(self, src, tar):
        """Return the Sokal & Sneath III similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Sokal & Sneath III similarity

        Examples
        --------
        >>> cmp = SokalSneathIII()
        >>> cmp.sim_score('cat', 'hat')
        195.0
        >>> cmp.sim_score('Niall', 'Neil')
        111.0
        >>> cmp.sim_score('aluminum', 'Catalan')
        51.333333333333336
        >>> cmp.sim_score('ATCG', 'TAGC')
        77.4

        .. versionadded:: 0.4.0

        """
        if src == tar:
            return float('inf')

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        if a + d > 0 and b + c == 0:
            return float('inf')
        return (a + d) / (b + c)

    def sim(self, *args, **kwargs):
        """Raise exception when called.

        Parameters
        ----------
        *args
            Variable length argument list
        **kwargs
            Arbitrary keyword arguments

        Raises
        ------
        NotImplementedError
            Method disabled for Sokal & Sneath III similarity.


        .. versionadded:: 0.3.6

        """
        raise NotImplementedError(
            'Method disabled for Sokal & Sneath III similarity.'
        )

    def dist(self, *args, **kwargs):
        """Raise exception when called.

        Parameters
        ----------
        *args
            Variable length argument list
        **kwargs
            Arbitrary keyword arguments

        Raises
        ------
        NotImplementedError
            Method disabled for Sokal & Sneath III similarity.


        .. versionadded:: 0.3.6

        """
        raise NotImplementedError(
            'Method disabled for Sokal & Sneath III similarity.'
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
