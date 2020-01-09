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

"""abydos.distance._lorentzian.

Lorentzian distance
"""

from math import log1p

from ._token_distance import _TokenDistance

__all__ = ['Lorentzian']


class Lorentzian(_TokenDistance):
    r"""Lorentzian distance.

    For two multisets X and Y drawn from an alphabet S, Lorentzian distance is

        .. math::

            dist_{Lorentzian}(X, Y) =
            \sum_{i \in S} log(1 + |A_i - B_i|)

    Notes
    -----
    No primary source for this measure could be located, but it is included
    in surveys and catalogues, such as :cite:`Deza:2016` and :cite:`Cha:2008`.

    .. versionadded:: 0.4.0

    """

    def __init__(self, tokenizer=None, **kwargs):
        """Initialize Lorentzian instance.

        Parameters
        ----------
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
        super(Lorentzian, self).__init__(tokenizer=tokenizer, **kwargs)

    def dist_abs(self, src, tar):
        """Return the Lorentzian distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Lorentzian distance

        Examples
        --------
        >>> cmp = Lorentzian()
        >>> cmp.dist_abs('cat', 'hat')
        2.772588722239781
        >>> cmp.dist_abs('Niall', 'Neil')
        4.852030263919617
        >>> cmp.dist_abs('aluminum', 'Catalan')
        10.1095256359474
        >>> cmp.dist_abs('ATCG', 'TAGC')
        6.931471805599453


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        alphabet = self._total().keys()

        return sum(
            log1p(abs(self._src_tokens[tok] - self._tar_tokens[tok]))
            for tok in alphabet
        )

    def dist(self, src, tar):
        """Return the normalized Lorentzian distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Lorentzian distance

        Examples
        --------
        >>> cmp = Lorentzian()
        >>> cmp.dist('cat', 'hat')
        0.6666666666666667
        >>> cmp.dist('Niall', 'Neil')
        0.7777777777777778
        >>> cmp.dist('aluminum', 'Catalan')
        0.9358355851062377
        >>> cmp.dist('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0
        elif not src or not tar:
            return 1.0

        score = self.dist_abs(src, tar)

        alphabet = self._total().keys()

        return score / sum(
            log1p(max(self._src_tokens[tok], self._tar_tokens[tok]))
            for tok in alphabet
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
