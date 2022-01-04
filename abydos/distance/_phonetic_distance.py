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

"""abydos.distance._phonetic_distance.

Phonetic distance.
"""

from typing import Any, Callable, List, Optional, Sequence, Type, Union

from ._distance import _Distance
from ..fingerprint import _Fingerprint
from ..phonetic import _Phonetic
from ..stemmer import _Stemmer

__all__ = ['PhoneticDistance']


class PhoneticDistance(_Distance):
    """Phonetic distance.

    Phonetic distance applies one or more supplied string transformations to
    words and compares the resulting transformed strings using a supplied
    distance measure.

    A simple example would be to create a 'Soundex distance':

    >>> from abydos.phonetic import Soundex
    >>> soundex = PhoneticDistance(transforms=Soundex())
    >>> soundex.dist('Ashcraft', 'Ashcroft')
    0.0
    >>> soundex.dist('Robert', 'Ashcraft')
    1.0

    .. versionadded:: 0.4.1
    """

    def __init__(
        self,
        transforms: Optional[
            Union[
                Type[_Phonetic],
                Type[_Stemmer],
                Type[_Fingerprint],
                _Phonetic,
                _Stemmer,
                _Fingerprint,
                Callable[[str], str],
                Sequence[
                    Union[
                        Type[_Phonetic],
                        Type[_Stemmer],
                        Type[_Fingerprint],
                        _Phonetic,
                        _Stemmer,
                        _Fingerprint,
                        Callable[[str], str],
                    ]
                ],
            ]
        ] = None,
        metric: Optional[Union[Type[_Distance], _Distance]] = None,
        encode_alpha: bool = False,
        **kwargs: Any
    ) -> None:
        """Initialize PhoneticDistance instance.

        Parameters
        ----------
        transforms : list or _Phonetic or _Stemmer or _Fingerprint or type
            An instance of a subclass of _Phonetic, _Stemmer, or _Fingerprint,
            or a list (or other iterable) of such instances to apply to each
            input word before computing their distance or similarity. If
            omitted, no transformations will be performed.
        metric : _Distance or type
            An instance of a subclass of _Distance, used for computing the
            inputs' distance or similarity after being transformed. If omitted,
            the strings will be compared for identify (returning 0.0 if
            identical, otherwise 1.0, when distance is computed).
        encode_alpha : bool
            Set to true to use the encode_alpha method of phonetic algoritms
            whenever possible.
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.1

        """
        super().__init__(**kwargs)
        self.transforms = []  # type: List[Callable[[str], str]]
        if transforms:
            if isinstance(transforms, Sequence):
                transforms = list(transforms)
            else:
                transforms = [transforms]

            for i, trans in enumerate(transforms):
                if isinstance(trans, (_Phonetic, _Fingerprint, _Stemmer)):
                    continue
                elif isinstance(trans, type) and issubclass(
                    trans, (_Phonetic, _Fingerprint, _Stemmer)
                ):
                    transforms[i] = trans()
                elif callable(trans):
                    continue
                else:
                    raise TypeError(
                        '{} has unknown type {}'.format(trans, type(trans))
                    )

            for trans in transforms:
                if isinstance(trans, _Phonetic):
                    if encode_alpha:
                        self.transforms.append(trans.encode_alpha)
                    else:
                        self.transforms.append(trans.encode)
                elif isinstance(trans, _Fingerprint):
                    self.transforms.append(trans.fingerprint)
                elif isinstance(trans, _Stemmer):
                    self.transforms.append(trans.stem)
                else:  # callable(trans)
                    self.transforms.append(trans)  # type: ignore

        if isinstance(metric, type) and issubclass(metric, _Distance):
            self.metric = metric()  # type: Optional[_Distance]
        elif isinstance(metric, _Distance):
            self.metric = metric
        elif metric is None:
            self.metric = None
        else:
            raise TypeError(
                '{} has unknown type {}'.format(metric, type(metric))
            )

    def dist_abs(self, src: str, tar: str) -> float:
        """Return the Phonetic distance.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float or int
            The Phonetic distance

        Examples
        --------
        >>> from abydos.phonetic import Soundex
        >>> cmp = PhoneticDistance(Soundex())
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        0
        >>> cmp.dist_abs('Colin', 'Cuilen')
        0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        1

        >>> from abydos.distance import Levenshtein
        >>> cmp = PhoneticDistance(transforms=[Soundex], metric=Levenshtein)
        >>> cmp.dist_abs('cat', 'hat')
        1
        >>> cmp.dist_abs('Niall', 'Neil')
        0
        >>> cmp.dist_abs('Colin', 'Cuilen')
        0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        3


        .. versionadded:: 0.4.1

        """
        for trans in self.transforms:
            src = trans(src)
            tar = trans(tar)
        if self.metric:
            return self.metric.dist_abs(src, tar)
        else:
            return int(src != tar)

    def dist(self, src: str, tar: str) -> float:
        """Return the normalized Phonetic distance.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The normalized Phonetic distance

        Examples
        --------
        >>> from abydos.phonetic import Soundex
        >>> cmp = PhoneticDistance(Soundex())
        >>> cmp.dist('cat', 'hat')
        1.0
        >>> cmp.dist('Niall', 'Neil')
        0.0
        >>> cmp.dist('Colin', 'Cuilen')
        0.0
        >>> cmp.dist('ATCG', 'TAGC')
        1.0

        >>> from abydos.distance import Levenshtein
        >>> cmp = PhoneticDistance(transforms=[Soundex], metric=Levenshtein)
        >>> cmp.dist('cat', 'hat')
        0.25
        >>> cmp.dist('Niall', 'Neil')
        0.0
        >>> cmp.dist('Colin', 'Cuilen')
        0.0
        >>> cmp.dist('ATCG', 'TAGC')
        0.75


        .. versionadded:: 0.4.1

        """
        for trans in self.transforms:
            src = trans(src)
            tar = trans(tar)
        if self.metric:
            return self.metric.dist(src, tar)
        else:
            return float(src != tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
