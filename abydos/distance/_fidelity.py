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

"""abydos.distance._fidelity.

Fidelity
"""

from ._token_distance import _TokenDistance

__all__ = ['Fidelity']


class Fidelity(_TokenDistance):
    r"""Fidelity.

    For two multisets X and Y drawn from an alphabet S, fidelity is

        .. math::

            sim_{Fidelity}(X, Y) =
            \Bigg( \sum_{i \in S} \sqrt{|\frac{A_i}{|A|} \cdot
            \frac{B_i}{|B|}|} \Bigg)^2

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, **kwargs):
        """Initialize Fidelity instance.

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
        super(Fidelity, self).__init__(tokenizer=tokenizer, **kwargs)

    def sim(self, src, tar):
        """Return the fidelity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            fidelity

        Examples
        --------
        >>> cmp = Fidelity()
        >>> cmp.sim('cat', 'hat')
        0.25
        >>> cmp.sim('Niall', 'Neil')
        0.1333333333333333
        >>> cmp.sim('aluminum', 'Catalan')
        0.013888888888888888
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.0

        """
        self._tokenize(src, tar)

        alphabet = self._total().keys()
        src_mag = max(1, sum(self._src_tokens.values()))
        tar_mag = max(1, sum(self._tar_tokens.values()))

        return (
            sum(
                (
                    abs(
                        self._src_tokens[tok]
                        / src_mag
                        * self._tar_tokens[tok]
                        / tar_mag
                    )
                )
                ** 0.5
                for tok in alphabet
            )
            ** 2
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
