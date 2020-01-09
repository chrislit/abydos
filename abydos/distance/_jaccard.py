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

"""abydos.distance._jaccard.

Jaccard similarity coefficient, distance, & Tanimoto coefficient
"""

from math import log2

from deprecation import deprecated

from ._tversky import Tversky
from .. import __version__

__all__ = ['Jaccard', 'dist_jaccard', 'sim_jaccard', 'tanimoto']


class Jaccard(Tversky):
    r"""Jaccard similarity.

    For two sets X and Y, the Jaccard similarity coefficient
    :cite:`Jaccard:1901,Ruzicka:1958` is

        .. math::

            sim_{Jaccard}(X, Y) =
            \frac{|X \cap Y|}{|X \cup Y|}`.

    This is identical to the Tanimoto similarity coefficient
    :cite:`Tanimoto:1958`
    and the Tversky index :cite:`Tversky:1977` for
    :math:`\alpha = \beta = 1`.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{Jaccard} =
            \frac{a}{a+b+c}

    Notes
    -----
    The multiset variant is termed Ellenberg similarity :cite:`Ellenberg:1956`.

    .. versionadded:: 0.3.6

    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize Jaccard instance.

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
        super(Jaccard, self).__init__(
            alpha=1,
            beta=1,
            bias=None,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        r"""Return the Jaccard similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Jaccard similarity

        Examples
        --------
        >>> cmp = Jaccard()
        >>> cmp.sim('cat', 'hat')
        0.3333333333333333
        >>> cmp.sim('Niall', 'Neil')
        0.2222222222222222
        >>> cmp.sim('aluminum', 'Catalan')
        0.0625
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        return super(Jaccard, self).sim(src, tar)

    def tanimoto_coeff(self, src, tar):
        """Return the Tanimoto distance between two strings.

        Tanimoto distance :cite:`Tanimoto:1958` is
        :math:`-log_{2} sim_{Tanimoto}(X, Y)`.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Tanimoto distance

        Examples
        --------
        >>> cmp = Jaccard()
        >>> cmp.tanimoto_coeff('cat', 'hat')
        -1.5849625007211563
        >>> cmp.tanimoto_coeff('Niall', 'Neil')
        -2.1699250014423126
        >>> cmp.tanimoto_coeff('aluminum', 'Catalan')
        -4.0
        >>> cmp.tanimoto_coeff('ATCG', 'TAGC')
        -inf


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        coeff = self.sim(src, tar)
        if coeff != 0:
            return log2(coeff)

        return float('-inf')


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Jaccard.sim method instead.',
)
def sim_jaccard(src, tar, qval=2):
    """Return the Jaccard similarity of two strings.

    This is a wrapper for :py:meth:`Jaccard.sim`.

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
        Jaccard similarity

    Examples
    --------
    >>> sim_jaccard('cat', 'hat')
    0.3333333333333333
    >>> sim_jaccard('Niall', 'Neil')
    0.2222222222222222
    >>> sim_jaccard('aluminum', 'Catalan')
    0.0625
    >>> sim_jaccard('ATCG', 'TAGC')
    0.0


    .. versionadded:: 0.1.0

    """
    return Jaccard(qval=qval).sim(src, tar)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Jaccard.dist method instead.',
)
def dist_jaccard(src, tar, qval=2):
    """Return the Jaccard distance between two strings.

    This is a wrapper for :py:meth:`Jaccard.dist`.

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
        Jaccard distance

    Examples
    --------
    >>> dist_jaccard('cat', 'hat')
    0.6666666666666667
    >>> dist_jaccard('Niall', 'Neil')
    0.7777777777777778
    >>> dist_jaccard('aluminum', 'Catalan')
    0.9375
    >>> dist_jaccard('ATCG', 'TAGC')
    1.0


    .. versionadded:: 0.1.0

    """
    return Jaccard(qval=qval).dist(src, tar)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Jaccard.tanimoto_coeff method instead.',
)
def tanimoto(src, tar, qval=2):
    """Return the Tanimoto coefficient of two strings.

    This is a wrapper for :py:meth:`Jaccard.tanimoto_coeff`.

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
        Tanimoto distance

    Examples
    --------
    >>> tanimoto('cat', 'hat')
    -1.5849625007211563
    >>> tanimoto('Niall', 'Neil')
    -2.1699250014423126
    >>> tanimoto('aluminum', 'Catalan')
    -4.0
    >>> tanimoto('ATCG', 'TAGC')
    -inf


    .. versionadded:: 0.1.0

    """
    return Jaccard(qval=qval).tanimoto_coeff(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
