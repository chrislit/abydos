# Copyright 2019-2022 by Christopher C. Little.
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

"""abydos.distance._sift4_extended.

Sift4 Extended approximate string distance
"""

from typing import Any, Callable, Dict, List, Optional, Union

from ._distance import _Distance
from ._sift4 import Sift4
from ..tokenizer import CharacterTokenizer, _Tokenizer

__all__ = ['Sift4Extended']


class Sift4Extended(_Distance):
    r"""Sift4 Extended version.

    This is an approximation of edit distance, described in
    :cite:`Zackwehdex:2014`.

    .. versionadded:: 0.4.0
    """

    _sift4 = Sift4()

    def __init__(
        self,
        max_offset: int = 5,
        max_distance: int = 0,
        tokenizer: Optional[_Tokenizer] = None,
        token_matcher: Optional[Callable[[str, str], bool]] = None,
        matching_evaluator: Optional[Callable[[str, str], float]] = None,
        local_length_evaluator: Optional[Callable[[float], float]] = None,
        transposition_cost_evaluator: Optional[
            Callable[[int, int], float]
        ] = None,
        transpositions_evaluator: Optional[
            Callable[[float, float], float]
        ] = None,
        **kwargs: Any
    ) -> None:
        """Initialize Sift4Extended instance.

        Parameters
        ----------
        max_offset : int
            The number of characters to search for matching letters
        max_distance : int
            The distance at which to stop and exit
        tokenizer : _Tokenizer
            A tokenizer instance (character tokenization by default)
        token_matcher : function
            A token matcher function of two parameters (equality by default).
            :math:`Sift4Extended.sift4_token_matcher` is also supplied.
        matching_evaluator : function
            A token match quality function of two parameters (1 by default).
            :math:`Sift4Extended.sift4_matching_evaluator` is also supplied.
        local_length_evaluator : function
            A local length evaluator function (its single parameter by
            default). :math:`Sift4Extended.reward_length_evaluator` and
            :math:`Sift4Extended.reward_length_evaluator_exp` are also
            supplied.
        transposition_cost_evaluator : function
            A transposition cost evaluator function of two parameters (1 by
            default).
            :math:`Sift4Extended.longer_transpositions_are_more_costly` is also
            supplied.
        transpositions_evaluator : function
            A transpositions evaluator function of two parameters (the second
            parameter subtracted from the first, by default).
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        super().__init__(**kwargs)
        self._max_offset = max_offset
        self._max_distance = max_distance

        if tokenizer is not None:
            self._tokenizer = tokenizer
        else:
            self._tokenizer = CharacterTokenizer()

        if token_matcher is not None:
            self._token_matcher = token_matcher
        else:
            self._token_matcher = lambda t1, t2: t1 == t2

        if matching_evaluator is not None:
            self._matching_evaluator = matching_evaluator
        else:
            self._matching_evaluator = lambda t1, t2: 1

        if local_length_evaluator is not None:
            self._local_length_evaluator = local_length_evaluator
        else:
            self._local_length_evaluator = lambda local_cs: local_cs

        if transposition_cost_evaluator is not None:
            self._transposition_cost_evaluator = transposition_cost_evaluator
        else:
            self._transposition_cost_evaluator = lambda c1, c2: 1

        if transpositions_evaluator is not None:
            self._transpositions_evaluator = transpositions_evaluator
        else:
            self._transpositions_evaluator = lambda lcss, trans: lcss - trans

    def dist_abs(self, src: str, tar: str) -> float:
        """Return the Sift4 Extended distance between two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int
            The Sift4 distance according to the extended formula

        Examples
        --------
        >>> cmp = Sift4Extended()
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        2
        >>> cmp.dist_abs('aluminum', 'Catalan')
        5
        >>> cmp.dist_abs('ATCG', 'TAGC')
        2


        .. versionadded:: 0.4.0

        """
        src_list = self._tokenizer.tokenize(src).get_list()
        tar_list = self._tokenizer.tokenize(tar).get_list()

        if not src_list:
            return len(tar_list)

        if not tar_list:
            return len(src_list)

        src_len = len(src_list)
        tar_len = len(tar_list)

        src_cur = 0
        tar_cur = 0
        lcss = 0.0
        local_cs = 0.0
        trans = 0.0
        offset_arr = []  # type: List[Dict[str, Union[int, bool]]]

        while (src_cur < src_len) and (tar_cur < tar_len):
            if self._token_matcher(src_list[src_cur], tar_list[tar_cur]):
                local_cs += self._matching_evaluator(
                    src_list[src_cur], tar_list[tar_cur]
                )
                is_trans = False
                i = 0
                while i < len(offset_arr):
                    ofs = offset_arr[i]
                    if src_cur <= ofs['src_cur'] or tar_cur <= ofs['tar_cur']:
                        is_trans = abs(tar_cur - src_cur) >= abs(
                            ofs['tar_cur'] - ofs['src_cur']
                        )
                        if is_trans:
                            trans += self._transposition_cost_evaluator(
                                src_cur, tar_cur
                            )
                        elif not ofs['trans']:
                            ofs['trans'] = True
                            trans += self._transposition_cost_evaluator(
                                ofs['tar_cur'], ofs['src_cur']
                            )
                        break
                    elif src_cur > ofs['tar_cur'] and tar_cur > ofs['src_cur']:
                        del offset_arr[i]
                    else:
                        i += 1

                offset_arr.append(
                    {'src_cur': src_cur, 'tar_cur': tar_cur, 'trans': is_trans}
                )
            else:
                lcss += self._local_length_evaluator(local_cs)
                local_cs = 0
                if src_cur != tar_cur:
                    src_cur = tar_cur = min(src_cur, tar_cur)
                for i in range(self._max_offset):
                    if not (
                        (src_cur + i < src_len) or (tar_cur + i < tar_len)
                    ):
                        break
                    if (src_cur + i < src_len) and (
                        self._token_matcher(
                            src_list[src_cur + i], tar_list[tar_cur]
                        )
                    ):
                        src_cur += i - 1
                        tar_cur -= 1
                        break
                    if (tar_cur + i < tar_len) and (
                        self._token_matcher(
                            src_list[src_cur], tar_list[tar_cur + i]
                        )
                    ):
                        src_cur -= 1
                        tar_cur += i - 1
                        break

            src_cur += 1
            tar_cur += 1

            if self._max_distance:
                temporary_distance = self._local_length_evaluator(
                    max(src_cur, tar_cur)
                ) - self._transpositions_evaluator(lcss, trans)
                if temporary_distance >= self._max_distance:
                    return round(temporary_distance)

            if (src_cur >= src_len) or (tar_cur >= tar_len):
                lcss += self._local_length_evaluator(local_cs)
                local_cs = 0
                src_cur = tar_cur = min(src_cur, tar_cur)

        lcss += self._local_length_evaluator(local_cs)
        return round(
            self._local_length_evaluator(max(src_len, tar_len))
            - self._transpositions_evaluator(lcss, trans)
        )

    @staticmethod
    def sift4_token_matcher(src: str, tar: str) -> bool:
        """Sift4 Token Matcher.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        bool
            Whether the Sift4 similarity of the two tokens is over 0.7

        .. versionadded:: 0.4.0

        """
        return Sift4Extended.sift4_matching_evaluator(src, tar) > 0.7

    @staticmethod
    def sift4_matching_evaluator(src: str, tar: str) -> float:
        """Sift4 Matching Evaluator.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The Sift4 similarity of the two tokens

        .. versionadded:: 0.4.0

        """
        return Sift4Extended._sift4.sim(src, tar)

    @staticmethod
    def reward_length_evaluator(length: int) -> float:
        """Reward Length Evaluator.

        Parameters
        ----------
        length : int
            The length of a local match

        Returns
        -------
        float
            A reward value that grows sub-linearly

        .. versionadded:: 0.4.0

        """
        if length < 1:
            return 1
        return length - 1 / (length + 1)

    @staticmethod
    def reward_length_evaluator_exp(length: int) -> float:
        """Reward Length Evaluator.

        Parameters
        ----------
        length : int
            The length of a local match

        Returns
        -------
        float
            A reward value that grows exponentially

        .. versionadded:: 0.4.0

        """
        return length ** 1.5

    @staticmethod
    def longer_transpositions_are_more_costly(pos1: int, pos2: int) -> float:
        """Longer Transpositions Are More Costly.

        Parameters
        ----------
        pos1 : int
            The position of the first transposition
        pos2 : int
            The position of the second transposition

        Returns
        -------
        float
            A cost that grows as difference in the positions increases

        .. versionadded:: 0.4.0

        """
        return abs(pos2 - pos1) / 9 + 1


if __name__ == '__main__':
    import doctest

    doctest.testmod()
