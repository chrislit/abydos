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

"""abydos.distance._iterative_substring.

Iterative-SubString (I-Sub) correlation
"""

from ._distance import _Distance

__all__ = ['IterativeSubString']


class IterativeSubString(_Distance):
    r"""Iterative-SubString correlation.

    Iterative-SubString (I-Sub) correlation :cite:`Stoilos:2005`

    This is a straightforward port of the primary author's Java implementation:
    http://www.image.ece.ntua.gr/~gstoil/software/I_Sub.java

    .. versionadded:: 0.4.0
    """

    def __init__(self, hamacher=0.6, normalize_strings=False, **kwargs):
        """Initialize IterativeSubString instance.

        Parameters
        ----------
        hamacher : float
            The constant factor for the Hamacher product
        normalize_strings : bool
            Normalize the strings by removing the characters in '._ ' and
            lower casing
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(IterativeSubString, self).__init__(**kwargs)
        self._normalize_strings = normalize_strings
        self._hamacher = hamacher

    def corr(self, src, tar):
        """Return the Iterative-SubString correlation of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Iterative-SubString correlation

        Examples
        --------
        >>> cmp = IterativeSubString()
        >>> cmp.corr('cat', 'hat')
        -1.0
        >>> cmp.corr('Niall', 'Neil')
        -0.9
        >>> cmp.corr('aluminum', 'Catalan')
        -1.0
        >>> cmp.corr('ATCG', 'TAGC')
        -1.0


        .. versionadded:: 0.4.0

        """
        input_src = src
        input_tar = tar

        def _winkler_improvement(src, tar, commonality):
            for i in range(min(len(src), len(tar))):
                if src[i] != tar[i]:
                    break
            return min(4, i) * 0.1 * (1 - commonality)

        if self._normalize_strings:
            src = src.lower()
            tar = tar.lower()

            for ch in '._ ':
                src = src.replace(ch, '')
                tar = tar.replace(ch, '')

        src_len = len(src)
        tar_len = len(tar)

        if src_len == 0 and tar_len == 0:
            return 1.0
        if src_len == 0 or tar_len == 0:
            return -1.0

        common = 0
        best = 2

        while len(src) > 0 and len(tar) > 0 and best != 0:
            best = 0

            ls = len(src)
            lt = len(tar)

            start_src = 0
            end_src = 0
            start_tar = 0
            end_tar = 0

            i = 0
            while i < ls and ls - i > best:
                j = 0
                while lt - j > best:
                    k = i

                    while j < lt and src[k] != tar[j]:
                        j += 1

                    if j != lt:
                        p = j
                        j += 1
                        k += 1
                        while j < lt and k < ls and src[k] == tar[j]:
                            j += 1
                            k += 1
                        if k - i > best:
                            best = k - i
                            start_src = i
                            end_src = k
                            start_tar = p
                            end_tar = j
                i += 1

            src = src[:start_src] + src[end_src:]
            tar = tar[:start_tar] + tar[end_tar:]

            if best > 2:
                common += best
            else:
                best = 0

        commonality = 2.0 * common / (src_len + tar_len)
        winkler_improvement = _winkler_improvement(
            input_src, input_tar, commonality
        )

        unmatched_src = max(src_len - common, 0) / src_len
        unmatched_tar = max(tar_len - common, 0) / tar_len

        unmatched_prod = unmatched_src * unmatched_tar
        dissimilarity = unmatched_prod / (
            self._hamacher
            + (1 - self._hamacher)
            * (unmatched_src + unmatched_tar - unmatched_prod)
        )

        return commonality - dissimilarity + winkler_improvement

    def sim(self, src, tar):
        """Return the Iterative-SubString similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Iterative-SubString similarity

        Examples
        --------
        >>> cmp = IterativeSubString()
        >>> cmp.sim('cat', 'hat')
        0.0
        >>> cmp.sim('Niall', 'Neil')
        0.04999999999999999
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        return (self.corr(src, tar) + 1.0) / 2.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
