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

"""abydos.distance._mlipns.

The distance.hamming module implements Hamming and related distance functions.
"""

from deprecation import deprecated

from ._distance import _Distance
from ._hamming import Hamming
from .. import __version__

__all__ = ['MLIPNS', 'dist_mlipns', 'sim_mlipns']


class MLIPNS(_Distance):
    """MLIPNS similarity.

    Modified Language-Independent Product Name Search (MLIPNS) is described in
    :cite:`Shannaq:2010`. This function returns only 1.0 (similar) or 0.0
    (not similar). LIPNS similarity is identical to normalized Hamming
    similarity.

    .. versionadded:: 0.3.6
    """

    _hamming = Hamming(diff_lens=True)

    def __init__(self, threshold=0.25, max_mismatches=2, **kwargs):
        """Initialize MLIPNS instance.

        Parameters
        ----------
        threshold : float
            A number [0, 1] indicating the maximum similarity score, below
            which the strings are considered 'similar' (0.25 by default)
        max_mismatches : int
            A number indicating the allowable number of mismatches to remove
            before declaring two strings not similar (2 by default)
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(MLIPNS, self).__init__(**kwargs)
        self._threshold = threshold
        self._max_mismatches = max_mismatches

    def sim(self, src, tar):
        """Return the MLIPNS similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            MLIPNS similarity

        Examples
        --------
        >>> sim_mlipns('cat', 'hat')
        1.0
        >>> sim_mlipns('Niall', 'Neil')
        0.0
        >>> sim_mlipns('aluminum', 'Catalan')
        0.0
        >>> sim_mlipns('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if tar == src:
            return 1.0
        if not src or not tar:
            return 0.0

        mismatches = 0
        ham = self._hamming.dist_abs(src, tar)
        max_length = max(len(src), len(tar))
        while src and tar and mismatches <= self._max_mismatches:
            if (
                max_length < 1
                or (1 - (max_length - ham) / max_length) <= self._threshold
            ):
                return 1.0
            else:
                mismatches += 1
                ham -= 1
                max_length -= 1

        if max_length < 1:
            return 1.0
        return 0.0


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the MLIPNS.sim method instead.',
)
def sim_mlipns(src, tar, threshold=0.25, max_mismatches=2):
    """Return the MLIPNS similarity of two strings.

    This is a wrapper for :py:meth:`MLIPNS.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    threshold : float
        A number [0, 1] indicating the maximum similarity score, below which
        the strings are considered 'similar' (0.25 by default)
    max_mismatches : int
        A number indicating the allowable number of mismatches to remove before
        declaring two strings not similar (2 by default)

    Returns
    -------
    float
        MLIPNS similarity

    Examples
    --------
    >>> sim_mlipns('cat', 'hat')
    1.0
    >>> sim_mlipns('Niall', 'Neil')
    0.0
    >>> sim_mlipns('aluminum', 'Catalan')
    0.0
    >>> sim_mlipns('ATCG', 'TAGC')
    0.0

    .. versionadded:: 0.1.0

    """
    return MLIPNS(threshold, max_mismatches).sim(src, tar)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the MLIPNS.dist method instead.',
)
def dist_mlipns(src, tar, threshold=0.25, max_mismatches=2):
    """Return the MLIPNS distance between two strings.

    This is a wrapper for :py:meth:`MLIPNS.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    threshold : float
        A number [0, 1] indicating the maximum similarity score, below which
        the strings are considered 'similar' (0.25 by default)
    max_mismatches : int
        A number indicating the allowable number of mismatches to remove before
        declaring two strings not similar (2 by default)

    Returns
    -------
    float
        MLIPNS distance

    Examples
    --------
    >>> dist_mlipns('cat', 'hat')
    0.0
    >>> dist_mlipns('Niall', 'Neil')
    1.0
    >>> dist_mlipns('aluminum', 'Catalan')
    1.0
    >>> dist_mlipns('ATCG', 'TAGC')
    1.0

    .. versionadded:: 0.1.0

    """
    return MLIPNS(threshold, max_mismatches).dist(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
