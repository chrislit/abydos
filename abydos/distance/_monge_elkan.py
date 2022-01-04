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

Generalized Monge-Elkan similarity & distance
"""

from typing import Any, Callable, Optional, Union

from ._distance import _Distance
from ._levenshtein import Levenshtein
from ..tokenizer import WhitespaceTokenizer, _Tokenizer

__all__ = ['MongeElkan']


class MongeElkan(_Distance):
    r"""Generalized Monge-Elkan similarity.

    For two sets of tokens X and Y, Monge-Elkan similarity :cite:`Monge:1996`
    is defined as:

        .. math::

            sim_{Monge-Elkan}(X, Y) =
            \frac{1}{|X|}\sum_{i=1}^{|X|}\max_{j=1}{|Y|} match(X_i, Y_j)

    The match function above returns 1 if two tokens `match', by one being
    identical to or an abbreviation of the other. If a similarity threshold is
    set during instantiation, this implementation acts somewhat more like the
    original description in :cite:`Monge:1996`. Two tokens whose similarity is
    at or above the threshold are counted as a match and assigned similarity of
    1.0, while those with similarity below the threshold counted as a non-match
    and assigned similarity of 0.0.

    If no threshold value is specified, the Generalized Monge-Elkan method
    described by :cite:`Jimenez:2009` is applied instead, where the value
    returned by the inner similarity function is used directly:

        .. math::

            sim_{Monge-Elkan}(X, Y) =
            \frac{1}{|X|}\sum_{i=1}^{|X|}\max_{j=1}{|Y|} sim(X_i, Y_j)

    By default, the input strings are tokenized on whitespace and each
    component token is compared using normalized Levenshtein distance, with no
    similarity threshold.

    Note: Monge-Elkan is NOT a symmetric similarity algorithm. Thus, the
    similarity of src to tar is not necessarily equal to the similarity of
    tar to src. If the symmetric argument is True, a symmetric value is
    calculated, at the cost of doubling the computation time (since
    :math:`sim_{Monge-Elkan}(src, tar)` and :math:`sim_{Monge-Elkan}(tar, src)`
    are both calculated and then averaged).

    .. versionadded:: 0.3.6
    .. versionchanged:: 0.6.0
        The default tokenizer was changed from QGrams() to
        WhitespaceTokenizer() in order to match Monge & Elkan's paper, and
        a threshold parameter was added to allow both the original &
        generalized versions of this similarity measure.
    """

    def __init__(
        self,
        sim_func: Optional[
            Union[_Distance, Callable[[str, str], float]]
        ] = None,
        symmetric: bool = False,
        tokenizer: Optional[_Tokenizer] = None,
        threshold: Optional[float] = None,
        **kwargs: Any
    ) -> None:
        """Initialize MongeElkan instance.

        Parameters
        ----------
        sim_func : function
            The internal similarity metric to employ. Levenshtein distance is
            employed by default. Jaro, Jaro-Winkler, and Jaccard have also been
            suggested in the literature.
        symmetric : bool
            Return a symmetric similarity measure by averaging the similarities
            given the input strings in both possible orderings.
        tokenizer : _Tokenizer
            A tokenizer instance from the :py:mod:`abydos.tokenizer` package
        threshold : float or None
            A threshold similarity, above which two tokens are considered a
            match, and below which two tokens are considered a non-match.
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super().__init__(**kwargs)
        if isinstance(sim_func, _Distance):
            self._sim_func = sim_func.sim  # type: Callable[[str, str], float]
        elif sim_func is None:
            self._sim_func = Levenshtein().sim
        else:
            self._sim_func = sim_func
        self._symmetric = symmetric
        self._tokenizer = tokenizer if tokenizer else WhitespaceTokenizer()
        self._threshold = threshold

    def sim(self, src: str, tar: str) -> float:
        """Return the Generalized Monge-Elkan similarity of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Generalized Monge-Elkan similarity

        Examples
        --------
        >>> from abydos.tokenizer import QGrams
        >>> cmp = MongeElkan(tokenizer=QGrams())
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

        src_toks = sorted(self._tokenizer.tokenize(src).get_list())
        tar_toks = sorted(self._tokenizer.tokenize(tar).get_list())

        if not src_toks or not tar_toks:
            return 0.0

        sum_of_maxes = 0.0
        for s_tok in src_toks:
            max_sim = 0.0
            for t_tok in tar_toks:
                if self._threshold is not None:
                    if self._sim_func(s_tok, t_tok) >= self._threshold:
                        max_sim = 1.0
                        break
                else:
                    max_sim = max(max_sim, self._sim_func(s_tok, t_tok))
            sum_of_maxes += max_sim
        sim_em = sum_of_maxes / len(src_toks)

        if self._symmetric:
            sum_of_maxes = 0.0
            for t_tok in tar_toks:
                max_sim = 0.0
                for s_tok in src_toks:
                    if self._threshold is not None:
                        if self._sim_func(t_tok, s_tok) >= self._threshold:
                            max_sim = 1.0
                            break
                    else:
                        max_sim = max(max_sim, self._sim_func(t_tok, s_tok))
                sum_of_maxes += max_sim
            sim_rev = sum_of_maxes / len(tar_toks)
            sim_em = (sim_em + sim_rev) / 2

        return sim_em


if __name__ == '__main__':
    import doctest

    doctest.testmod()
