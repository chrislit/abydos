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

"""abydos.distance._dice.

Sørensen–Dice coefficient & distance
"""

from deprecation import deprecated

from ._tversky import Tversky
from .. import __version__

__all__ = ['Dice', 'dist_dice', 'sim_dice']


class Dice(Tversky):
    r"""Sørensen–Dice coefficient.

    For two sets X and Y, the Sørensen–Dice coefficient
    :cite:`Dice:1945,Sorensen:1948,Czekanowski:1909,Motyka:1950` is

        .. math::

            sim_{Dice}(X, Y) = \frac{2 \cdot |X \cap Y|}{|X| + |Y|}

    This is the complement of Bray & Curtis dissimilarity :cite:`Bray:1957`,
    also known as the Lance & Williams dissimilarity :cite:`Lance:1967`.

    This is identical to the Tanimoto similarity coefficient
    :cite:`Tanimoto:1958` and the Tversky index :cite:`Tversky:1977` for
    :math:`\alpha = \beta = 0.5`.

    In the Ruby text library this is identified as White similarity, after
    :cite:`White:Nd`.

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{Dice} =
            \frac{2a}{2a+b+c}

    Notes
    -----
    In terms of a confusion matrix, this is equivalent to :math:`F_1` score
    :py:meth:`ConfusionTable.f1_score`.

    The multiset variant is termed Gleason similarity :cite:`Gleason:1920`.

    .. versionadded:: 0.3.6

    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize Dice instance.

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
        super(Dice, self).__init__(
            alpha=0.5,
            beta=0.5,
            bias=None,
            tokenizer=tokenizer,
            intersection_type=intersection_type,
            **kwargs
        )

    def sim(self, src, tar):
        """Return the Sørensen–Dice coefficient of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Sørensen–Dice similarity

        Examples
        --------
        >>> cmp = Dice()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.36363636363636365
        >>> cmp.sim('aluminum', 'Catalan')
        0.11764705882352941
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        return super(Dice, self).sim(src, tar)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Dice.sim method instead.',
)
def sim_dice(src, tar, qval=2):
    """Return the Sørensen–Dice coefficient of two strings.

    This is a wrapper for :py:meth:`Dice.sim`.

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
        Sørensen–Dice similarity

    Examples
    --------
    >>> sim_dice('cat', 'hat')
    0.5
    >>> sim_dice('Niall', 'Neil')
    0.36363636363636365
    >>> sim_dice('aluminum', 'Catalan')
    0.11764705882352941
    >>> sim_dice('ATCG', 'TAGC')
    0.0

    .. versionadded:: 0.1.0

    """
    return Dice(qval=qval).sim(src, tar)


@deprecated(
    deprecated_in='0.4.0',
    removed_in='0.6.0',
    current_version=__version__,
    details='Use the Dice.dist method instead.',
)
def dist_dice(src, tar, qval=2):
    """Return the Sørensen–Dice distance between two strings.

    This is a wrapper for :py:meth:`Dice.dist`.

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
        Sørensen–Dice distance

    Examples
    --------
    >>> dist_dice('cat', 'hat')
    0.5
    >>> dist_dice('Niall', 'Neil')
    0.6363636363636364
    >>> dist_dice('aluminum', 'Catalan')
    0.8823529411764706
    >>> dist_dice('ATCG', 'TAGC')
    1.0

    .. versionadded:: 0.1.0

    """
    return Dice(qval=qval).dist(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
