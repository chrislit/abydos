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

"""abydos.distance._millar.

Millar's binomial deviance dissimilarity
"""

from math import log

from ._token_distance import _TokenDistance

__all__ = ['Millar']


class Millar(_TokenDistance):
    r"""Millar's binomial deviance dissimilarity.

    For two sets X and Y drawn from a population S, Millar's binomial deviance
    dissimilarity :cite:`Anderson:2004` is:

        .. math::

            dist_{Millar}(X, Y) = \sum_{i=0}^{|S|} \frac{1}{x_i+y_i}
            \bigg\{x_i log(\frac{x_i}{x_i+y_i}) + y_i log(\frac{y_i}{x_i+y_i})
            - (x_i+y_i) log(\frac{1}{2})\bigg\}


    .. versionadded:: 0.4.1
    """

    def __init__(self, **kwargs):
        """Initialize Millar instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.1

        """
        super(Millar, self).__init__(**kwargs)

    def dist_abs(self, src, tar):
        """Return Millar's binomial deviance dissimilarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Millar's binomial deviance dissimilarity

        Examples
        --------
        >>> cmp = Millar()
        >>> cmp.dist_abs('cat', 'hat')
        2.772588722239781
        >>> cmp.dist_abs('Niall', 'Neil')
        4.852030263919617
        >>> cmp.dist_abs('aluminum', 'Catalan')
        9.704060527839234
        >>> cmp.dist_abs('ATCG', 'TAGC')
        6.931471805599453


        .. versionadded:: 0.4.1

        """
        self._tokenize(src, tar)

        src_tok = self._src_tokens
        tar_tok = self._tar_tokens
        alphabet = set(src_tok.keys() | tar_tok.keys())

        log2 = log(2)
        score = 0
        for tok in alphabet:
            n_k = src_tok[tok] + tar_tok[tok]

            src_val = 0
            if src_tok[tok]:
                src_val = src_tok[tok] * log(src_tok[tok] / n_k)

            tar_val = 0
            if tar_tok[tok]:
                tar_val = tar_tok[tok] * log(tar_tok[tok] / n_k)

            score += (src_val + tar_val + n_k * log2) / n_k

        if score > 0:
            return score
        return 0.0

    def sim(self, *args, **kwargs):
        """Raise exception when called.

        Parameters
        ----------
        *args
            Variable length argument list
        **kwargs
            Arbitrary keyword arguments

        Raises
        ------
        NotImplementedError
            Method disabled for Millar dissimilarity.


        .. versionadded:: 0.3.6

        """
        raise NotImplementedError('Method disabled for Millar dissimilarity.')

    def dist(self, *args, **kwargs):
        """Raise exception when called.

        Parameters
        ----------
        *args
            Variable length argument list
        **kwargs
            Arbitrary keyword arguments

        Raises
        ------
        NotImplementedError
            Method disabled for Millar dissimilarity.


        .. versionadded:: 0.3.6

        """
        raise NotImplementedError('Method disabled for Millar dissimilarity.')


if __name__ == '__main__':
    import doctest

    doctest.testmod()
