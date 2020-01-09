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

"""abydos.distance._length.

Length similarity & distance
"""

from deprecation import deprecated

from ._distance import _Distance
from .. import __version__

__all__ = ['Length', 'dist_length', 'sim_length']


class Length(_Distance):
    """Length similarity and distance.

    .. versionadded:: 0.3.6
    """

    def sim(self, src, tar):
        """Return the length similarity of two strings.

        Length similarity is the ratio of the length of the shorter string to
        the longer.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Length similarity

        Examples
        --------
        >>> cmp = Length()
        >>> cmp.sim('cat', 'hat')
        1.0
        >>> cmp.sim('Niall', 'Neil')
        0.8
        >>> cmp.sim('aluminum', 'Catalan')
        0.875
        >>> cmp.sim('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0
        return (
            len(src) / len(tar) if len(src) < len(tar) else len(tar) / len(src)
        )


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Length.sim method instead.',
)
def sim_length(src, tar):
    """Return the length similarity of two strings.

    This is a wrapper for :py:meth:`Length.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    float
        Length similarity

    Examples
    --------
    >>> sim_length('cat', 'hat')
    1.0
    >>> sim_length('Niall', 'Neil')
    0.8
    >>> sim_length('aluminum', 'Catalan')
    0.875
    >>> sim_length('ATCG', 'TAGC')
    1.0


    .. versionadded:: 0.1.0

    """
    return Length().sim(src, tar)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Length.dist method instead.',
)
def dist_length(src, tar):
    """Return the length distance between two strings.

    This is a wrapper for :py:meth:`Length.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    float
        Length distance

    Examples
    --------
    >>> dist_length('cat', 'hat')
    0.0
    >>> dist_length('Niall', 'Neil')
    0.19999999999999996
    >>> dist_length('aluminum', 'Catalan')
    0.125
    >>> dist_length('ATCG', 'TAGC')
    0.0


    .. versionadded:: 0.1.0

    """
    return Length().dist(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
