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

"""abydos.distance._sokal_sneath_ii.

Sokal & Sneath II similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['SokalSneathII']


class SokalSneathII(_TokenDistance):
    r"""Sokal & Sneath II similarity.

    For two sets X and Y, Sokal & Sneath II similarity :cite:`Sokal:1963` is

        .. math::

            sim_{SokalSneathII}(X, Y) =
            \frac{|X \cap Y|}
            {|X \cap Y| + 2|X \triangle Y|}

    This is the second of five "Unnamed coefficients" presented in
    :cite:`Sokal:1963`. It corresponds to the "Unmatched pairs carry twice the
    weight of matched pairs in the Denominator" with "Negative Matches in
    Numerator Excluded".
    "Negative Matches in Numerator Included" corresponds to the Rogers &
    Tanimoto similarity, :class:`.RogersTanimoto`.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{SokalSneathII} =
            \frac{a}{a+2(b+c)}

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize SokalSneathII instance.

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
        super(SokalSneathII, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )

    def sim(self, src, tar):
        """Return the Sokal & Sneath II similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Sokal & Sneath II similarity

        Examples
        --------
        >>> cmp = SokalSneathII()
        >>> cmp.sim('cat', 'hat')
        0.2
        >>> cmp.sim('Niall', 'Neil')
        0.125
        >>> cmp.sim('aluminum', 'Catalan')
        0.03225806451612903
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()

        return a / (a + 2 * (b + c))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
