# Copyright 2018-2022 by Christopher C. Little.
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

"""abydos.distance._sift4.

Sift4 Common approximate string distance
"""

from typing import Any, Dict, List, Union

from ._distance import _Distance

__all__ = ['Sift4']


class Sift4(_Distance):
    """Sift4 Common version.

    This is an approximation of edit distance, described in
    :cite:`Zackwehdex:2014`.

    .. versionadded:: 0.3.6
    """

    def __init__(
        self, max_offset: int = 5, max_distance: int = 0, **kwargs: Any
    ) -> None:
        """Initialize Sift4 instance.

        Parameters
        ----------
        max_offset : int
            The number of characters to search for matching letters
        max_distance : int
            The distance at which to stop and exit
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super().__init__(**kwargs)
        self._max_offset = max_offset
        self._max_distance = max_distance

    def dist_abs(self, src: str, tar: str) -> float:
        """Return the "common" Sift4 distance between two terms.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int
            The Sift4 distance according to the common formula

        Examples
        --------
        >>> cmp = Sift4()
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        2
        >>> cmp.dist_abs('Colin', 'Cuilen')
        3
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if not src:
            return len(tar)

        if not tar:
            return len(src)

        src_len = len(src)
        tar_len = len(tar)

        src_cur = 0
        tar_cur = 0
        lcss = 0
        local_cs = 0
        trans = 0
        offset_arr = []  # type: List[Dict[str, Union[int, bool]]]

        while (src_cur < src_len) and (tar_cur < tar_len):
            if src[src_cur] == tar[tar_cur]:
                local_cs += 1
                is_trans = False
                i = 0
                while i < len(offset_arr):
                    ofs = offset_arr[i]
                    if src_cur <= ofs['src_cur'] or tar_cur <= ofs['tar_cur']:
                        is_trans = abs(tar_cur - src_cur) >= abs(
                            ofs['tar_cur'] - ofs['src_cur']
                        )
                        if is_trans:
                            trans += 1
                        elif not ofs['trans']:
                            ofs['trans'] = True
                            trans += 1
                        break
                    elif src_cur > ofs['tar_cur'] and tar_cur > ofs['src_cur']:
                        del offset_arr[i]
                    else:
                        i += 1

                offset_arr.append(
                    {'src_cur': src_cur, 'tar_cur': tar_cur, 'trans': is_trans}
                )
            else:
                lcss += local_cs
                local_cs = 0
                if src_cur != tar_cur:
                    src_cur = tar_cur = min(src_cur, tar_cur)
                for i in range(self._max_offset):
                    if not (
                        (src_cur + i < src_len) or (tar_cur + i < tar_len)
                    ):
                        break
                    if (src_cur + i < src_len) and (
                        src[src_cur + i] == tar[tar_cur]
                    ):
                        src_cur += i - 1
                        tar_cur -= 1
                        break
                    if (tar_cur + i < tar_len) and (
                        src[src_cur] == tar[tar_cur + i]
                    ):
                        src_cur -= 1
                        tar_cur += i - 1
                        break

            src_cur += 1
            tar_cur += 1

            if self._max_distance:
                temporary_distance = max(src_cur, tar_cur) - lcss + trans
                if temporary_distance >= self._max_distance:
                    return round(temporary_distance)

            if (src_cur >= src_len) or (tar_cur >= tar_len):
                lcss += local_cs
                local_cs = 0
                src_cur = tar_cur = min(src_cur, tar_cur)

        lcss += local_cs
        return round(max(src_len, tar_len) - lcss + trans)

    def dist(self, src: str, tar: str) -> float:
        """Return the normalized "common" Sift4 distance between two terms.

        This is Sift4 distance, normalized to [0, 1].

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The normalized Sift4 distance

        Examples
        --------
        >>> cmp = Sift4()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.333333333333
        >>> cmp.dist('Niall', 'Neil')
        0.4
        >>> cmp.dist('Colin', 'Cuilen')
        0.5
        >>> cmp.dist('ATCG', 'TAGC')
        0.5


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        return self.dist_abs(src, tar) / (max(len(src), len(tar), 1))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
