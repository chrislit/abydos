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

The distance._distance module implements abstract class _Distance.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


class _Distance(object):
    """Abstract Distance class."""

    def sim(self, src, tar, *args, **kwargs):
        """Return similarity.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.

        Returns
        -------
        float
            Similarity

        """
        return 1.0 - self.dist(src, tar, *args, **kwargs)

    def dist(self, src, tar, *args, **kwargs):
        """Return distance.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.

        Returns
        -------
        float
            Distance

        """
        return 1.0 - self.sim(src, tar, *args, **kwargs)

    def dist_abs(self, src, tar, *args, **kwargs):
        """Return absolute distance.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.

        Returns
        -------
        int
            Absolute distance

        """
        return self.dist(src, tar, *args, **kwargs)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
