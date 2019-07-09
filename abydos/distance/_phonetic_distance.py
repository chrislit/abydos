# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ._distance import _Distance
from ..fingerprint._fingerprint import _Fingerprint
from ..phonetic._phonetic import _Phonetic
from ..stemmer._stemmer import _Stemmer

__all__ = ['PhoneticDistance']


class PhoneticDistance(_Distance):
    """Phonetic distance.

    Phonetic distance applies one or more supplied string transformations to
    words and compares the resulting transformed strings using a supplied
    distance measure.

    A simple example would be to create a 'Soundex distance':

    >>> soundex = PhoneticDistance(transforms=Soundex())
    >>> soundex.dist(..., ...)
    1.0
    >>> soundex.dist(..., ...)
    0.0

    .. versionadded:: 0.4.1
    """

    def __init__(
        self, transforms=None, metric=None, encode_alpha=False, **kwargs
    ):
        """Initialize PhoneticDistance instance.

        Parameters
        ----------
        transforms : list or _Phonetic or _Stemmer or _Fingerprint
            An instance of a subclass of _Phonetic, _Stemmer, or _Fingerprint,
            or a list (or other iterable) of such instances to apply to each
            input word before computing their distance or similarity. If
            omitted, no transformations will be performed.
        metric : _Distance
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
        super(PhoneticDistance, self).__init__(**kwargs)
        self.transforms = transforms
        if self.transforms:
            if hasattr(self.transforms, '__iter__'):
                self.transforms = list(self.transforms)
                for i, t in enumerate(self.transforms):
                    if isinstance(t, (_Phonetic, _Fingerprint, _Stemmer)):
                        continue
                    elif type(t) == 'type' and issubclass(
                        t, (_Phonetic, _Fingerprint, _Stemmer)
                    ):
                        self.transforms[i] = t()
                    else:
                        raise TypeError('Unknown type ' + str(type(t)))
            else:
                if isinstance(
                    self.transforms, (_Phonetic, _Fingerprint, _Stemmer)
                ):
                    self.transforms = [self.transforms]
                elif type(self.transforms) == 'type' and issubclass(
                    self.transforms, (_Phonetic, _Fingerprint, _Stemmer)
                ):
                    self.transforms = [self.transforms()]
                else:
                    raise TypeError(
                        'Unknown type ' + str(type(self.transforms))
                    )

        for i, t in enumerate(self.transforms):
            if isinstance(t, _Phonetic):
                if encode_alpha:
                    self.transforms[i] = self.transforms[i].encode_alpha
                else:
                    self.transforms[i] = self.transforms[i].encode
            elif isinstance(t, _Fingerprint):
                self.transforms[i] = self.transforms[i].fingerprint
            elif isinstance(t, _Stemmer):
                self.transforms[i] = self.transforms[i].stem

        self.metric = metric
        if type(self.metric) == 'type' and issubclass(
            self.metric, _Distance
        ):
            self.transforms = [self.metric()]
        elif not isinstance(self.metric, _Distance):
            raise TypeError('Unknown type ' + str(type(self.metric)))

    def dist_abs(self, src, tar):
        """Return the Phonetic distance.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            The Phonetic distance

        Examples
        --------
        >>> cmp = PhoneticDistance()
        >>> cmp.dist_abs('cat', 'hat')
        0.666666666667
        >>> cmp.dist_abs('Niall', 'Neil')
        0.4
        >>> cmp.dist_abs('Colin', 'Cuilen')
        0.166666666667
        >>> cmp.dist_abs('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.1

        """
        pass

    def dist(self, src, tar):
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
        >>> cmp = PhoneticDistance()
        >>> cmp.dist('cat', 'hat')
        0.666666666667
        >>> cmp.dist('Niall', 'Neil')
        0.4
        >>> cmp.dist('Colin', 'Cuilen')
        0.166666666667
        >>> cmp.dist('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.1

        """
        pass


if __name__ == '__main__':
    import doctest

    doctest.testmod()
