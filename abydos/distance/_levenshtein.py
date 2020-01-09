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

"""abydos.distance._levenshtein.

The distance._Levenshtein module implements string edit distance functions
based on Levenshtein distance, including:

    - Levenshtein distance
    - Optimal String Alignment distance
"""

from sys import float_info

from deprecation import deprecated

import numpy as np

from ._distance import _Distance
from .. import __version__

__all__ = ['Levenshtein', 'dist_levenshtein', 'levenshtein', 'sim_levenshtein']


class Levenshtein(_Distance):
    """Levenshtein distance.

    This is the standard edit distance measure. Cf.
    :cite:`Levenshtein:1965,Levenshtein:1966`.

    Optimal string alignment (aka restricted
    Damerau-Levenshtein distance) :cite:`Boytsov:2011` is also supported.

    The ordinary Levenshtein & Optimal String Alignment distance both
    employ the Wagner-Fischer dynamic programming algorithm
    :cite:`Wagner:1974`.

    Levenshtein edit distance ordinarily has unit insertion, deletion, and
    substitution costs.

    .. versionadded:: 0.3.6
    .. versionchanged:: 0.4.0
        Added taper option
    """

    def __init__(
        self,
        mode='lev',
        cost=(1, 1, 1, 1),
        normalizer=max,
        taper=False,
        **kwargs
    ):
        """Initialize Levenshtein instance.

        Parameters
        ----------
        mode : str
            Specifies a mode for computing the Levenshtein distance:

                - ``lev`` (default) computes the ordinary Levenshtein distance,
                  in which edits may include inserts, deletes, and
                  substitutions
                - ``osa`` computes the Optimal String Alignment distance, in
                  which edits may include inserts, deletes, substitutions, and
                  transpositions but substrings may only be edited once

        cost : tuple
            A 4-tuple representing the cost of the four possible edits:
            inserts, deletes, substitutions, and transpositions, respectively
            (by default: (1, 1, 1, 1))
        normalizer : function
            A function that takes an list and computes a normalization term
            by which the edit distance is divided (max by default). Another
            good option is the sum function.
        taper : bool
            Enables cost tapering. Following :cite:`Zobel:1996`, it causes
            edits at the start of the string to "just [exceed] twice the
            minimum penalty for replacement or deletion at the end of the
            string".
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(Levenshtein, self).__init__(**kwargs)
        self._mode = mode
        self._cost = cost
        self._normalizer = normalizer
        self._taper_enabled = taper

    def _taper(self, pos, length):
        return (
            round(1 + ((length - pos) / length) * (1 + float_info.epsilon), 15)
            if self._taper_enabled
            else 1
        )

    def _alignment_matrix(self, src, tar, backtrace=True):
        """Return the Levenshtein alignment matrix.

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
        max_len = max(src_len, tar_len)

        d_mat = np.zeros((src_len + 1, tar_len + 1), dtype=np.float)
        if backtrace:
            trace_mat = np.zeros((src_len + 1, tar_len + 1), dtype=np.int8)
        for i in range(src_len + 1):
            d_mat[i, 0] = i * self._taper(i, max_len) * del_cost
            if backtrace:
                trace_mat[i, 0] = 1
        for j in range(tar_len + 1):
            d_mat[0, j] = j * self._taper(j, max_len) * ins_cost
            if backtrace:
                trace_mat[0, j] = 0

        for i in range(src_len):
            for j in range(tar_len):
                opts = (
                    d_mat[i + 1, j]
                    + ins_cost * self._taper(1 + max(i, j), max_len),  # ins
                    d_mat[i, j + 1]
                    + del_cost * self._taper(1 + max(i, j), max_len),  # del
                    d_mat[i, j]
                    + (
                        sub_cost * self._taper(1 + max(i, j), max_len)
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
                            d_mat[i - 1, j - 1]
                            + trans_cost * self._taper(1 + max(i, j), max_len),
                        )
                        if backtrace:
                            trace_mat[i + 1, j + 1] = 2

        if backtrace:
            return d_mat, trace_mat
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
        >>> cmp = Levenshtein()
        >>> cmp.alignment('cat', 'hat')
        (1.0, 'cat', 'hat')
        >>> cmp.alignment('Niall', 'Neil')
        (3.0, 'N-iall', 'Nei-l-')
        >>> cmp.alignment('aluminum', 'Catalan')
        (7.0, '-aluminum', 'Catalan--')
        >>> cmp.alignment('ATCG', 'TAGC')
        (3.0, 'ATCG-', '-TAGC')

        >>> cmp = Levenshtein(mode='osa')
        >>> cmp.alignment('ATCG', 'TAGC')
        (2.0, 'ATCG', 'TAGC')
        >>> cmp.alignment('ACTG', 'TAGC')
        (4.0, 'ACT-G-', '--TAGC')


        .. versionadded:: 0.4.1

        """
        d_mat, trace_mat = self._alignment_matrix(src, tar, backtrace=True)

        src_aligned = []
        tar_aligned = []

        src_pos = len(src)
        tar_pos = len(tar)

        distance = d_mat[src_pos, tar_pos]

        while src_pos and tar_pos:

            src_trace, tar_trace = (
                (src_pos, tar_pos - 1),
                (src_pos - 1, tar_pos),
                (src_pos - 1, tar_pos - 1),
            )[trace_mat[src_pos, tar_pos]]

            if src_pos != src_trace and tar_pos != tar_trace:
                src_aligned.append(src[src_trace])
                tar_aligned.append(tar[tar_trace])
            elif src_pos != src_trace:
                src_aligned.append(src[src_trace])
                tar_aligned.append('-')
            else:
                src_aligned.append('-')
                tar_aligned.append(tar[tar_trace])
            src_pos, tar_pos = src_trace, tar_trace
        while tar_pos:
            tar_pos -= 1
            src_aligned.append('-')
            tar_aligned.append(tar[tar_pos])
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
        >>> cmp = Levenshtein()
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        3
        >>> cmp.dist_abs('aluminum', 'Catalan')
        7
        >>> cmp.dist_abs('ATCG', 'TAGC')
        3

        >>> cmp = Levenshtein(mode='osa')
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2
        >>> cmp.dist_abs('ACTG', 'TAGC')
        4


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        ins_cost, del_cost, sub_cost, trans_cost = self._cost

        src_len = len(src)
        tar_len = len(tar)
        max_len = max(src_len, tar_len)

        if src == tar:
            return 0
        if not src:
            return sum(
                ins_cost * self._taper(pos, max_len) for pos in range(tar_len)
            )
        if not tar:
            return sum(
                del_cost * self._taper(pos, max_len) for pos in range(src_len)
            )

        d_mat = self._alignment_matrix(src, tar, backtrace=False)

        if int(d_mat[src_len, tar_len]) == d_mat[src_len, tar_len]:
            return int(d_mat[src_len, tar_len])
        else:
            return d_mat[src_len, tar_len]

    def dist(self, src, tar):
        """Return the normalized Levenshtein distance between two strings.

        The Levenshtein distance is normalized by dividing the Levenshtein
        distance (calculated by either of the two supported methods) by the
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
        >>> cmp = Levenshtein()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.333333333333
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.6
        >>> cmp.dist('aluminum', 'Catalan')
        0.875
        >>> cmp.dist('ATCG', 'TAGC')
        0.75


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if src == tar:
            return 0.0
        ins_cost, del_cost = self._cost[:2]

        src_len = len(src)
        tar_len = len(tar)

        if self._taper_enabled:
            normalize_term = self._normalizer(
                [
                    sum(
                        self._taper(pos, src_len) * del_cost
                        for pos in range(src_len)
                    ),
                    sum(
                        self._taper(pos, tar_len) * ins_cost
                        for pos in range(tar_len)
                    ),
                ]
            )
        else:
            normalize_term = self._normalizer(
                [src_len * del_cost, tar_len * ins_cost]
            )

        return self.dist_abs(src, tar) / normalize_term


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Levenshtein.dist_abs method instead.',
)
def levenshtein(src, tar, mode='lev', cost=(1, 1, 1, 1)):
    """Return the Levenshtein distance between two strings.

    This is a wrapper of :py:meth:`Levenshtein.dist_abs`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    mode : str
        Specifies a mode for computing the Levenshtein distance:

            - ``lev`` (default) computes the ordinary Levenshtein distance, in
              which edits may include inserts, deletes, and substitutions
            - ``osa`` computes the Optimal String Alignment distance, in which
              edits may include inserts, deletes, substitutions, and
              transpositions but substrings may only be edited once

    cost : tuple
        A 4-tuple representing the cost of the four possible edits: inserts,
        deletes, substitutions, and transpositions, respectively (by default:
        (1, 1, 1, 1))

    Returns
    -------
    int (may return a float if cost has float values)
        The Levenshtein distance between src & tar

    Examples
    --------
    >>> levenshtein('cat', 'hat')
    1
    >>> levenshtein('Niall', 'Neil')
    3
    >>> levenshtein('aluminum', 'Catalan')
    7
    >>> levenshtein('ATCG', 'TAGC')
    3

    >>> levenshtein('ATCG', 'TAGC', mode='osa')
    2
    >>> levenshtein('ACTG', 'TAGC', mode='osa')
    4

    .. versionadded:: 0.1.0

    """
    return Levenshtein(mode=mode, cost=cost).dist_abs(src, tar)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Levenshtein.dist method instead.',
)
def dist_levenshtein(src, tar, mode='lev', cost=(1, 1, 1, 1)):
    """Return the normalized Levenshtein distance between two strings.

    This is a wrapper of :py:meth:`Levenshtein.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    mode : str
        Specifies a mode for computing the Levenshtein distance:

            - ``lev`` (default) computes the ordinary Levenshtein distance, in
              which edits may include inserts, deletes, and substitutions
            - ``osa`` computes the Optimal String Alignment distance, in which
              edits may include inserts, deletes, substitutions, and
              transpositions but substrings may only be edited once

    cost : tuple
        A 4-tuple representing the cost of the four possible edits: inserts,
        deletes, substitutions, and transpositions, respectively (by default:
        (1, 1, 1, 1))

    Returns
    -------
    float
        The Levenshtein distance between src & tar

    Examples
    --------
    >>> round(dist_levenshtein('cat', 'hat'), 12)
    0.333333333333
    >>> round(dist_levenshtein('Niall', 'Neil'), 12)
    0.6
    >>> dist_levenshtein('aluminum', 'Catalan')
    0.875
    >>> dist_levenshtein('ATCG', 'TAGC')
    0.75

    .. versionadded:: 0.1.0

    """
    return Levenshtein(mode=mode, cost=cost).dist(src, tar)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Levenshtein.sim method instead.',
)
def sim_levenshtein(src, tar, mode='lev', cost=(1, 1, 1, 1)):
    """Return the Levenshtein similarity of two strings.

    This is a wrapper of :py:meth:`Levenshtein.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    mode : str
        Specifies a mode for computing the Levenshtein distance:

            - ``lev`` (default) computes the ordinary Levenshtein distance, in
              which edits may include inserts, deletes, and substitutions
            - ``osa`` computes the Optimal String Alignment distance, in which
              edits may include inserts, deletes, substitutions, and
              transpositions but substrings may only be edited once

    cost : tuple
        A 4-tuple representing the cost of the four possible edits: inserts,
        deletes, substitutions, and transpositions, respectively (by default:
        (1, 1, 1, 1))

    Returns
    -------
    float
        The Levenshtein similarity between src & tar

    Examples
    --------
    >>> round(sim_levenshtein('cat', 'hat'), 12)
    0.666666666667
    >>> round(sim_levenshtein('Niall', 'Neil'), 12)
    0.4
    >>> sim_levenshtein('aluminum', 'Catalan')
    0.125
    >>> sim_levenshtein('ATCG', 'TAGC')
    0.25

    .. versionadded:: 0.1.0

    """
    return Levenshtein(mode=mode, cost=cost).sim(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
