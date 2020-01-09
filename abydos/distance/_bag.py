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

"""abydos.distance._bag.

Bag similarity & distance
"""

from deprecation import deprecated

from ._token_distance import _TokenDistance
from .. import __version__
from ..tokenizer import CharacterTokenizer

__all__ = ['Bag', 'bag', 'dist_bag', 'sim_bag']


class Bag(_TokenDistance):
    """Bag distance.

    Bag distance is proposed in :cite:`Bartolini:2002`. It is defined as

        .. math::

            dist_{bag}(src, tar) =
            max(|multiset(src)-multiset(tar)|, |multiset(tar)-multiset(src)|)

    .. versionadded:: 0.3.6
    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize Bag instance.

        Parameters
        ----------
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
        if tokenizer is None:
            tokenizer = CharacterTokenizer()
        super(Bag, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )

    def dist_abs(self, src, tar, normalized=False):
        """Return the bag distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        normalized : bool
            Normalizes to [0, 1] if True

        Returns
        -------
        int or float
            Bag distance

        Examples
        --------
        >>> cmp = Bag()
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        2
        >>> cmp.dist_abs('aluminum', 'Catalan')
        5
        >>> cmp.dist_abs('ATCG', 'TAGC')
        0
        >>> cmp.dist_abs('abcdefg', 'hijklm')
        7
        >>> cmp.dist_abs('abcdefg', 'hijklmno')
        8


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if tar == src:
            return 0
        elif not src:
            return len(tar)
        elif not tar:
            return len(src)

        self._tokenize(src, tar)

        dist = max(self._src_only_card(), self._tar_only_card())

        if normalized:
            dist /= max(self._src_card(), self._tar_card())

        return dist

    def dist(self, src, tar):
        """Return the normalized bag distance between two strings.

        Bag distance is normalized by dividing by :math:`max( |src|, |tar| )`.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Normalized bag distance

        Examples
        --------
        >>> cmp = Bag()
        >>> cmp.dist('cat', 'hat')
        0.3333333333333333
        >>> cmp.dist('Niall', 'Neil')
        0.4
        >>> cmp.dist('aluminum', 'Catalan')
        0.625
        >>> cmp.dist('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if tar == src:
            return 0.0
        if not src or not tar:
            return 1.0

        return self.dist_abs(src, tar, normalized=True)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Bag.dist_abs method instead.',
)
def bag(src, tar):
    """Return the bag distance between two strings.

    This is a wrapper for :py:meth:`Bag.dist_abs`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    int
        Bag distance

    Examples
    --------
    >>> bag('cat', 'hat')
    1
    >>> bag('Niall', 'Neil')
    2
    >>> bag('aluminum', 'Catalan')
    5
    >>> bag('ATCG', 'TAGC')
    0
    >>> bag('abcdefg', 'hijklm')
    7
    >>> bag('abcdefg', 'hijklmno')
    8

    .. versionadded:: 0.1.0

    """
    return Bag().dist_abs(src, tar)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Bag.dist method instead.',
)
def dist_bag(src, tar):
    """Return the normalized bag distance between two strings.

    This is a wrapper for :py:meth:`Bag.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    float
        Normalized bag distance

    Examples
    --------
    >>> dist_bag('cat', 'hat')
    0.3333333333333333
    >>> dist_bag('Niall', 'Neil')
    0.4
    >>> dist_bag('aluminum', 'Catalan')
    0.625
    >>> dist_bag('ATCG', 'TAGC')
    0.0

    .. versionadded:: 0.1.0

    """
    return Bag().dist(src, tar)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Bag.sim method instead.',
)
def sim_bag(src, tar):
    """Return the normalized bag similarity of two strings.

    This is a wrapper for :py:meth:`Bag.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison

    Returns
    -------
    float
        Normalized bag similarity

    Examples
    --------
    >>> round(sim_bag('cat', 'hat'), 12)
    0.666666666667
    >>> sim_bag('Niall', 'Neil')
    0.6
    >>> sim_bag('aluminum', 'Catalan')
    0.375
    >>> sim_bag('ATCG', 'TAGC')
    1.0

    .. versionadded:: 0.1.0

    """
    return Bag().sim(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
