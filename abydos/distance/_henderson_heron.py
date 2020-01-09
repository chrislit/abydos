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

"""abydos.distance._henderson_heron.

Henderson-Heron dissimilarity
"""

from math import factorial

from ._token_distance import _TokenDistance

__all__ = ['HendersonHeron']


class HendersonHeron(_TokenDistance):
    r"""Henderson-Heron dissimilarity.

    For two sets X and Y and a population N, Henderson-Heron dissimilarity
    :cite:`Henderson:1977` is:

    .. math:

        sim_{Henderson-Heron}(X, Y) = \frac{|X|! |Y|! (|N| - |X|)!
        (|N|- |Y|)!}{|N|! |X \cap Y|! (|X| - |X \cap Y|)!
        (|Y| - |Y \cap X|)! (|N| - |X| - |Y| + |X \cap Y|)!}

    .. versionadded:: 0.4.1
    """

    def __init__(self, **kwargs):
        """Initialize HendersonHeron instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.1

        """
        super(HendersonHeron, self).__init__(**kwargs)

    def dist(self, src, tar):
        """Return the Henderson-Heron dissimilarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Henderson-Heron dissimilarity

        Examples
        --------
        >>> cmp = HendersonHeron()
        >>> cmp.dist('cat', 'hat')
        0.00011668873858680838
        >>> cmp.dist('Niall', 'Neil')
        0.00048123075776606097
        >>> cmp.dist('aluminum', 'Catalan')
        0.08534181060514882
        >>> cmp.dist('ATCG', 'TAGC')
        0.9684367974410505


        .. versionadded:: 0.4.1

        """
        self._tokenize(src, tar)

        a = self._intersection_card()
        ab = self._src_card()
        ac = self._tar_card()
        n = self._population_unique_card()

        return (
            factorial(ab)
            * factorial(ac)
            * factorial(n - ab)
            * factorial(n - ac)
            / (
                factorial(n)
                * factorial(a)
                * factorial(ab - a)
                * factorial(ac - a)
                * factorial((n - ac - ab + a))
            )
        )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
