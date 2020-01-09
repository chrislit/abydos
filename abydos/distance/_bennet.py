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

"""abydos.distance._bennet.

Bennet's S correlation
"""

from ._token_distance import _TokenDistance

__all__ = ['Bennet']


class Bennet(_TokenDistance):
    r"""Bennet's S correlation.

    For two sets X and Y and a population N, Bennet's :math:`S`
    correlation :cite:`Bennet:1954` is

        .. math::

            corr_{Bennet}(X, Y) = S =
            \frac{p_o - p_e^S}{1 - p_e^S}

    where

        .. math::

            p_o = \frac{|X \cap Y| + |(N \setminus X) \setminus Y|}{|N|}

            p_e^S = \frac{1}{2}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            p_o = \frac{a+d}{n}

            p_e^S = \frac{1}{2}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Bennet instance.

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
        super(Bennet, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return the Bennet's S correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Bennet's S correlation

        Examples
        --------
        >>> cmp = Bennet()
        >>> cmp.corr('cat', 'hat')
        0.989795918367347
        >>> cmp.corr('Niall', 'Neil')
        0.9821428571428572
        >>> cmp.corr('aluminum', 'Catalan')
        0.9617834394904459
        >>> cmp.corr('ATCG', 'TAGC')
        0.9744897959183674


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        d = self._total_complement_card()
        n = self._population_unique_card()

        return 2 * (a + d) / n - 1

    def sim(self, src, tar):
        """Return the Bennet's S similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Bennet's S similarity

        Examples
        --------
        >>> cmp = Bennet()
        >>> cmp.sim('cat', 'hat')
        0.9948979591836735
        >>> cmp.sim('Niall', 'Neil')
        0.9910714285714286
        >>> cmp.sim('aluminum', 'Catalan')
        0.9808917197452229
        >>> cmp.sim('ATCG', 'TAGC')
        0.9872448979591837


        .. versionadded:: 0.4.0

        """
        return (1 + self.corr(src, tar)) / 2


if __name__ == '__main__':
    import doctest

    doctest.testmod()
