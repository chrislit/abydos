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

"""abydos.distance._gilbert.

Gilbert correlation
"""

from ._token_distance import _TokenDistance

__all__ = ['Gilbert']


class Gilbert(_TokenDistance):
    r"""Gilbert correlation.

    For two sets X and Y and a population N, the Gilbert correlation
    :cite:`Gilbert:1884` is

        .. math::

            corr_{Gilbert}(X, Y) =
            \frac{2(|X \cap Y| \cdot |(N \setminus X) \setminus Y| -
            |X \setminus Y| \cdot |Y \setminus X|)}
            {|N|^2 - |X \cap Y|^2 + |X \setminus Y|^2 + |Y \setminus X|^2 -
            |(N \setminus X) \setminus Y|^2}

    For lack of access to the original, this formula is based on the concurring
    formulae presented in :cite:`Peirce:1884` and :cite:`Doolittle:1884`.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{Gilbert} =
            \frac{2(ad-cd)}{n^2-a^2+b^2+c^2-d^2}

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Gilbert instance.

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
        super(Gilbert, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return the Gilbert correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Gilbert correlation

        Examples
        --------
        >>> cmp = Gilbert()
        >>> cmp.corr('cat', 'hat')
        0.3310580204778157
        >>> cmp.corr('Niall', 'Neil')
        0.21890122402504983
        >>> cmp.corr('aluminum', 'Catalan')
        0.057094811018577836
        >>> cmp.corr('ATCG', 'TAGC')
        -0.003198976327575176


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        n = self._population_unique_card()

        num = a * n - (a + b) * (a + c)
        if num:
            return num / (n * (a + b + c) - (a + b) * (a + c))
        return 0.0

    def sim(self, src, tar):
        """Return the Gilbert similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Gilbert similarity

        Examples
        --------
        >>> cmp = Gilbert()
        >>> cmp.sim('cat', 'hat')
        0.6655290102389079
        >>> cmp.sim('Niall', 'Neil')
        0.6094506120125249
        >>> cmp.sim('aluminum', 'Catalan')
        0.5285474055092889
        >>> cmp.sim('ATCG', 'TAGC')
        0.4984005118362124


        .. versionadded:: 0.4.0

        """
        return (1.0 + self.corr(src, tar)) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
