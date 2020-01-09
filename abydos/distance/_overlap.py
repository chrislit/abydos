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

"""abydos.distance._overlap.

Overlap similarity & distance
"""

from deprecation import deprecated

from ._token_distance import _TokenDistance
from .. import __version__

__all__ = ['Overlap', 'dist_overlap', 'sim_overlap']


class Overlap(_TokenDistance):
    r"""Overlap coefficient.

    For two sets X and Y, the overlap coefficient
    :cite:`Szymkiewicz:1934,Simpson:1949`, also called the
    Szymkiewicz-Simpson coefficient and Simpson's ecological coexistence
    coefficient, is

        .. math::

            sim_{overlap}(X, Y) = \frac{|X \cap Y|}{min(|X|, |Y|)}

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{overlap} = \frac{a}{min(a+b, a+c)}

    .. versionadded:: 0.3.6
    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize Overlap instance.

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
        super(Overlap, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )

    def sim(self, src, tar):
        r"""Return the overlap coefficient of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Overlap similarity

        Examples
        --------
        >>> cmp = Overlap()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.4
        >>> cmp.sim('aluminum', 'Catalan')
        0.125
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        if not self._src_card() or not self._tar_card():
            return 0.0

        return self._intersection_card() / min(
            self._src_card(), self._tar_card()
        )


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Overlap.sim method instead.',
)
def sim_overlap(src, tar, qval=2):
    r"""Return the overlap coefficient of two strings.

    This is a wrapper for :py:meth:`Overlap.sim`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram

    Returns
    -------
    float
        Overlap similarity

    Examples
    --------
    >>> sim_overlap('cat', 'hat')
    0.5
    >>> sim_overlap('Niall', 'Neil')
    0.4
    >>> sim_overlap('aluminum', 'Catalan')
    0.125
    >>> sim_overlap('ATCG', 'TAGC')
    0.0

    .. versionadded:: 0.1.0

    """
    return Overlap(qval=qval).sim(src, tar)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Overlap.dist method instead.',
)
def dist_overlap(src, tar, qval=2):
    """Return the overlap distance between two strings.

    This is a wrapper for :py:meth:`Overlap.dist`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram

    Returns
    -------
    float
        Overlap distance

    Examples
    --------
    >>> dist_overlap('cat', 'hat')
    0.5
    >>> dist_overlap('Niall', 'Neil')
    0.6
    >>> dist_overlap('aluminum', 'Catalan')
    0.875
    >>> dist_overlap('ATCG', 'TAGC')
    1.0

    .. versionadded:: 0.1.0

    """
    return Overlap(qval=qval).dist(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
