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

"""abydos.distance._guth.

Guth matching algorithm
"""

from ._distance import _Distance
from ..tokenizer import QGrams

__all__ = ['Guth']


class Guth(_Distance):
    r"""Guth matching.

    Guth matching :cite:`Guth:1976` uses a simple positional matching rule list
    to determine whether two names match. Following the original, the
    :meth:`.sim_score` method returns only 1.0 for matching or 0.0 for
    non-matching.

    The :math:`.sim` mathod instead penalizes more distant matches and never
    outrightly declares two names a non-matching unless no matches can be made
    in the two strings.

    Tokens other than single characters can be matched by specifying a
    tokenizer during initialization or setting the qval parameter.

    .. versionadded:: 0.4.1
    """

    def __init__(self, tokenizer=None, **kwargs):
        """Initialize Guth instance.

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


        .. versionadded:: 0.4.1

        """
        super(Guth, self).__init__(**kwargs)

        self.params['tokenizer'] = tokenizer
        if 'qval' in self.params:
            self.params['tokenizer'] = QGrams(
                qval=self.params['qval'], start_stop='$#', skip=0, scaler=None
            )

    def _token_at(self, name, pos):
        """Return the token of name at position pos.

        Parameters
        ----------
        name : str or list
            A string (or list) from which to return a token
        pos : int
            The position of the token to return

        Returns
        -------
        str
            The requested token or None if the position is invalid


        .. versionadded:: 0.4.1

        """
        if pos < 0:
            return None
        if pos >= len(name):
            return None
        return name[pos]

    def sim_score(self, src, tar):
        """Return the Guth matching score of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Guth matching score (1.0 if matching, otherwise 0.0)

        Examples
        --------
        >>> cmp = Guth()
        >>> cmp.sim_score('cat', 'hat')
        1.0
        >>> cmp.sim_score('Niall', 'Neil')
        1.0
        >>> cmp.sim_score('aluminum', 'Catalan')
        0.0
        >>> cmp.sim_score('ATCG', 'TAGC')
        1.0


        .. versionadded:: 0.4.1

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0

        if self.params['tokenizer']:
            src = self.params['tokenizer'].tokenize(src).get_list()
            tar = self.params['tokenizer'].tokenize(tar).get_list()

        for pos in range(len(src)):
            s = self._token_at(src, pos)
            t = set(tar[max(0, pos - 1) : pos + 3])
            if s and s in t:
                continue

            s = set(src[max(0, pos - 1) : pos + 3])
            t = self._token_at(tar, pos)
            if t and t in s:
                continue

            s = self._token_at(src, pos + 1)
            t = self._token_at(tar, pos + 1)
            if s and t and s == t:
                continue

            s = self._token_at(src, pos + 2)
            t = self._token_at(tar, pos + 2)
            if s and t and s == t:
                continue

            break
        else:
            return 1.0
        return 0.0

    def sim(self, src, tar):
        """Return the relative Guth similarity of two strings.

        This deviates from the algorithm described in :cite:`Guth:1976` in that
        more distant matches are penalized, so that less similar terms score
        lower that more similar terms.

        If no match is found for a particular token in the source string, this
        does not result in an automatic 0.0 score. Rather, the score is further
        penalized towards 0.0.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Relative Guth matching score

        Examples
        --------
        >>> cmp = Guth()
        >>> cmp.sim('cat', 'hat')
        0.8666666666666667
        >>> cmp.sim('Niall', 'Neil')
        0.8800000000000001
        >>> cmp.sim('aluminum', 'Catalan')
        0.4
        >>> cmp.sim('ATCG', 'TAGC')
        0.8


        .. versionadded:: 0.4.1

        """
        if src == tar:
            return 1.0
        if not src or not tar:
            return 0.0

        if self.params['tokenizer']:
            src = self.params['tokenizer'].tokenize(src).get_list()
            tar = self.params['tokenizer'].tokenize(tar).get_list()

        score = 0
        for pos in range(len(src)):
            s = self._token_at(src, pos)
            t = self._token_at(tar, pos)
            if s and t and s == t:
                score += 1.0
                continue

            t = self._token_at(tar, pos + 1)
            if s and t and s == t:
                score += 0.8
                continue

            t = self._token_at(tar, pos + 2)
            if s and t and s == t:
                score += 0.6
                continue

            t = self._token_at(tar, pos - 1)
            if s and t and s == t:
                score += 0.8
                continue

            s = self._token_at(src, pos - 1)
            t = self._token_at(tar, pos)
            if s and t and s == t:
                score += 0.8
                continue

            s = self._token_at(src, pos + 1)
            if s and t and s == t:
                score += 0.8
                continue

            s = self._token_at(src, pos + 2)
            if s and t and s == t:
                score += 0.6
                continue

            s = self._token_at(src, pos + 1)
            t = self._token_at(tar, pos + 1)
            if s and t and s == t:
                score += 0.6
                continue

            s = self._token_at(src, pos + 2)
            t = self._token_at(tar, pos + 2)
            if s and t and s == t:
                score += 0.2
                continue

        return score / len(src)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
