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

"""abydos.distance._monge_elkan.

Monge-Elkan similarity & distance
"""

from typing import Any, Callable, Optional, Union

from ._distance import _Distance
from ._levenshtein import Levenshtein
from ..tokenizer import QGrams

__all__ = ['MongeElkan']


class MongeElkan(_Distance):
    """Monge-Elkan similarity.

    Monge-Elkan is defined in :cite:`Monge:1996`.

    Note: Monge-Elkan is NOT a symmetric similarity algorithm. Thus, the
    similarity of src to tar is not necessarily equal to the similarity of
    tar to src. If the symmetric argument is True, a symmetric value is
    calculated, at the cost of doubling the computation time (since
    :math:`sim_{Monge-Elkan}(src, tar)` and :math:`sim_{Monge-Elkan}(tar, src)`
    are both calculated and then averaged).

    .. versionadded:: 0.3.6
    """

    def __init__(
        self,
        sim_func: Optional[
            Union[_Distance, Callable[[str, str], float]]
        ] = None,
        symmetric: bool = False,
        **kwargs: Any
    ) -> None:
        """Initialize MongeElkan instance.

        Parameters
        ----------
        sim_func : function
            The internal similarity metric to employ
        symmetric : bool
            Return a symmetric similarity measure
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super(MongeElkan, self).__init__(**kwargs)
        if isinstance(sim_func, _Distance):
            self._sim_func = sim_func.sim  # type: Callable[[str, str], float]
        elif sim_func is None:
            self._sim_func = Levenshtein().sim
        else:
            self._sim_func = sim_func
        self._symmetric = symmetric

    def sim(self, src: str, tar: str) -> float:
        """Return the Monge-Elkan similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Monge-Elkan similarity

        Examples
        --------
        >>> cmp = MongeElkan()
        >>> cmp.sim('cat', 'hat')
        0.75
        >>> round(cmp.sim('Niall', 'Neil'), 12)
        0.666666666667
        >>> round(cmp.sim('aluminum', 'Catalan'), 12)
        0.388888888889
        >>> cmp.sim('ATCG', 'TAGC')
        0.5


        .. versionadded:: 0.1.0
        .. versionchanged:: 0.3.6
            Encapsulated in class

        """
        if src == tar:
            return 1.0

        q_src = sorted(QGrams().tokenize(src).get_list())
        q_tar = sorted(QGrams().tokenize(tar).get_list())

        if not q_src or not q_tar:
            return 0.0

        sum_of_maxes = 0.0
        for q_s in q_src:
            max_sim = float('-inf')
            for q_t in q_tar:
                max_sim = max(max_sim, self._sim_func(q_s, q_t))
            sum_of_maxes += max_sim
        sim_em = sum_of_maxes / len(q_src)

        if self._symmetric:
            sum_of_maxes = 0.0
            for q_t in q_tar:
                max_sim = float('-inf')
                for q_s in q_src:
                    max_sim = max(max_sim, self._sim_func(q_t, q_s))
                sum_of_maxes += max_sim
            sim_rev = sum_of_maxes / len(q_tar)
            sim_em = (sim_em + sim_rev) / 2

        return sim_em


if __name__ == '__main__':
    import doctest

    doctest.testmod()
