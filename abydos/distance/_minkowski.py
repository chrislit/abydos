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

"""abydos.distance._minkowski.

Minkowski distance & similarity
"""

from deprecation import deprecated

from ._token_distance import _TokenDistance
from .. import __version__

__all__ = ['Minkowski', 'dist_minkowski', 'minkowski', 'sim_minkowski']


class Minkowski(_TokenDistance):
    """Minkowski distance.

    The Minkowski distance :cite:`Minkowski:1910` is a distance metric in
    :math:`L^p-space`.

    .. versionadded:: 0.3.6
    """

    def __init__(
        self,
        pval=1,
        alphabet=0,
        tokenizer=None,
        intersection_type='crisp',
        **kwargs
    ):
        """Initialize Euclidean instance.

        Parameters
        ----------
        pval : int
            The :math:`p`-value of the :math:`L^p`-space
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
        super(Minkowski, self).__init__(
            tokenizer=tokenizer,
            alphabet=alphabet,
            intersection_type=intersection_type,
            **kwargs
        )
        self.set_params(pval=pval)

    def dist_abs(self, src, tar, normalized=False):
        """Return the Minkowski distance (:math:`L^p`-norm) of two strings.

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
            The Minkowski distance

        Examples
        --------
        >>> cmp = Minkowski()
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
        self._tokenize(src, tar)
        diffs = self._symmetric_difference().values()

        normalizer = 1
        if normalized:
            totals = self._total().values()
            if self.params['alphabet']:
                normalizer = self.params['alphabet']
            elif self.params['pval'] == 0:
                normalizer = len(totals)
            else:
                normalizer = sum(_ ** self.params['pval'] for _ in totals) ** (
                    1 / self.params['pval']
                )

        if len(diffs) == 0:
            return 0.0
        if self.params['pval'] == float('inf'):
            # Chebyshev distance
            return max(diffs) / normalizer
        if self.params['pval'] == 0:
            # This is the l_0 "norm" as developed by David Donoho
            return sum(_ != 0 for _ in diffs) / normalizer
        return (
            sum(_ ** self.params['pval'] for _ in diffs)
            ** (1 / self.params['pval'])
            / normalizer
        )

    def dist(self, src, tar):
        """Return normalized Minkowski distance of two strings.

        The normalized Minkowski distance :cite:`Minkowski:1910` is a distance
        metric in :math:`L^p`-space, normalized to [0, 1].

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            The normalized Minkowski distance

        Examples
        --------
        >>> cmp = Minkowski()
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
    details='Use the Minkowski.dist_abs method instead.',
)
def minkowski(src, tar, qval=2, pval=1, normalized=False, alphabet=0):
    """Return the Minkowski distance (:math:`L^p`-norm) of two strings.

    This is a wrapper for :py:meth:`Minkowski.dist_abs`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram
    pval : int or float
        The :math:`p`-value of the :math:`L^p`-space
    normalized : bool
        Normalizes to [0, 1] if True
    alphabet : collection or int
        The values or size of the alphabet

    Returns
    -------
    float
        The Minkowski distance

    Examples
    --------
    >>> minkowski('cat', 'hat')
    4.0
    >>> minkowski('Niall', 'Neil')
    7.0
    >>> minkowski('Colin', 'Cuilen')
    9.0
    >>> minkowski('ATCG', 'TAGC')
    10.0

    .. versionadded:: 0.3.0

    """
    return Minkowski(pval=pval, alphabet=alphabet, qval=qval).dist_abs(
        src, tar, normalized=normalized
    )


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Minkowski.dist method instead.',
)
def dist_minkowski(src, tar, qval=2, pval=1, alphabet=0):
    """Return normalized Minkowski distance of two strings.

    This is a wrapper for :py:meth:`Minkowski.dist`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram
    pval : int or float
        The :math:`p`-value of the :math:`L^p`-space
    alphabet : collection or int
        The values or size of the alphabet

    Returns
    -------
    float
        The normalized Minkowski distance

    Examples
    --------
    >>> dist_minkowski('cat', 'hat')
    0.5
    >>> round(dist_minkowski('Niall', 'Neil'), 12)
    0.636363636364
    >>> round(dist_minkowski('Colin', 'Cuilen'), 12)
    0.692307692308
    >>> dist_minkowski('ATCG', 'TAGC')
    1.0

    .. versionadded:: 0.3.0

    """
    return Minkowski(pval=pval, alphabet=alphabet, qval=qval).dist_abs(
        src, tar, normalized=True
    )


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Minkowski.sim method instead.',
)
def sim_minkowski(src, tar, qval=2, pval=1, alphabet=0):
    """Return normalized Minkowski similarity of two strings.

    This is a wrapper for :py:meth:`Minkowski.sim`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram
    pval : int or float
        The :math:`p`-value of the :math:`L^p`-space
    alphabet : collection or int
        The values or size of the alphabet

    Returns
    -------
    float
        The normalized Minkowski similarity

    Examples
    --------
    >>> sim_minkowski('cat', 'hat')
    0.5
    >>> round(sim_minkowski('Niall', 'Neil'), 12)
    0.363636363636
    >>> round(sim_minkowski('Colin', 'Cuilen'), 12)
    0.307692307692
    >>> sim_minkowski('ATCG', 'TAGC')
    0.0

    .. versionadded:: 0.3.0

    """
    return Minkowski(pval=pval, alphabet=alphabet, qval=qval).sim(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
