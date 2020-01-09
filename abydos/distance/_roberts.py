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

"""abydos.distance._roberts.

Roberts similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['Roberts']


class Roberts(_TokenDistance):
    r"""Roberts similarity.

    For two multisets X and Y drawn from an alphabet S, Roberts similarity
    :cite:`Roberts:1986` is

        .. math::

            sim_{Roberts}(X, Y) =
            \frac{\Big[\sum_{i \in S} (X_i + Y_i) \cdot
            \frac{min(X_i, Y_i)}{max(X_i, Y_i)}\Big]}
            {\sum_{i \in S} (X_i + Y_i)}

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, **kwargs):
        """Initialize Roberts instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        **kwargs
            Arbitrary keyword arguments

        Other Parameters
        ----------------
        qval : int
            The length of each q-gram. Using this parameter and tokenizer=None
            will cause the instance to use the QGram tokenizer with this
            q value.


        .. versionadded:: 0.4.0

        """
        super(Roberts, self).__init__(tokenizer=tokenizer, **kwargs)

    def sim(self, src, tar):
        """Return the Roberts similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Roberts similarity

        Examples
        --------
        >>> cmp = Roberts()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.36363636363636365
        >>> cmp.sim('aluminum', 'Catalan')
        0.11764705882352941
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        alphabet = self._total().keys()

        return sum(
            (self._src_tokens[i] + self._tar_tokens[i])
            * min(self._src_tokens[i], self._tar_tokens[i])
            / max(self._src_tokens[i], self._tar_tokens[i])
            for i in alphabet
        ) / sum((self._src_tokens[i] + self._tar_tokens[i]) for i in alphabet)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
