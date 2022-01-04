# Copyright 2018-2020 by Christopher C. Little.
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

"""abydos.tokenizer._tokenize.

_Tokenizer base class
"""

from collections import Counter, defaultdict
from math import exp, log1p, log2
from typing import (
    Any,
    Callable,
    Counter as TCounter,
    DefaultDict,
    List,
    Optional,
    Set,
    Union,
    cast,
)

__all__ = ['_Tokenizer']


class _Tokenizer:
    """Abstract _Tokenizer class.

    .. versionadded:: 0.4.0
    """

    def __init__(
        self,
        scaler: Optional[Union[str, Callable[[float], float]]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize Tokenizer.

        Parameters
        ----------
        scaler : None, str, or function
            A scaling function for the Counter:

                - None : no scaling
                - 'set' : All non-zero values are set to 1.
                - 'length' : Each token has weight equal to its length.
                - 'length-log' : Each token has weight equal to the log of its
                   length + 1.
                - 'length-exp' : Each token has weight equal to e raised to its
                   length.
                - 'entropy' : Weights are scaled to the (log_2) information
                  entropy of each key's frequency.
                - a callable function : The function is applied to each value
                  in the Counter. Some useful functions include math.exp,
                  math.log1p, math.sqrt, and indexes into interesting integer
                  sequences such as the Fibonacci sequence.


        .. versionadded:: 0.4.0

        """
        super().__init__()

        self._scaler = scaler
        self._tokens = defaultdict(int)  # type: DefaultDict[str, float]
        self._string = ''
        self._ordered_tokens = []  # type: List[str]
        self._ordered_weights = []  # type: List[float]

    def tokenize(self, string: str) -> '_Tokenizer':
        """Tokenize the term and store it.

        The tokenized term is stored as an ordered list and as a defaultdict
        object.

        Parameters
        ----------
        string : str
            The string to tokenize


        .. versionadded:: 0.4.0
        .. versionchanged:: 0.4.1
            Added 'length', 'entropy', and related scalers
        .. versionchanged:: 0.6.0
            Moved scaling & counterizing to separate function

        """
        self._string = string
        self._ordered_tokens = [self._string]
        self._ordered_weights = [1]

        self._scale_and_counterize()
        return self

    def _scale_and_counterize(self) -> None:
        """Scale the tokens and store them in a defaultdict.

        .. versionadded:: 0.6.0

        """
        if self._scaler in {'SSK', 'length', 'length-log', 'length-exp'}:
            self._tokens = defaultdict(float)
            if cast(str, self._scaler)[:6] == 'length':
                self._ordered_weights = [len(_) for _ in self._ordered_tokens]
                if self._scaler == 'length-log':
                    self._ordered_weights = [
                        log1p(_) for _ in self._ordered_weights
                    ]
                elif self._scaler == 'length-exp':
                    self._ordered_weights = [
                        exp(_) for _ in self._ordered_weights
                    ]
            for token, weight in zip(
                self._ordered_tokens, self._ordered_weights
            ):
                self._tokens[token] += weight
        elif self._scaler == 'entropy':
            counts = Counter(self._ordered_tokens)
            n = len(self._ordered_tokens)
            self._tokens = defaultdict(float)
            self._tokens.update(
                {
                    key: -(val / n) * log2(val / n)
                    for key, val in counts.items()
                }
            )
            self._ordered_weights = [
                self._tokens[tok] / counts[tok] for tok in self._ordered_tokens
            ]
        else:
            self._tokens = defaultdict(int)
            self._tokens.update(Counter(self._ordered_tokens))

    def count(self) -> int:
        """Return token count.

        Returns
        -------
        int
            The total count of tokens

        Examples
        --------
        >>> tok = _Tokenizer().tokenize('term')
        >>> tok.count()
        1


        .. versionadded:: 0.4.0

        """
        return sum(self.get_counter().values())

    def count_unique(self) -> int:
        """Return the number of unique elements.

        Returns
        -------
        int
            The number of unique tokens

        Examples
        --------
        >>> tok = _Tokenizer().tokenize('term')
        >>> tok.count_unique()
        1


        .. versionadded:: 0.4.0

        """
        return len(self._tokens.values())

    def get_counter(self) -> TCounter[str]:
        """Return the tokens as a Counter object.

        Returns
        -------
        Counter
            The Counter of tokens

        Examples
        --------
        >>> tok = _Tokenizer().tokenize('term')
        >>> tok.get_counter()
        Counter({'term': 1})


        .. versionadded:: 0.4.0

        """
        if self._scaler == 'set':
            return Counter({key: 1 for key in self._tokens.keys()})
        elif callable(self._scaler):
            return Counter(
                {key: self._scaler(val) for key, val in self._tokens.items()}
            )
        else:
            return Counter(self._tokens)

    def get_set(self) -> Set[str]:
        """Return the unique tokens as a set.

        Returns
        -------
        Counter
            The set of tokens

        Examples
        --------
        >>> tok = _Tokenizer().tokenize('term')
        >>> tok.get_set()
        {'term'}


        .. versionadded:: 0.4.0

        """
        return set(self._tokens.keys())

    def get_list(self) -> List[str]:
        """Return the tokens as an ordered list.

        Returns
        -------
        Counter
            The list of q-grams in the order they were added.

        Examples
        --------
        >>> tok = _Tokenizer().tokenize('term')
        >>> tok.get_list()
        ['term']


        .. versionadded:: 0.4.0

        """
        return self._ordered_tokens

    def __repr__(self) -> str:
        """Return representation of tokens object.

        .. versionadded:: 0.4.0

        """
        return f'{self.__class__.__name__}({str(self._tokens)[27:]}'

    def __and__(self, other: '_Tokenizer') -> TCounter[str]:
        """Return intersection with other tokens.

        .. versionadded:: 0.4.0

        """
        return self.get_counter() & other.get_counter()

    def __add__(self, other: '_Tokenizer') -> TCounter[str]:
        """Return union with other tokens.

        .. versionadded:: 0.4.0

        """
        return self.get_counter() + other.get_counter()

    def __sub__(self, other: '_Tokenizer') -> TCounter[str]:
        """Return difference from other tokens.

        .. versionadded:: 0.4.0

        """
        return self.get_counter() - other.get_counter()


if __name__ == '__main__':
    import doctest

    doctest.testmod()
