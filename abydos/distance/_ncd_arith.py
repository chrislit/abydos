# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.distance._ncd_arith.

NCD using Arithmetic Coding
"""

from typing import Any, Dict, Optional

from ._distance import _Distance
from ..compression import Arithmetic

__all__ = ['NCDarith']


class NCDarith(_Distance):
    """Normalized Compression Distance using arithmetic coding.

    Cf. https://en.wikipedia.org/wiki/Arithmetic_coding

    Normalized compression distance (NCD) :cite:`Cilibrasi:2005`.

    .. versionadded:: 0.3.6
    """

    def __init__(
        self, probs: Optional[Dict[str, tuple]] = None, **kwargs: Any
    ) -> None:
        """Initialize the arithmetic coder object.

        Parameters
        ----------
        probs : dict
            A dictionary trained with :py:meth:`Arithmetic.train`


        .. versionadded:: 0.3.6
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        super(NCDarith, self).__init__(**kwargs)
        self._coder = Arithmetic()
        self._probs = probs

    def dist(self, src: str, tar: str) -> float:
        """Return the NCD between two strings using arithmetic coding.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Compression distance

        Examples
        --------
        >>> cmp = NCDarith()
        >>> cmp.dist('cat', 'hat')
        0.5454545454545454
        >>> cmp.dist('Niall', 'Neil')
        0.6875
        >>> cmp.dist('aluminum', 'Catalan')
        0.8275862068965517
        >>> cmp.dist('ATCG', 'TAGC')
        0.6923076923076923


        .. versionadded:: 0.3.5
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if src == tar:
            return 0.0

        if self._probs is None:
            # lacking a reasonable dictionary, train on the strings themselves
            self._coder.train(src + tar)
        else:
            self._coder.set_probs(self._probs)

        src_comp = self._coder.encode(src)[1]
        tar_comp = self._coder.encode(tar)[1]
        concat_comp = self._coder.encode(src + tar)[1]
        concat_comp2 = self._coder.encode(tar + src)[1]

        return (
            min(concat_comp, concat_comp2) - min(src_comp, tar_comp)
        ) / max(src_comp, tar_comp)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
