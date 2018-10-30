# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
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

"""abydos.distance.basic.

The distance.basic module implements simple string edit distance functions
including:

    - Identity similarity & distance
    - Length similarity & distance
    - Prefix similarity & distance
    - Suffix similarity & distance
"""

from __future__ import division, unicode_literals

from six.moves import range

from ._util import Distance

__all__ = [
    'Ident',
    'dist_ident',
    'sim_ident',
    'Length',
    'dist_length',
    'sim_length',
    'Prefix',
    'dist_prefix',
    'sim_prefix',
    'Suffix',
    'dist_suffix',
    'sim_suffix',
]


class Ident(Distance):
    """Identity distance and similarity."""

    def sim(self, src, tar):
        """Return the identity similarity of two strings.

        Identity similarity is 1 if the two strings are identical, otherwise 0.

        :param str src: source string for comparison
        :param str tar: target string for comparison
        :returns: identity similarity
        :rtype: float

        >>> cmp = Ident()
        >>> cmp.sim('cat', 'hat')
        0
        >>> cmp.sim('cat', 'cat')
        1
        """
        return 1.0 if src == tar else 0.0

    def dist(self, src, tar):
        """Return the identity distance between two strings.

        Identity distance is 0 if the two strings are identical, otherwise 1.

        :param str src: source string for comparison
        :param str tar: target string for comparison
        :returns: identity distance
        :rtype: int

        >>> cmp = Ident()
        >>> cmp.dist('cat', 'hat')
        1
        >>> cmp.dist('cat', 'cat')
        0
        """
        return super().dist(src, tar)


def sim_ident(src, tar):
    """Return the identity similarity of two strings.

    This is a wrapper for :py:meth:`Ident.sim`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: identity similarity
    :rtype: int

    >>> sim_ident('cat', 'hat')
    0
    >>> sim_ident('cat', 'cat')
    1
    """
    return Ident().sim(src, tar)


def dist_ident(src, tar):
    """Return the identity distance between two strings.

    This is a wrapper for :py:meth:`Ident.dist`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: identity distance
    :rtype: int

    >>> dist_ident('cat', 'hat')
    1
    >>> dist_ident('cat', 'cat')
    0
    """
    return Ident().dist(src, tar)


class Length(Distance):
    """Length similarity and distance."""

    def sim(self, src, tar):
        """Return the length similarity of two strings.

        Length similarity is the ratio of the length of the shorter string to the
        longer.

        :param str src: source string for comparison
        :param str tar: target string for comparison
        :returns: length similarity
        :rtype: float

        >>> cmp = Length()
        >>> cmp.sim('cat', 'hat')
        1.0
        >>> cmp.sim('Niall', 'Neil')
        0.8
        >>> cmp.sim('aluminum', 'Catalan')
        0.875
        >>> cmp.sim('ATCG', 'TAGC')
        1.0
        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0
        return len(src) / len(tar) if len(src) < len(tar) else len(tar) / len(src)

    def dist(self, src, tar):
        """Return the length distance between two strings.

        Length distance is the complement of length similarity:
        :math:`dist_{length} = 1 - sim_{length}`.

        :param str src: source string for comparison
        :param str tar: target string for comparison
        :returns: length distance
        :rtype: float

        >>> cmp = Length()
        >>> cmp.dist('cat', 'hat')
        0.0
        >>> cmp.dist('Niall', 'Neil')
        0.19999999999999996
        >>> cmp.dist('aluminum', 'Catalan')
        0.125
        >>> cmp.dist('ATCG', 'TAGC')
        0.0
        """
        return super().dist(src, tar)


def sim_length(src, tar):
    """Return the length similarity of two strings.

    This is a wrapper for :py:meth:`Length.sim`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: length similarity
    :rtype: float

    >>> sim_length('cat', 'hat')
    1.0
    >>> sim_length('Niall', 'Neil')
    0.8
    >>> sim_length('aluminum', 'Catalan')
    0.875
    >>> sim_length('ATCG', 'TAGC')
    1.0
    """
    return Length().sim(src, tar)


def dist_length(src, tar):
    """Return the length distance between two strings.

    This is a wrapper for :py:meth:`Length.dist`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: length distance
    :rtype: float

    >>> dist_length('cat', 'hat')
    0.0
    >>> dist_length('Niall', 'Neil')
    0.19999999999999996
    >>> dist_length('aluminum', 'Catalan')
    0.125
    >>> dist_length('ATCG', 'TAGC')
    0.0
    """
    return Length().dist(src, tar)


class Prefix(Distance):
    """Prefix similiarity and distance."""

    def sim(self, src, tar):
        """Return the prefix similarity of two strings.

        Prefix similarity is the ratio of the length of the shorter term that
        exactly matches the longer term to the length of the shorter term,
        beginning at the start of both terms.

        :param str src: source string for comparison
        :param str tar: target string for comparison
        :returns: prefix similarity
        :rtype: float

        >>> cmp = Prefix()
        >>> cmp.sim('cat', 'hat')
        0.0
        >>> cmp.sim('Niall', 'Neil')
        0.25
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0
        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0
        min_word, max_word = (src, tar) if len(src) < len(tar) else (tar, src)
        min_len = len(min_word)
        for i in range(min_len, 0, -1):
            if min_word[:i] == max_word[:i]:
                return i / min_len
        return 0.0

    def dist(self, src, tar):
        """Return the prefix distance between two strings.

        Prefix distance is the complement of prefix similarity:
        :math:`dist_{prefix} = 1 - sim_{prefix}`.

        :param str src: source string for comparison
        :param str tar: target string for comparison
        :returns: prefix distance
        :rtype: float

        >>> cmp = Prefix()
        >>> cmp.dist('cat', 'hat')
        1.0
        >>> cmp.dist('Niall', 'Neil')
        0.75
        >>> cmp.dist('aluminum', 'Catalan')
        1.0
        >>> cmp.dist('ATCG', 'TAGC')
        1.0
        """
        return super().dist(src, tar)


def sim_prefix(src, tar):
    """Return the prefix similarity of two strings.

    This is a wrapper for :py:meth:`Prefix.sim`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: prefix similarity
    :rtype: float

    >>> sim_prefix('cat', 'hat')
    0.0
    >>> sim_prefix('Niall', 'Neil')
    0.25
    >>> sim_prefix('aluminum', 'Catalan')
    0.0
    >>> sim_prefix('ATCG', 'TAGC')
    0.0
    """
    return Prefix().sim(src, tar)


def dist_prefix(src, tar):
    """Return the prefix distance between two strings.

    This is a wrapper for :py:meth:`Prefix.dist`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: prefix distance
    :rtype: float

    >>> dist_prefix('cat', 'hat')
    1.0
    >>> dist_prefix('Niall', 'Neil')
    0.75
    >>> dist_prefix('aluminum', 'Catalan')
    1.0
    >>> dist_prefix('ATCG', 'TAGC')
    1.0
    """
    return Prefix().dist(src, tar)


class Suffix(Distance):
    """Suffix similarity and distance."""

    def sim(self, src, tar):
        """Return the suffix similarity of two strings.

        Suffix similarity is the ratio of the length of the shorter term that
        exactly matches the longer term to the length of the shorter term,
        beginning at the end of both terms.

        :param str src: source string for comparison
        :param str tar: target string for comparison
        :returns: suffix similarity
        :rtype: float

        >>> cmp = Suffix()
        >>> cmp.sim('cat', 'hat')
        0.6666666666666666
        >>> cmp.sim('Niall', 'Neil')
        0.25
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0
        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0
        min_word, max_word = (src, tar) if len(src) < len(tar) else (tar, src)
        min_len = len(min_word)
        for i in range(min_len, 0, -1):
            if min_word[-i:] == max_word[-i:]:
                return i / min_len
        return 0.0

    def dist(self, src, tar):
        """Return the suffix distance between two strings.

        Suffix distance is the complement of suffix similarity:
        :math:`dist_{suffix} = 1 - sim_{suffix}`.

        :param str src: source string for comparison
        :param str tar: target string for comparison
        :returns: suffix distance
        :rtype: float

        >>> cmp = Suffix()
        >>> cmp.dist('cat', 'hat')
        0.33333333333333337
        >>> cmp.dist('Niall', 'Neil')
        0.75
        >>> cmp.dist('aluminum', 'Catalan')
        1.0
        >>> cmp.dist('ATCG', 'TAGC')
        1.0
        """
        return super().dist(src, tar)


def sim_suffix(src, tar):
    """Return the suffix similarity of two strings.

    This is a wrapper for :py:meth:`Suffix.sim`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: suffix similarity
    :rtype: float

    >>> sim_suffix('cat', 'hat')
    0.6666666666666666
    >>> sim_suffix('Niall', 'Neil')
    0.25
    >>> sim_suffix('aluminum', 'Catalan')
    0.0
    >>> sim_suffix('ATCG', 'TAGC')
    0.0
    """
    return Suffix().sim(src, tar)


def dist_suffix(src, tar):
    """Return the suffix distance between two strings.

    This is a wrapper for :py:meth:`Suffix.dist`.

    :param str src: source string for comparison
    :param str tar: target string for comparison
    :returns: suffix distance
    :rtype: float

    >>> dist_suffix('cat', 'hat')
    0.33333333333333337
    >>> dist_suffix('Niall', 'Neil')
    0.75
    >>> dist_suffix('aluminum', 'Catalan')
    1.0
    >>> dist_suffix('ATCG', 'TAGC')
    1.0
    """
    return Suffix().dist(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
