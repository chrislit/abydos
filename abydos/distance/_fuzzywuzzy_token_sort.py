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

"""abydos.distance._fuzzywuzzy_token_sort.

FuzzyWuzzy Token Sort similarity
"""

from difflib import SequenceMatcher

from ._token_distance import _TokenDistance
from ..tokenizer import RegexpTokenizer

__all__ = ['FuzzyWuzzyTokenSort']


class FuzzyWuzzyTokenSort(_TokenDistance):
    r"""FuzzyWuzzy Token Sort similarity.

    This follows the FuzzyWuzzy Token Sort similarity algorithm
    :cite:`Cohen:2011`. Rather than returning an integer in the range [0, 100],
    as demonstrated in the blog post, this implementation returns a float in
    the range [0.0, 1.0].

    .. versionadded:: 0.4.0
    """

    def __init__(self, tokenizer=None, **kwargs):
        """Initialize FuzzyWuzzyTokenSort instance.

        Parameters
        ----------
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package.
            By default, the regexp tokenizer is employed, matching only
            letters.
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
        if tokenizer is None:
            tokenizer = RegexpTokenizer()
        super(FuzzyWuzzyTokenSort, self).__init__(
            tokenizer=tokenizer, **kwargs
        )

    def sim(self, src, tar):
        """Return the FuzzyWuzzy Token Sort similarity of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison

        Returns
        -------
        float
            FuzzyWuzzy Token Sort similarity

        Examples
        --------
        >>> cmp = FuzzyWuzzyTokenSort()
        >>> cmp.sim('cat', 'hat')
        0.6666666666666666
        >>> cmp.sim('Niall', 'Neil')
        0.6666666666666666
        >>> cmp.sim('aluminum', 'Catalan')
        0.4
        >>> cmp.sim('ATCG', 'TAGC')
        0.5


        .. versionadded:: 0.4.0

        """
        src = ' '.join(
            sorted(self.params['tokenizer'].tokenize(src).get_list())
        )
        tar = ' '.join(
            sorted(self.params['tokenizer'].tokenize(tar).get_list())
        )

        return SequenceMatcher(None, src, tar).ratio()


if __name__ == '__main__':
    import doctest

    doctest.testmod()
