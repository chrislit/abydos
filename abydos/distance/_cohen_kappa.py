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

"""abydos.distance._cohen_kappa.

Cohen's Kappa similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['CohenKappa']


class CohenKappa(_TokenDistance):
    r"""Cohen's Kappa similarity.

    For two sets X and Y and a population N, Cohen's \kappa similarity
    :cite:`Cohen:1960` is

        .. math::

            sim_{Cohen_\kappa}(X, Y) = \kappa =
            \frac{p_o - p_e^\kappa}{1 - p_e^\kappa}

    where

        .. math::

            \begin{array}{l}
            p_o = \frac{|X \cap Y| + |(N \setminus X) \setminus Y|}{|N|}\\
            \\
            p_e^\kappa = \frac{|X|}{|N|} \cdot \frac{|Y|}{|N|} +
            \frac{|N \setminus X|}{|N|} \cdot \frac{|N \setminus Y|}{|N|}
            \end{array}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            \begin{array}{l}
            p_o = \frac{a+d}{n}\\
            \\
            p_e^\kappa = \frac{a+b}{n} \cdot \frac{a+c}{n} +
            \frac{c+d}{n} \cdot \frac{b+d}{n}
            \end{array}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize CohenKappa instance.

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
        super(CohenKappa, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return Cohen's Kappa similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Cohen's Kappa similarity

        Examples
        --------
        >>> cmp = CohenKappa()
        >>> cmp.sim('cat', 'hat')
        0.9974358974358974
        >>> cmp.sim('Niall', 'Neil')
        0.9955041746949261
        >>> cmp.sim('aluminum', 'Catalan')
        0.9903412749517064
        >>> cmp.sim('ATCG', 'TAGC')
        0.993581514762516


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        b = self._src_only_card()
        c = self._tar_only_card()
        d = self._total_complement_card()

        if d:
            return 2 * d / (b + c + 2 * d)
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
