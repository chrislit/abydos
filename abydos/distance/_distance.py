# -*- coding: utf-8 -*-

# Copyright 2018 by Christopher C. Little.
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

"""abydos.distance._distance.

The distance._distance module implements abstract class Distance.
"""

from __future__ import unicode_literals

from collections import Counter

from ..tokenizer import QGrams


class Distance(object):
    """Abstract Distance class."""

    def sim(self, src, tar, *args, **kwargs):
        """Return similarity.

        :param src:
        :param tar:
        :param args:
        :param kwargs:
        :return:
        """
        return 1.0 - self.dist(src, tar, *args, **kwargs)

    def dist(self, src, tar, *args, **kwargs):
        """Return distance.

        :param src:
        :param tar:
        :param args:
        :param kwargs:
        :return:
        """
        return 1.0 - self.sim(src, tar, *args, **kwargs)

    def dist_abs(self, src, tar, *args, **kwargs):
        """Return absolute distance.

        :param src:
        :param tar:
        :param args:
        :param kwargs:
        :return:
        """
        return self.dist(src, tar, *args, **kwargs)


class TokenDistance(Distance):
    """Abstract Token Distance class."""

    def _get_qgrams(self, src, tar, qval=0, skip=0):
        """Return the Q-Grams in src & tar.

        :param str src: source string (or QGrams/Counter objects) for
            comparison
        :param str tar: target string (or QGrams/Counter objects) for
            comparison
        :param int qval: the length of each q-gram; 0 for non-q-gram version
        :param int skip: the number of characters to skip (only works when
            src and tar are strings
        :returns: Q-Grams
        :rtype: tuple of Counters

        >>> pe = TokenDistance()
        >>> pe._get_qgrams('AT', 'TT', qval=2)
        (QGrams({'$A': 1, 'AT': 1, 'T#': 1}),
         QGrams({'$T': 1, 'TT': 1, 'T#': 1}))
        """
        if isinstance(src, Counter) and isinstance(tar, Counter):
            return src, tar
        if qval > 0:
            return QGrams(src, qval, '$#', skip), QGrams(tar, qval, '$#', skip)
        return Counter(src.strip().split()), Counter(tar.strip().split())


if __name__ == '__main__':
    import doctest

    doctest.testmod()
