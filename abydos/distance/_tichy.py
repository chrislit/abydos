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

"""abydos.distance._tichy.

Tichy edit distance
"""

from ._distance import _Distance

__all__ = ['Tichy']


class Tichy(_Distance):
    """Tichy edit distance.

    Tichy described an algorithm, implemented below, in :cite:`Tichy:1984`.
    Following this, :cite:`Cormode:2003` identifies an interpretation of this
    algorithm's output as a distance measure, which is largely followed by the
    methods below.

    Tichy's algorithm locates substrings of a string S to be copied in order
    to create a string T. The only other operation used by his algorithms for
    string reconstruction are add operations.

    Notes
    -----
    While :cite:`Cormode:2003` counts only move operations to calculate
    distance, I give the option (enabled by default) of counting add operations
    as part of the distance measure. To ignore the cost of add operations, set
    the cost value to (1, 0), for example, when initializing the object.
    Further, in the case that S and T are identical, a distance of 0 will be
    returned, even though this would still be counted as a single move
    operation spanning the whole of string S.

    .. versionadded:: 0.4.0

    """

    def __init__(self, cost=(1, 1), **kwargs):
        """Initialize Tichy instance.

        Parameters
        ----------
        cost : tuple
            A 2-tuple representing the cost of the two possible edits:
            block moves and adds (by default: (1, 1))
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(Tichy, self).__init__(**kwargs)
        self._cost = cost

    def dist_abs(self, src, tar):
        """Return the Tichy distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int (may return a float if cost has float values)
            The Tichy distance between src & tar

        Examples
        --------
        >>> cmp = Tichy()
        >>> cmp.dist_abs('cat', 'hat')
        2
        >>> cmp.dist_abs('Niall', 'Neil')
        4
        >>> cmp.dist_abs('aluminum', 'Catalan')
        6
        >>> cmp.dist_abs('ATCG', 'TAGC')
        4


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0

        def _find_max_block(src, tar, q_pos):
            length = 0
            p_pos = 0
            p_cur = 0

            while p_cur + length <= src_len and q_pos + length <= tar_len:
                length_cur = 0
                while (
                    p_cur + length_cur < src_len
                    and q_pos + length_cur < tar_len
                    and src[p_cur + length_cur] == tar[q_pos + length_cur]
                ):
                    length_cur += 1
                if length_cur > length:
                    length = length_cur
                    p_pos = p_cur
                p_cur += 1
            return p_pos, length

        moves = 0
        adds = 0
        src_len = len(src)
        tar_len = len(tar)
        q_pos = 0

        while q_pos < tar_len:
            p_pos, length = _find_max_block(src, tar, q_pos)
            if length > 0:
                moves += 1
            else:
                adds += 1
            q_pos += max(1, length)

        return moves * self._cost[0] + adds * self._cost[1]

    def dist(self, src, tar):
        """Return the normalized Tichy edit distance between two strings.

        The Tichy distance is normalized by dividing the distance by the length
        of the tar string.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The normalized Tichy distance between src & tar

        Examples
        --------
        >>> cmp = Tichy()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.666666666667
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        1.0
        >>> cmp.dist('aluminum', 'Catalan')
        0.8571428571428571
        >>> cmp.dist('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 0.0

        score = self.dist_abs(src, tar)
        if score:
            return score / (len(tar) * max(self._cost))
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
