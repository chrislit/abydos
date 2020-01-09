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

"""abydos.distance._phonetic_edit_distance.

Phonetic edit distance
"""

import numpy as np

from ._levenshtein import Levenshtein
from ..phones._phones import _FEATURE_MASK, cmp_features, ipa_to_features

__all__ = ['PhoneticEditDistance']


class PhoneticEditDistance(Levenshtein):
    """Phonetic edit distance.

    This is a variation on Levenshtein edit distance, intended for strings in
    IPA, that compares individual phones based on their featural similarity.

    .. versionadded:: 0.4.1
    """

    def __init__(
        self,
        mode='lev',
        cost=(1, 1, 1, 0.33333),
        normalizer=max,
        weights=None,
        **kwargs
    ):
        """Initialize PhoneticEditDistance instance.

        Parameters
        ----------
        mode : str
            Specifies a mode for computing the edit distance:

                - ``lev`` (default) computes the ordinary Levenshtein distance,
                  in which edits may include inserts, deletes, and
                  substitutions
                - ``osa`` computes the Optimal String Alignment distance, in
                  which edits may include inserts, deletes, substitutions, and
                  transpositions but substrings may only be edited once

        cost : tuple
            A 4-tuple representing the cost of the four possible edits:
            inserts, deletes, substitutions, and transpositions, respectively
            (by default: (1, 1, 1, 0.33333)). Note that transpositions cost a
            relatively low 0.33333. If this were 1.0, no phones would ever be
            transposed under the normal weighting, since even quite dissimilar
            phones such as [a] and [p] still agree in nearly 63% of their
            features.
        normalizer : function
            A function that takes an list and computes a normalization term
            by which the edit distance is divided (max by default). Another
            good option is the sum function.
        weights : None or list or tuple or dict
            If None, all features are of equal significance and a simple
            normalized hamming distance of the features is calculated. If a
            list or tuple of numeric values is supplied, the values are
            inferred as the weights for each feature, in order of the features
            listed in abydos.phones._phones._FEATURE_MASK. If a dict is
            supplied, its key values should match keys in
            abydos.phones._phones._FEATURE_MASK to which each weight (value)
            should be assigned. Missing values in all cases are assigned a
            weight of 0 and will be omitted from the comparison.
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.1

        """
        super(PhoneticEditDistance, self).__init__(**kwargs)
        self._mode = mode
        self._cost = cost
        self._normalizer = normalizer

        if isinstance(weights, dict):
            weights = [
                weights[feature] if feature in weights else 0
                for feature in sorted(
                    _FEATURE_MASK, key=_FEATURE_MASK.get, reverse=True
                )
            ]
        elif isinstance(weights, (list, tuple)):
            weights = list(weights) + [0] * (len(_FEATURE_MASK) - len(weights))
        self._weights = weights

    def _alignment_matrix(self, src, tar, backtrace=True):
        """Return the phonetic edit distance alignment matrix.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        backtrace : bool
            Return the backtrace matrix as well

        Returns
        -------
        numpy.ndarray or tuple(numpy.ndarray, numpy.ndarray)
            The alignment matrix and (optionally) the backtrace matrix


        .. versionadded:: 0.4.1

        """
        ins_cost, del_cost, sub_cost, trans_cost = self._cost

        src_len = len(src)
        tar_len = len(tar)

        src = ipa_to_features(src)
        tar = ipa_to_features(tar)

        d_mat = np.zeros((src_len + 1, tar_len + 1), dtype=np.float)
        if backtrace:
            trace_mat = np.zeros((src_len + 1, tar_len + 1), dtype=np.int8)
        for i in range(1, src_len + 1):
            d_mat[i, 0] = i * del_cost
            if backtrace:
                trace_mat[i, 0] = 0
        for j in range(1, tar_len + 1):
            d_mat[0, j] = j * ins_cost
            if backtrace:
                trace_mat[0, j] = 1

        for i in range(src_len):
            for j in range(tar_len):
                traces = ((i + 1, j), (i, j + 1), (i, j))
                opts = (
                    d_mat[traces[0]] + ins_cost,  # ins
                    d_mat[traces[1]] + del_cost,  # del
                    d_mat[traces[2]]
                    + (
                        sub_cost
                        * (1.0 - cmp_features(src[i], tar[j], self._weights))
                        if src[i] != tar[j]
                        else 0
                    ),  # sub/==
                )
                d_mat[i + 1, j + 1] = min(opts)
                if backtrace:
                    trace_mat[i + 1, j + 1] = int(np.argmin(opts))

                if self._mode == 'osa':
                    if (
                        i + 1 > 1
                        and j + 1 > 1
                        and src[i] == tar[j - 1]
                        and src[i - 1] == tar[j]
                    ):
                        # transposition
                        d_mat[i + 1, j + 1] = min(
                            d_mat[i + 1, j + 1],
                            d_mat[i - 1, j - 1] + trans_cost,
                        )
                        if backtrace:
                            trace_mat[i + 1, j + 1] = 2
        if backtrace:
            return d_mat, trace_mat
        return d_mat

    def dist_abs(self, src, tar):
        """Return the phonetic edit distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int (may return a float if cost has float values)
            The phonetic edit distance between src & tar

        Examples
        --------
        >>> cmp = PhoneticEditDistance()
        >>> cmp.dist_abs('cat', 'hat')
        0.17741935483870974
        >>> cmp.dist_abs('Niall', 'Neil')
        1.161290322580645
        >>> cmp.dist_abs('aluminum', 'Catalan')
        2.467741935483871
        >>> cmp.dist_abs('ATCG', 'TAGC')
        1.193548387096774

        >>> cmp = PhoneticEditDistance(mode='osa')
        >>> cmp.dist_abs('ATCG', 'TAGC')
        0.46236225806451603
        >>> cmp.dist_abs('ACTG', 'TAGC')
        1.2580645161290323


        .. versionadded:: 0.4.1

        """
        ins_cost, del_cost, sub_cost, trans_cost = self._cost

        src_len = len(src)
        tar_len = len(tar)

        if src == tar:
            return 0
        if not src:
            return ins_cost * tar_len
        if not tar:
            return del_cost * src_len

        d_mat = self._alignment_matrix(src, tar, backtrace=False)

        if int(d_mat[src_len, tar_len]) == d_mat[src_len, tar_len]:
            return int(d_mat[src_len, tar_len])
        else:
            return d_mat[src_len, tar_len]

    def dist(self, src, tar):
        """Return the normalized phonetic edit distance between two strings.

        The edit distance is normalized by dividing the edit distance
        (calculated by either of the two supported methods) by the
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
        >>> cmp = PhoneticEditDistance()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.059139784946
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.232258064516
        >>> cmp.dist('aluminum', 'Catalan')
        0.3084677419354839
        >>> cmp.dist('ATCG', 'TAGC')
        0.2983870967741935


        .. versionadded:: 0.4.1

        """
        if src == tar:
            return 0.0
        ins_cost, del_cost = self._cost[:2]

        src_len = len(src)
        tar_len = len(tar)

        normalize_term = self._normalizer(
            [src_len * del_cost, tar_len * ins_cost]
        )

        return self.dist_abs(src, tar) / normalize_term


if __name__ == '__main__':
    import doctest

    doctest.testmod()
