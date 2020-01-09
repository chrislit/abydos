# Copyright 2019-2020 by Christopher C. Little.
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

"""abydos.distance._q_gram.

q-gram distance
"""

from ._token_distance import _TokenDistance
from ..tokenizer import QGrams as QGramTokenizer

__all__ = ['QGram']


class QGram(_TokenDistance):
    r"""q-gram distance.

    For two multisets X and Y, q-gram distance
    :cite:`Ukkonen:1992` is

        .. math::

            sim_{QGram}(X, Y) = |X \triangle Y|

    In :ref:`2x2 confusion table terms <confusion_table>`, where a+b+c+d=n,
    this is

        .. math::

            sim_{QGram} = b+c

    Notes
    -----
    This class uses bigrams without appended start or stop symbols, by default,
    as in :cite:`Ukkonen:1992`'s examples. It is described as the :math:`L_1`
    norm of the difference of two strings' q-gram profiles, which are the
    vectors of q-gram occurrences. But this norm is simply the symmetric
    difference of the two multisets.

    There aren't any limitations on which tokenizer is used with this class,
    but, as the name would imply, q-grams are expected and the default.

    The normalized form uses the union of X and Y, making it equivalent to the
    Jaccard distance :py:class:`.Jaccard`, but the Jaccard class, by default
    uses bigrams with start & stop symbols.

    .. versionadded:: 0.4.0

    """

    def __init__(self, tokenizer=None, intersection_type='crisp', **kwargs):
        """Initialize QGram instance.

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
            if 'qval' in kwargs:
                qval = kwargs['qval']
            else:
                qval = 2
            tokenizer = QGramTokenizer(qval=qval, start_stop='')

        super(QGram, self).__init__(
            tokenizer=tokenizer, intersection_type=intersection_type, **kwargs
        )

    def dist_abs(self, src, tar):
        """Return the q-gram distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        int
            q-gram distance

        Examples
        --------
        >>> cmp = QGram()
        >>> cmp.dist_abs('cat', 'hat')
        2
        >>> cmp.dist_abs('Niall', 'Neil')
        7
        >>> cmp.dist_abs('aluminum', 'Catalan')
        11
        >>> cmp.dist_abs('ATCG', 'TAGC')
        6
        >>> cmp.dist_abs('01000', '001111')
        5


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        b = self._src_only_card()
        c = self._tar_only_card()

        return b + c

    def dist(self, src, tar):
        """Return the normalized q-gram distance of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            q-gram distance

        Examples
        --------
        >>> cmp = QGram()
        >>> cmp.sim('cat', 'hat')
        0.33333333333333337
        >>> cmp.sim('Niall', 'Neil')
        0.0
        >>> cmp.sim('aluminum', 'Catalan')
        0.08333333333333337
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        num = self.dist_abs(src, tar)
        if num:
            return num / self._union_card()
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
