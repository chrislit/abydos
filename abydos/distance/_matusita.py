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

"""abydos.distance._matusita.

Matusita distance
"""

from ._token_distance import _TokenDistance

__all__ = ['Matusita']


class Matusita(_TokenDistance):
    r"""Matusita distance.

    For two multisets X and Y drawn from an alphabet S, Matusita distance
    :cite:`Matusita:1955` is

        .. math::

            dist_{Matusita}(X, Y) =
            \sqrt{\sum_{i \in S} \Bigg(\sqrt{\frac{|A_i|}{|A|}} -
             \sqrt{\frac{|B_i|}{|B|}}\Bigg)^2}

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, **kwargs):
        """Initialize Matusita instance.

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
        super(Matusita, self).__init__(tokenizer=tokenizer, **kwargs)

    def dist_abs(self, src, tar):
        """Return the Matusita distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Matusita distance

        Examples
        --------
        >>> cmp = Matusita()
        >>> cmp.dist_abs('cat', 'hat')
        1.0
        >>> cmp.dist_abs('Niall', 'Neil')
        1.126811100699571
        >>> cmp.dist_abs('aluminum', 'Catalan')
        1.3282687000770907
        >>> cmp.dist_abs('ATCG', 'TAGC')
        1.414213562373095


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        alphabet = self._total().keys()

        src_card = self._src_card()
        if src_card == 0:
            src_card = 1.0
        tar_card = self._tar_card()
        if tar_card == 0:
            tar_card = 1.0

        return (
            sum(
                (
                    (abs(self._src_tokens[tok]) / src_card) ** 0.5
                    - (abs(self._tar_tokens[tok]) / tar_card) ** 0.5
                )
                ** 2
                for tok in alphabet
            )
        ) ** 0.5

    def dist(self, src, tar):
        """Return the normalized Matusita distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Normalized Matusita distance

        Examples
        --------
        >>> cmp = Matusita()
        >>> cmp.dist('cat', 'hat')
        0.707106781186547
        >>> cmp.dist('Niall', 'Neil')
        0.796775770420944
        >>> cmp.dist('aluminum', 'Catalan')
        0.939227805062351
        >>> cmp.dist('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0

        return round(self.dist_abs(src, tar) / 2 ** 0.5, 15)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
