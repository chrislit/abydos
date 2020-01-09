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

"""abydos.distance._clark.

Clark's coefficient of divergence
"""

from ._token_distance import _TokenDistance

__all__ = ['Clark']


class Clark(_TokenDistance):
    r"""Clark's coefficient of divergence.

    For two sets X and Y and a population N, Clark's coefficient of divergence
    :cite:`Clark:1952` is:

        .. math::

            dist_{Clark}(X, Y) = \sqrt{\frac{\sum_{i=0}^{|N|}
            \big(\frac{x_i-y_i}{x_i+y_i}\big)^2}{|N|}}

    .. versionadded:: 0.4.1
    """

    def __init__(self, **kwargs):
        """Initialize Clark instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.1

        """
        super(Clark, self).__init__(**kwargs)

    def dist(self, src, tar):
        """Return Clark's coefficient of divergence of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Clark's coefficient of divergence

        Examples
        --------
        >>> cmp = Clark()
        >>> cmp.dist('cat', 'hat')
        0.816496580927726
        >>> cmp.dist('Niall', 'Neil')
        0.8819171036881969
        >>> cmp.dist('aluminum', 'Catalan')
        0.9660917830792959
        >>> cmp.dist('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.1

        """
        if src == tar:
            return 0.0

        self._tokenize(src, tar)

        src_tok = self._src_tokens
        tar_tok = self._tar_tokens
        alphabet = set(src_tok.keys() | tar_tok.keys())

        return (
            sum(
                ((src_tok[ltr] - tar_tok[ltr]) / (src_tok[ltr] + tar_tok[ltr]))
                ** 2
                for ltr in alphabet
            )
            / len(alphabet)
        ) ** 0.5


if __name__ == '__main__':
    import doctest

    doctest.testmod()
