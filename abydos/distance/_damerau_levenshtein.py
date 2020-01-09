# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.distance._damerau_levenshtein.

Damerau-Levenshtein distance
"""

from sys import maxsize

from deprecation import deprecated

from numpy import int as np_int
from numpy import zeros as np_zeros

from ._distance import _Distance
from .. import __version__

__all__ = [
    'DamerauLevenshtein',
    'damerau_levenshtein',
    'dist_damerau',
    'sim_damerau',
]


class DamerauLevenshtein(_Distance):
    """Damerau-Levenshtein distance.

    This computes the Damerau-Levenshtein distance :cite:`Damerau:1964`.
    Damerau-Levenshtein code is based on Java code by Kevin L. Stern
    :cite:`Stern:2014`, under the MIT license:
    https://github.com/KevinStern/software-and-algorithms/blob/master/src/main/java/blogspot/software_and_algorithms/stern_library/string/DamerauLevenshteinAlgorithm.java
    """

    def __init__(self, cost=(1, 1, 1, 1), normalizer=max, **kwargs):
        """Initialize Levenshtein instance.

        Parameters
        ----------
        cost : tuple
            A 4-tuple representing the cost of the four possible edits:
            inserts, deletes, substitutions, and transpositions, respectively
            (by default: (1, 1, 1, 1))
        normalizer : function
            A function that takes an list and computes a normalization term
            by which the edit distance is divided (max by default). Another
            good option is the sum function.
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(DamerauLevenshtein, self).__init__(**kwargs)
        self._cost = cost
        self._normalizer = normalizer

    def dist_abs(self, src, tar):
        """Return the Damerau-Levenshtein distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int (may return a float if cost has float values)
            The Damerau-Levenshtein distance between src & tar

        Raises
        ------
        ValueError
            Unsupported cost assignment; the cost of two transpositions must
            not be less than the cost of an insert plus a delete.

        Examples
        --------
        >>> cmp = DamerauLevenshtein()
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        3
        >>> cmp.dist_abs('aluminum', 'Catalan')
        7
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        ins_cost, del_cost, sub_cost, trans_cost = self._cost

        if src == tar:
            return 0
        if not src:
            return len(tar) * ins_cost
        if not tar:
            return len(src) * del_cost

        if 2 * trans_cost < ins_cost + del_cost:
            raise ValueError(
                'Unsupported cost assignment; the cost of two transpositions '
                + 'must not be less than the cost of an insert plus a delete.'
            )

        d_mat = np_zeros((len(src), len(tar)), dtype=np_int)

        if src[0] != tar[0]:
            d_mat[0, 0] = min(sub_cost, ins_cost + del_cost)

        src_index_by_character = {src[0]: 0}
        for i in range(1, len(src)):
            del_distance = d_mat[i - 1, 0] + del_cost
            ins_distance = (i + 1) * del_cost + ins_cost
            match_distance = i * del_cost + (
                0 if src[i] == tar[0] else sub_cost
            )
            d_mat[i, 0] = min(del_distance, ins_distance, match_distance)

        for j in range(1, len(tar)):
            del_distance = (j + 1) * ins_cost + del_cost
            ins_distance = d_mat[0, j - 1] + ins_cost
            match_distance = j * ins_cost + (
                0 if src[0] == tar[j] else sub_cost
            )
            d_mat[0, j] = min(del_distance, ins_distance, match_distance)

        for i in range(1, len(src)):
            max_src_letter_match_index = 0 if src[i] == tar[0] else -1
            for j in range(1, len(tar)):
                candidate_swap_index = (
                    -1
                    if tar[j] not in src_index_by_character
                    else src_index_by_character[tar[j]]
                )
                j_swap = max_src_letter_match_index
                del_distance = d_mat[i - 1, j] + del_cost
                ins_distance = d_mat[i, j - 1] + ins_cost
                match_distance = d_mat[i - 1, j - 1]
                if src[i] != tar[j]:
                    match_distance += sub_cost
                else:
                    max_src_letter_match_index = j

                if candidate_swap_index != -1 and j_swap != -1:
                    i_swap = candidate_swap_index

                    if i_swap == 0 and j_swap == 0:
                        pre_swap_cost = 0
                    else:
                        pre_swap_cost = d_mat[
                            max(0, i_swap - 1), max(0, j_swap - 1)
                        ]
                    swap_distance = (
                        pre_swap_cost
                        + (i - i_swap - 1) * del_cost
                        + (j - j_swap - 1) * ins_cost
                        + trans_cost
                    )
                else:
                    swap_distance = maxsize

                d_mat[i, j] = min(
                    del_distance, ins_distance, match_distance, swap_distance
                )
            src_index_by_character[src[i]] = i

        return d_mat[len(src) - 1, len(tar) - 1]

    def dist(self, src, tar):
        """Return the Damerau-Levenshtein similarity of two strings.

        Damerau-Levenshtein distance normalized to the interval [0, 1].

        The Damerau-Levenshtein distance is normalized by dividing the
        Damerau-Levenshtein distance by the greater of
        the number of characters in src times the cost of a delete and
        the number of characters in tar times the cost of an insert.
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
            The normalized Damerau-Levenshtein distance

        Examples
        --------
        >>> cmp = DamerauLevenshtein()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.333333333333
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.6
        >>> cmp.dist('aluminum', 'Catalan')
        0.875
        >>> cmp.dist('ATCG', 'TAGC')
        0.5


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if src == tar:
            return 0.0
        ins_cost, del_cost = self._cost[:2]
        return self.dist_abs(src, tar) / (
            self._normalizer([len(src) * del_cost, len(tar) * ins_cost])
        )


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the DamerauLevenshtein.dist_abs method instead.',
)
def damerau_levenshtein(src, tar, cost=(1, 1, 1, 1)):
    """Return the Damerau-Levenshtein distance between two strings.

    This is a wrapper of :py:meth:`DamerauLevenshtein.dist_abs`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    cost : tuple
        A 4-tuple representing the cost of the four possible edits: inserts,
        deletes, substitutions, and transpositions, respectively (by default:
        (1, 1, 1, 1))

    Returns
    -------
    int (may return a float if cost has float values)
        The Damerau-Levenshtein distance between src & tar

    Examples
    --------
    >>> damerau_levenshtein('cat', 'hat')
    1
    >>> damerau_levenshtein('Niall', 'Neil')
    3
    >>> damerau_levenshtein('aluminum', 'Catalan')
    7
    >>> damerau_levenshtein('ATCG', 'TAGC')
    2

    .. versionadded:: 0.1.0

    """
    return DamerauLevenshtein(cost).dist_abs(src, tar)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the DamerauLevenshtein.dist method instead.',
)
def dist_damerau(src, tar, cost=(1, 1, 1, 1)):
    """Return the Damerau-Levenshtein similarity of two strings.

    This is a wrapper of :py:meth:`DamerauLevenshtein.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    cost : tuple
        A 4-tuple representing the cost of the four possible edits: inserts,
        deletes, substitutions, and transpositions, respectively (by default:
        (1, 1, 1, 1))

    Returns
    -------
    float
        The normalized Damerau-Levenshtein distance

    Examples
    --------
    >>> round(dist_damerau('cat', 'hat'), 12)
    0.333333333333
    >>> round(dist_damerau('Niall', 'Neil'), 12)
    0.6
    >>> dist_damerau('aluminum', 'Catalan')
    0.875
    >>> dist_damerau('ATCG', 'TAGC')
    0.5

    .. versionadded:: 0.1.0

    """
    return DamerauLevenshtein(cost).dist(src, tar)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the DamerauLevenshtein.sim method instead.',
)
def sim_damerau(src, tar, cost=(1, 1, 1, 1)):
    """Return the Damerau-Levenshtein similarity of two strings.

    This is a wrapper of :py:meth:`DamerauLevenshtein.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    cost : tuple
        A 4-tuple representing the cost of the four possible edits: inserts,
        deletes, substitutions, and transpositions, respectively (by default:
        (1, 1, 1, 1))

    Returns
    -------
    float
        The normalized Damerau-Levenshtein similarity

    Examples
    --------
    >>> round(sim_damerau('cat', 'hat'), 12)
    0.666666666667
    >>> round(sim_damerau('Niall', 'Neil'), 12)
    0.4
    >>> sim_damerau('aluminum', 'Catalan')
    0.125
    >>> sim_damerau('ATCG', 'TAGC')
    0.5

    .. versionadded:: 0.1.0

    """
    return DamerauLevenshtein(cost).sim(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
