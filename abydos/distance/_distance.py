# Copyright 2018-2022 by Christopher C. Little.
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

"""abydos.distance._distance.

The distance._distance module implements abstract class _Distance.
"""
from typing import Any, Dict

__all__ = ['_Distance']


class _Distance:
    """Abstract Distance class.

    .. versionadded:: 0.3.6
    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize _Distance instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        self.params = {}  # type: Dict[str, Any]
        self.set_params(**kwargs)

    def set_params(self, **kwargs: Any) -> None:
        """Store params in the params dict.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.0

        """
        for key in kwargs:
            self.params[key] = kwargs[key]

    def sim(self, src: str, tar: str) -> float:
        """Return similarity.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Similarity


        .. versionadded:: 0.3.6

        """
        return 1.0 - self.dist(src, tar)

    def dist(self, src: str, tar: str) -> float:
        """Return distance.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Distance


        .. versionadded:: 0.3.6

        """
        return 1.0 - self.sim(src, tar)

    def dist_abs(self, src: str, tar: str) -> float:
        """Return absolute distance.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        int
            Absolute distance


        .. versionadded:: 0.3.6

        """
        return self.dist(src, tar)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
