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

"""abydos.distance._gotoh.

Gotoh score
"""

from deprecation import deprecated

from numpy import float32 as np_float32
from numpy import zeros as np_zeros

from ._ident import sim_ident
from ._needleman_wunsch import NeedlemanWunsch
from .. import __version__

__all__ = ['Gotoh', 'gotoh']


class Gotoh(NeedlemanWunsch):
    """Gotoh score.

    The Gotoh score :cite:`Gotoh:1982` is essentially Needleman-Wunsch with
    affine gap penalties.

    .. versionadded:: 0.3.6
    """

    def __init__(self, gap_open=1, gap_ext=0.4, sim_func=None, **kwargs):
        """Initialize Gotoh instance.

        Parameters
        ----------
        gap_open : float
            The cost of an open alignment gap (1 by default)
        gap_ext : float
            The cost of an alignment gap extension (0.4 by default)
        sim_func : function
            A function that returns the similarity of two characters (identity
            similarity by default)
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(Gotoh, self).__init__(**kwargs)
        self._gap_open = gap_open
        self._gap_ext = gap_ext
        self._sim_func = sim_func
        if self._sim_func is None:
            self._sim_func = NeedlemanWunsch.sim_matrix

    def sim_score(self, src, tar):
        """Return the Gotoh score of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Gotoh score

        Examples
        --------
        >>> cmp = Gotoh()
        >>> cmp.sim_score('cat', 'hat')
        2.0
        >>> cmp.sim_score('Niall', 'Neil')
        1.0
        >>> round(cmp.sim_score('aluminum', 'Catalan'), 12)
        -0.4
        >>> cmp.sim_score('cat', 'hat')
        2.0


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        d_mat = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_float32)
        p_mat = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_float32)
        q_mat = np_zeros((len(src) + 1, len(tar) + 1), dtype=np_float32)

        d_mat[0, 0] = 0
        p_mat[0, 0] = float('-inf')
        q_mat[0, 0] = float('-inf')
        for i in range(1, len(src) + 1):
            d_mat[i, 0] = float('-inf')
            p_mat[i, 0] = -self._gap_open - self._gap_ext * (i - 1)
            q_mat[i, 0] = float('-inf')
            if len(tar) > 1:
                q_mat[i, 1] = -self._gap_open
        for j in range(1, len(tar) + 1):
            d_mat[0, j] = float('-inf')
            p_mat[0, j] = float('-inf')
            if len(src) > 1:
                p_mat[1, j] = -self._gap_open
            q_mat[0, j] = -self._gap_open - self._gap_ext * (j - 1)

        for i in range(1, len(src) + 1):
            for j in range(1, len(tar) + 1):
                sim_val = self._sim_func(src[i - 1], tar[j - 1])
                d_mat[i, j] = max(
                    d_mat[i - 1, j - 1] + sim_val,
                    p_mat[i - 1, j - 1] + sim_val,
                    q_mat[i - 1, j - 1] + sim_val,
                )

                p_mat[i, j] = max(
                    d_mat[i - 1, j] - self._gap_open,
                    p_mat[i - 1, j] - self._gap_ext,
                )

                q_mat[i, j] = max(
                    d_mat[i, j - 1] - self._gap_open,
                    q_mat[i, j - 1] - self._gap_ext,
                )

        i, j = (n - 1 for n in d_mat.shape)
        return max(d_mat[i, j], p_mat[i, j], q_mat[i, j])

    def sim(self, src, tar):
        """Return the normalized Gotoh score of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized Gotoh score

        Examples
        --------
        >>> cmp = Gotoh()
        >>> cmp.sim('cat', 'hat')
        0.6666666666666667
        >>> cmp.sim('Niall', 'Neil')
        0.22360679774997896
        >>> round(cmp.sim('aluminum', 'Catalan'), 12)
        0.0
        >>> cmp.sim('cat', 'hat')
        0.6666666666666667


        .. versionadded:: 0.4.1

        """
        if src == tar:
            return 1.0
        return max(0.0, self.sim_score(src, tar)) / (
            self.sim_score(src, src) ** 0.5 * self.sim_score(tar, tar) ** 0.5
        )


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Gotoh.dist_abs method instead.',
)
def gotoh(src, tar, gap_open=1, gap_ext=0.4, sim_func=sim_ident):
    """Return the Gotoh score of two strings.

    This is a wrapper for :py:meth:`Gotoh.dist_abs`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    gap_open : float
        The cost of an open alignment gap (1 by default)
    gap_ext : float
        The cost of an alignment gap extension (0.4 by default)
    sim_func : function
        A function that returns the similarity of two characters (identity
        similarity by default)

    Returns
    -------
    float
        Gotoh score

    Examples
    --------
    >>> gotoh('cat', 'hat')
    2.0
    >>> gotoh('Niall', 'Neil')
    1.0
    >>> round(gotoh('aluminum', 'Catalan'), 12)
    -0.4
    >>> gotoh('cat', 'hat')
    2.0

    .. versionadded:: 0.1.0

    """
    return Gotoh(gap_open, gap_ext, sim_func).sim_score(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
