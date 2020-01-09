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

"""abydos.distance._quantitative_cosine.

Quantitative Cosine similarity
"""

from ._token_distance import _TokenDistance

__all__ = ['QuantitativeCosine']


class QuantitativeCosine(_TokenDistance):
    r"""Quantitative Cosine similarity.

    For two multisets X and Y drawn from an alphabet S, Quantitative Cosine
    similarity is

        .. math::

            sim_{QuantitativeCosine}(X, Y) =
            \frac{\sum_{i \in S} X_iY_i}
            {\sqrt{\sum_{i \in S} X_i^2}\sqrt{\sum_{i \in S} Y_i^2}}

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, **kwargs):
        """Initialize QuantitativeCosine instance.

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
        super(QuantitativeCosine, self).__init__(tokenizer=tokenizer, **kwargs)

    def sim(self, src, tar):
        """Return the Quantitative Cosine similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            Quantitative Cosine similarity

        Examples
        --------
        >>> cmp = QuantitativeCosine()
        >>> cmp.sim('cat', 'hat')
        0.5
        >>> cmp.sim('Niall', 'Neil')
        0.3651483716701107
        >>> cmp.sim('aluminum', 'Catalan')
        0.10660035817780521
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        self._tokenize(src, tar)

        if not self._src_card() or not self._tar_card():
            return 0.0

        alphabet = self._total().keys()

        return sum(
            self._src_tokens[tok] * self._tar_tokens[tok] for tok in alphabet
        ) / (
            sum(
                self._src_tokens[tok] * self._src_tokens[tok]
                for tok in alphabet
            )
            ** 0.5
            * sum(
                self._tar_tokens[tok] * self._tar_tokens[tok]
                for tok in alphabet
            )
            ** 0.5
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
