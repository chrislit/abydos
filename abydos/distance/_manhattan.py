# Copyright 2018-2020 by Christopher C. Little.
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

"""abydos.distance._manhattan.

Manhattan distance & similarity
"""

from deprecation import deprecated

from ._minkowski import Minkowski
from .. import __version__

__all__ = ['Manhattan', 'dist_manhattan', 'manhattan', 'sim_manhattan']


class Manhattan(Minkowski):
    """Manhattan distance.

    Manhattan distance is the city-block or taxi-cab distance, equivalent
    to Minkowski distance in :math:`L^1`-space.

    .. versionadded:: 0.3.6
    """

    def __init__(
        self, alphabet=0, tokenizer=None, intersection_type='crisp', **kwargs
    ):
        """Initialize Manhattan instance.

        Parameters
        ----------
        alphabet : collection or int
            The values or size of the alphabet
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        intersection_type : str
            Specifies the intersection type, and set type as a result:
            See :ref:`intersection_type <intersection_type>` description in
            :py:class:`_TokenDistance` for details.
        **kwargs
            Arbitrary keyword arguments

        Other Parameters
        ----------------
        qval : int
            The length of each q-gram. Using this parameter and tokenizer=None
            will cause the instance to use the QGram tokenizer with this
            q value.
        metric : _Distance
            A string distance measure class for use in the ``soft`` and
            ``fuzzy`` variants.
        threshold : float
            A threshold value, similarities above which are counted as
            members of the intersection for the ``fuzzy`` variant.


        .. versionadded:: 0.4.0

        """
        super(Manhattan, self).__init__(
            pval=1,
            alphabet=alphabet,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def dist_abs(self, src, tar, normalized=False):
        """Return the Manhattan distance between two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison
        normalized : bool
            Normalizes to [0, 1] if True

        Returns
        -------
        float
            The Manhattan distance

        Examples
        --------
        >>> cmp = Manhattan()
        >>> cmp.dist_abs('cat', 'hat')
        4.0
        >>> cmp.dist_abs('Niall', 'Neil')
        7.0
        >>> cmp.dist_abs('Colin', 'Cuilen')
        9.0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        10.0


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        return super(Manhattan, self).dist_abs(src, tar, normalized=normalized)

    def dist(self, src, tar):
        """Return the normalized Manhattan distance between two strings.

        The normalized Manhattan distance is a distance metric in
        :math:`L^1`-space, normalized to [0, 1].

        This is identical to Canberra distance.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            The normalized Manhattan distance

        Examples
        --------
        >>> cmp = Manhattan()
        >>> cmp.dist('cat', 'hat')
        0.5
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.636363636364
        >>> round(cmp.dist('Colin', 'Cuilen'), 12)
        0.692307692308
        >>> cmp.dist('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.3.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        return self.dist_abs(src, tar, normalized=True)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Manhattan.dist_abs method instead.',
)
def manhattan(src, tar, qval=2, normalized=False, alphabet=None):
    """Return the Manhattan distance between two strings.

    This is a wrapper for :py:meth:`Manhattan.dist_abs`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram
    normalized : bool
        Normalizes to [0, 1] if True
    alphabet : collection or int
        The values or size of the alphabet

    Returns
    -------
    float
        The Manhattan distance

    Examples
    --------
    >>> manhattan('cat', 'hat')
    4.0
    >>> manhattan('Niall', 'Neil')
    7.0
    >>> manhattan('Colin', 'Cuilen')
    9.0
    >>> manhattan('ATCG', 'TAGC')
    10.0

    .. versionadded:: 0.3.0

    """
    return Manhattan(alphabet=alphabet, qval=qval).dist_abs(
        src, tar, normalized=normalized
    )


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Manhattan.dist method instead.',
)
def dist_manhattan(src, tar, qval=2, alphabet=0):
    """Return the normalized Manhattan distance between two strings.

    This is a wrapper for :py:meth:`Manhattan.dist`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram
    alphabet : collection or int
        The values or size of the alphabet

    Returns
    -------
    float
        The normalized Manhattan distance

    Examples
    --------
    >>> dist_manhattan('cat', 'hat')
    0.5
    >>> round(dist_manhattan('Niall', 'Neil'), 12)
    0.636363636364
    >>> round(dist_manhattan('Colin', 'Cuilen'), 12)
    0.692307692308
    >>> dist_manhattan('ATCG', 'TAGC')
    1.0

    .. versionadded:: 0.3.0

    """
    return Manhattan(alphabet=alphabet, qval=qval).dist(src, tar)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Manhattan.sim method instead.',
)
def sim_manhattan(src, tar, qval=2, alphabet=0):
    """Return the normalized Manhattan similarity of two strings.

    This is a wrapper for :py:meth:`Manhattan.sim`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram
    alphabet : collection or int
        The values or size of the alphabet

    Returns
    -------
    float
        The normalized Manhattan similarity

    Examples
    --------
    >>> sim_manhattan('cat', 'hat')
    0.5
    >>> round(sim_manhattan('Niall', 'Neil'), 12)
    0.363636363636
    >>> round(sim_manhattan('Colin', 'Cuilen'), 12)
    0.307692307692
    >>> sim_manhattan('ATCG', 'TAGC')
    0.0

    .. versionadded:: 0.3.0

    """
    return Manhattan(alphabet=alphabet, qval=qval).sim(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
