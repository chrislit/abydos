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

"""abydos.distance._rouge_s.

Rouge-S similarity
"""

from ._distance import _Distance
from ..tokenizer import QSkipgrams
from ..util._ncr import _ncr

__all__ = ['RougeS']


class RougeS(_Distance):
    r"""Rouge-S similarity.

    Rouge-S similarity :cite:`Lin:2004`, operating on character-level skipgrams

    .. versionadded:: 0.4.0
    """

    def __init__(self, qval=2, **kwargs):
        """Initialize RougeS instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(RougeS, self).__init__(**kwargs)
        self._qval = qval
        self._tokenizer = QSkipgrams(qval=qval, start_stop='')

    def sim(self, src, tar, beta=8):
        """Return the Rouge-S similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        beta : int or float
            A weighting factor to prejudice similarity towards src

        Returns
        -------
        float
            Rouge-S similarity

        Examples
        --------
        >>> cmp = RougeS()
        >>> cmp.sim('cat', 'hat')
        0.3333333333333333
        >>> cmp.sim('Niall', 'Neil')
        0.30185758513931893
        >>> cmp.sim('aluminum', 'Catalan')
        0.10755653612796467
        >>> cmp.sim('ATCG', 'TAGC')
        0.6666666666666666


        .. versionadded:: 0.4.0

        """
        if src == tar:
            return 1.0

        qsg_src = self._tokenizer.tokenize(src).get_counter()
        qsg_tar = self._tokenizer.tokenize(tar).get_counter()
        intersection = sum((qsg_src & qsg_tar).values())

        if intersection:
            r_skip = intersection / _ncr(len(src), self._qval)
            p_skip = intersection / _ncr(len(tar), self._qval)
        else:
            return 0.0

        beta_sq = beta * beta

        return (1 + beta_sq) * r_skip * p_skip / (r_skip + beta_sq * p_skip)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
