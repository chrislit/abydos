# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.distance._discounted_levenshtein.

Discounted Levenshtein edit distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from math import log

from numpy import float as np_float
from numpy import zeros as np_zeros

from six.moves import range

from ._distance import _Distance

__all__ = ['DiscountedLevenshtein']


class DiscountedLevenshtein(_Distance):
    """Discounted Levenshtein distance.

    This is a variant of Levenshtein distance for which edits later in a string
    have discounted cost, on the theory that earlier edits are less likely
    than later ones.

    .. versionadded:: 0.4.1
    """

    def __init__(
        self,
        mode='lev',
        normalizer=max,
        discount_from=1,
        discount_func='log',
        vowels='aeiou',
        **kwargs
    ):
        """Initialize DiscountedLevenshtein instance.

        Parameters
        ----------
        mode : str
            Specifies a mode for computing the discounted Levenshtein distance:

                - ``lev`` (default) computes the ordinary Levenshtein distance,
                  in which edits may include inserts, deletes, and
                  substitutions
                - ``osa`` computes the Optimal String Alignment distance, in
                  which edits may include inserts, deletes, substitutions, and
                  transpositions but substrings may only be edited once

        normalizer : function
            A function that takes an list and computes a normalization term
            by which the edit distance is divided (max by default). Another
            good option is the sum function.
        discount_from : int or str
            If an int is supplied, this is the first character whose edit cost
            will be discounted. If the str ``vowels`` is supplied, discounting
            will start with the first non-vowel after the first vowel (the
            first syllable coda).
        discount_func : str or function
            The two supported str arguments are ``log``, for a logarithmic
            discount function, and ``exp`` for a exponential discount function.
            See notes below for information on how to supply your own
            discount function.
        vowels : str
            These are the letters to consider as vowels when discount_from is
            set to ``vowels``. It defaults to the English vowels 'aeiou', but
            it would be reasonable to localize this to other languages or to
            add orthographic semi-vowels like 'y', 'w', and even 'h'.
        **kwargs
            Arbitrary keyword arguments

        Notes
        -----
        This class is highly experimental and will need additional tuning.

        The discount function can be passed as a callable function. It should
        expect an integer as its only argument and return a float, ideally
        less than or equal to 1.0. The argument represents the degree of
        discounting to apply.


        .. versionadded:: 0.4.1

        """
        super(DiscountedLevenshtein, self).__init__(**kwargs)
        self._mode = mode
        self._normalizer = normalizer
        self._discount_from = discount_from
        self._vowels = set(vowels.lower())
        if callable(discount_func):
            self._cost = discount_func
        elif discount_func == 'exp':
            self._cost = self._exp_discount
        else:
            self._cost = self._log_discount

    @staticmethod
    def _log_discount(discounts):
        return 1 / (log(1 + discounts / 5) + 1)

    @staticmethod
    def _exp_discount(discounts):
        return 1 / (discounts + 1) ** 0.2

    def _alignment_matrix(self, src, tar):
        """Return the Levenshtein alignment matrix.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        numpy.ndarray
            The alignment matrix


        .. versionadded:: 0.4.1

        """
        src_len = len(src)
        tar_len = len(tar)

        if self._discount_from == 'vowels':
            discount_from = [0, 0]

            src_voc = src.lower()
            for i in range(len(src_voc)):
                if src_voc[i] in self._vowels:
                    discount_from[0] = i
                    break
            for i in range(discount_from[0], len(src_voc)):
                if src_voc[i] not in self._vowels:
                    discount_from[0] = i
                    break
            else:
                discount_from[0] += 1

            tar_voc = tar.lower()
            for i in range(len(tar_voc)):
                if tar_voc[i] in self._vowels:
                    discount_from[1] = i
                    break
            for i in range(discount_from[1], len(tar_voc)):
                if tar_voc[i] not in self._vowels:
                    discount_from[1] = i
                    break
            else:
                discount_from[1] += 1

        elif isinstance(self._discount_from, int):
            discount_from = [self._discount_from, self._discount_from]
        else:
            discount_from = [1, 1]

        d_mat = np_zeros((src_len + 1, tar_len + 1), dtype=np_float)
        for i in range(1, src_len + 1):
            d_mat[i, 0] = d_mat[i - 1, 0] + self._cost(
                max(0, i - discount_from[0])
            )
        for j in range(1, tar_len + 1):
            d_mat[0, j] = d_mat[0, j - 1] + self._cost(
                max(0, j - discount_from[1])
            )

        for i in range(src_len):
            i_extend = self._cost(max(0, i - discount_from[0]))
            for j in range(tar_len):
                cost = min(i_extend, self._cost(max(0, j - discount_from[1])))
                d_mat[i + 1, j + 1] = min(
                    d_mat[i + 1, j] + cost,  # ins
                    d_mat[i, j + 1] + cost,  # del
                    d_mat[i, j] + (cost if src[i] != tar[j] else 0),  # sub/==
                )

                if self._mode == 'osa':
                    if (
                        i + 1 > 1
                        and j + 1 > 1
                        and src[i] == tar[j - 1]
                        and src[i - 1] == tar[j]
                    ):
                        # transposition
                        d_mat[i + 1, j + 1] = min(
                            d_mat[i + 1, j + 1], d_mat[i - 1, j - 1] + cost
                        )

        return d_mat

    def alignment(self, src, tar):
        """Return the Levenshtein alignment of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        tuple
            A tuple containing the Levenshtein distance and the two strings,
            aligned.

        Examples
        --------
        >>> cmp = DiscountedLevenshtein()
        >>> cmp.alignment('cat', 'hat')
        (1.0, 'cat', 'hat')
        >>> cmp.alignment('Niall', 'Neil')
        (2.526064024369237, 'N-iall', 'Neil--')
        >>> cmp.alignment('aluminum', 'Catalan')
        (5.053867269967515, '-aluminum', 'Catalan--')
        >>> cmp.alignment('ATCG', 'TAGC')
        (2.594032108779918, 'ATCG-', '-TAGC')

        >>> cmp = DiscountedLevenshtein(mode='osa')
        >>> cmp.alignment('ATCG', 'TAGC')
        (1.7482385137517997, 'ATCG', 'TAGC')
        >>> cmp.alignment('ACTG', 'TAGC')
        (3.342270622531718, '-ACTG', 'TAGC-')


        .. versionadded:: 0.4.1

        """
        d_mat = self._alignment_matrix(src, tar)

        src_aligned = []
        tar_aligned = []

        src_pos = len(src)
        tar_pos = len(tar)

        distance = d_mat[src_pos, tar_pos]

        while src_pos and tar_pos:
            up = d_mat[src_pos, tar_pos - 1]
            left = d_mat[src_pos - 1, tar_pos]
            diag = d_mat[src_pos - 1, tar_pos - 1]

            if diag <= min(up, left):
                src_pos -= 1
                tar_pos -= 1
                src_aligned.append(src[src_pos])
                tar_aligned.append(tar[tar_pos])
            elif up <= left:
                tar_pos -= 1
                src_aligned.append('-')
                tar_aligned.append(tar[tar_pos])
            else:
                src_pos -= 1
                src_aligned.append(src[src_pos])
                tar_aligned.append('-')
        while tar_pos:
            tar_pos -= 1
            tar_aligned.append(tar[tar_pos])
            src_aligned.append('-')
        while src_pos:
            src_pos -= 1
            src_aligned.append(src[src_pos])
            tar_aligned.append('-')

        return distance, ''.join(src_aligned[::-1]), ''.join(tar_aligned[::-1])

    def dist_abs(self, src, tar):
        """Return the Levenshtein distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int (may return a float if cost has float values)
            The Levenshtein distance between src & tar

        Examples
        --------
        >>> cmp = DiscountedLevenshtein()
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        2.526064024369237
        >>> cmp.dist_abs('aluminum', 'Catalan')
        5.053867269967515
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2.594032108779918

        >>> cmp = DiscountedLevenshtein(mode='osa')
        >>> cmp.dist_abs('ATCG', 'TAGC')
        1.7482385137517997
        >>> cmp.dist_abs('ACTG', 'TAGC')
        3.342270622531718


        .. versionadded:: 0.4.1

        """
        src_len = len(src)
        tar_len = len(tar)

        if src == tar:
            return 0

        if isinstance(self._discount_from, int):
            discount_from = self._discount_from
        else:
            discount_from = 1

        if not src:
            return sum(
                self._cost(max(0, pos - discount_from))
                for pos in range(tar_len)
            )
        if not tar:
            return sum(
                self._cost(max(0, pos - discount_from))
                for pos in range(src_len)
            )

        d_mat = self._alignment_matrix(src, tar)

        if int(d_mat[src_len, tar_len]) == d_mat[src_len, tar_len]:
            return int(d_mat[src_len, tar_len])
        else:
            return d_mat[src_len, tar_len]

    def dist(self, src, tar):
        """Return the normalized Levenshtein distance between two strings.

        The Levenshtein distance is normalized by dividing the Levenshtein
        distance (calculated by any of the three supported methods) by the
        greater of the number of characters in src times the cost of a delete
        and the number of characters in tar times the cost of an insert.
        For the case in which all operations have :math:`cost = 1`, this is
        equivalent to the greater of the length of the two strings src & tar.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The normalized Levenshtein distance between src & tar

        Examples
        --------
        >>> cmp = DiscountedLevenshtein()
        >>> cmp.dist('cat', 'hat')
        0.3513958291799864
        >>> cmp.dist('Niall', 'Neil')
        0.5909885886270658
        >>> cmp.dist('aluminum', 'Catalan')
        0.8348163322045603
        >>> cmp.dist('ATCG', 'TAGC')
        0.7217609721523955


        .. versionadded:: 0.4.1

        """
        if src == tar:
            return 0

        if isinstance(self._discount_from, int):
            discount_from = self._discount_from
        else:
            discount_from = 1

        src_len = len(src)
        tar_len = len(tar)

        normalize_term = self._normalizer(
            [
                sum(
                    self._cost(max(0, pos - discount_from))
                    for pos in range(src_len)
                ),
                sum(
                    self._cost(max(0, pos - discount_from))
                    for pos in range(tar_len)
                ),
            ]
        )

        return self.dist_abs(src, tar) / normalize_term


if __name__ == '__main__':
    import doctest

    doctest.testmod()
