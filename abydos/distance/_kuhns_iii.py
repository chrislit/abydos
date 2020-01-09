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

"""abydos.distance._kuhns_iii.

Kuhns III correlation
"""

from ._token_distance import _TokenDistance

__all__ = ['KuhnsIII']


class KuhnsIII(_TokenDistance):
    r"""Kuhns III correlation.

    For two sets X and Y and a population N, Kuhns III correlation
    :cite:`Kuhns:1965`, the excess of proportion of overlap over its
    independence value (P), is

        .. math::

            corr_{KuhnsIII}(X, Y) =
            \frac{\delta(X, Y)}{\big(1-\frac{|X \cap Y|}{|X|+|Y|}\big)
            \big(|X|+|Y|-\frac{|X|\cdot|Y|}{|N|}\big)}

    where

        .. math::

            \delta(X, Y) = |X \cap Y| - \frac{|X| \cdot |Y|}{|N|}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            corr_{KuhnsIII} =
            \frac{\delta(a+b, a+c)}{\big(1-\frac{a}{2a+b+c}\big)
            \big(2a+b+c-\frac{(a+b)(a+c)}{n}\big)}

    where

        .. math::

            \delta(a+b, a+c) = a - \frac{(a+b)(a+c)}{n}

    Notes
    -----
    The coefficient presented in :cite:`Eidenberger:2014,Morris:2012` as Kuhns'
    "Proportion of overlap above independence" is a significantly different
    coefficient, not evidenced in :cite:`Kuhns:1965`.

    .. versionadded:: 0.4.0

    """

    def __init__(
        self,
        alphabet=None,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize KuhnsIII instance.

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
        super(KuhnsIII, self).__init__(
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def corr(self, src, tar):
        """Return the Kuhns III correlation of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Kuhns III correlation

        Examples
        --------
        >>> cmp = KuhnsIII()
        >>> cmp.corr('cat', 'hat')
        0.3307757885763001
        >>> cmp.corr('Niall', 'Neil')
        0.21873141468207793
        >>> cmp.corr('aluminum', 'Catalan')
        0.05707545392902886
        >>> cmp.corr('ATCG', 'TAGC')
        -0.003198976327575176


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        b = self._src_only_card()
        c = self._tar_only_card()
        n = self._population_unique_card()

        apbmapc = (a + b) * (a + c)
        if not apbmapc:
            delta_ab = a
        else:
            delta_ab = a - apbmapc / n
        if not delta_ab:
            return 0.0
        else:
            return delta_ab / (
                (1 - a / (2 * a + b + c))
                * (2 * a + b + c - ((a + b) * (a + c) / n))
            )

    def sim(self, src, tar):
        """Return the Kuhns III similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Kuhns III similarity

        Examples
        --------
        >>> cmp = KuhnsIII()
        >>> cmp.sim('cat', 'hat')
        0.498081841432225
        >>> cmp.sim('Niall', 'Neil')
        0.41404856101155846
        >>> cmp.sim('aluminum', 'Catalan')
        0.29280659044677165
        >>> cmp.sim('ATCG', 'TAGC')
        0.24760076775431863


        .. versionadded:: 0.4.0

        """
        return (1 / 3 + self.corr(src, tar)) / (4 / 3)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
