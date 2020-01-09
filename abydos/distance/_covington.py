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

"""abydos.distance._covington.

Covington distance
"""

from collections import namedtuple
from unicodedata import normalize as unicode_normalize

from ._distance import _Distance

__all__ = ['Covington']

Alignment = namedtuple('Alignment', ['src', 'tar', 'score'])


class Covington(_Distance):
    r"""Covington distance.

    Covington distance :cite:`Covington:1996`

    .. versionadded:: 0.4.0
    """

    def __init__(self, weights=(0, 5, 10, 30, 60, 100, 40, 50), **kwargs):
        """Initialize Covington instance.

        Parameters
        ----------
        weights : tuple
            An 8-tuple of costs for each kind of match or mismatch described in
            Covington's paper:

                - exact consonant or glide match
                - exact vowel match
                - vowel-vowel length mismatch or i and y or u and w
                - vowel-vowel mismatch
                - consonant-consonant mismatch
                - consonant-vowel mismatch
                - skip preceded by a skip
                - skip not preceded by a skip

            The weights used in Covington's first approximation can be used
            by supplying the tuple (0.0, 0.0, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5)
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(Covington, self).__init__(**kwargs)
        self._weights = weights
        self._vowels = set('aeiou')
        self._consonants = set('bcdfghjklmnpqrstvxz')
        self._glides = set('wy')

    def dist_abs(self, src, tar):
        """Return the Covington distance of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Covington distance

        Examples
        --------
        >>> cmp = Covington()
        >>> cmp.dist_abs('cat', 'hat')
        65
        >>> cmp.dist_abs('Niall', 'Neil')
        115
        >>> cmp.dist_abs('aluminum', 'Catalan')
        325
        >>> cmp.dist_abs('ATCG', 'TAGC')
        200


        .. versionadded:: 0.4.0

        """
        return self.alignments(src, tar, 1)[0][-1]

    def dist(self, src, tar):
        """Return the normalized Covington distance of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized Covington distance

        Examples
        --------
        >>> cmp = Covington()
        >>> cmp.dist('cat', 'hat')
        0.19117647058823528
        >>> cmp.dist('Niall', 'Neil')
        0.25555555555555554
        >>> cmp.dist('aluminum', 'Catalan')
        0.43333333333333335
        >>> cmp.dist('ATCG', 'TAGC')
        0.45454545454545453


        .. versionadded:: 0.4.0

        """
        normalizer = self._weights[5] * min(len(src), len(tar))
        if len(src) != len(tar):
            normalizer += self._weights[7]
        normalizer += self._weights[6] * abs(abs(len(src) - len(tar)) - 1)

        return self.dist_abs(src, tar) / normalizer

    def alignment(self, src, tar):
        """Return the top Covington alignment of two strings.

        This returns only the top alignment in a standard
        (score, source alignment, target alignment) tuple format.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        tuple(float, str, str)
            Covington score & alignment

        Examples
        --------
        >>> cmp = Covington()
        >>> cmp.alignment('hart', 'kordis')
        (240, 'hart--', 'kordis')
        >>> cmp.alignment('niy', 'genu')
        (170, '--niy', 'genu-')


        .. versionadded:: 0.4.1

        """
        alignment = self.alignments(src, tar, 1)[0]
        return alignment.score, alignment.src, alignment.tar

    def alignments(self, src, tar, top_n=None):
        """Return the Covington alignments of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        top_n : int
            The number of alignments to return. If None, all alignments will
            be returned. If 0, all alignments with the top score will be
            returned.

        Returns
        -------
        list
            Covington alignments

        Examples
        --------
        >>> cmp = Covington()
        >>> cmp.alignments('hart', 'kordis', top_n=1)[0]
        Alignment(src='hart--', tar='kordis', score=240)
        >>> cmp.alignments('niy', 'genu', top_n=1)[0]
        Alignment(src='--niy', tar='genu-', score=170)


        .. versionadded:: 0.4.0

        """
        if not src:
            if not tar:
                return [['', '', 0]]
            return [
                [
                    '-' * len(tar),
                    src,
                    self._weights[7] + self._weights[6] * (len(tar) - 1),
                ]
            ]
        if not tar:
            return [
                [
                    src,
                    '-' * len(src),
                    self._weights[7] + self._weights[6] * (len(src) - 1),
                ]
            ]

        terminals = []

        def _cost(s, t):
            if s[-1:] == '-':
                if s[-2:] == '--':
                    return self._weights[6]
                else:
                    return self._weights[7]
            elif t[-1:] == '-':
                if t[-2:] == '--':
                    return self._weights[6]
                else:
                    return self._weights[7]

            s = unicode_normalize('NFC', s)[-1:]
            t = unicode_normalize('NFC', t)[-1:]

            if s == t:
                if s in self._consonants or s in self._glides:
                    return self._weights[0]
                else:
                    return self._weights[1]

            if ''.join(sorted([s, t])) in {'iy', 'uw'}:
                return self._weights[2]

            sd = unicode_normalize('NFKD', s)
            td = unicode_normalize('NFKD', t)

            if sd[0] == td[0] and s in self._vowels:
                return self._weights[2]

            if sd[0] in self._vowels and td[0] in self._vowels:
                return self._weights[3]
            if sd[0] in self._consonants and td[0] in self._consonants:
                return self._weights[4]

            return self._weights[5]

        def _add_alignments(cost, src, tar, src_align, tar_align):
            cost += _cost(src_align, tar_align)

            if src and tar:
                _add_alignments(
                    cost,
                    src[1:],
                    tar[1:],
                    src_align + src[0],
                    tar_align + tar[0],
                )
            if tar and tar_align[-1] != '-':
                _add_alignments(
                    cost, src, tar[1:], src_align + '-', tar_align + tar[0]
                )
            if src and src_align[-1] != '-':
                _add_alignments(
                    cost, src[1:], tar, src_align + src[0], tar_align + '-'
                )

            if not src and not tar:
                terminals.append(Alignment(src_align, tar_align, cost))

            return

        _add_alignments(0, src, tar[1:], '-', tar[0])
        _add_alignments(0, src[1:], tar, src[0], '-')
        _add_alignments(0, src[1:], tar[1:], src[0], tar[0])

        def _score(al):
            return al.score

        terminals = sorted(terminals, key=_score)

        if top_n == 0:
            top_score = terminals[0].score
            top_n = 1
            while (
                top_n < len(terminals) and terminals[top_n].score == top_score
            ):
                top_n += 1

        if top_n is None:
            return terminals
        else:
            return terminals[:top_n]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
