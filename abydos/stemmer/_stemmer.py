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

"""abydos.stemmer._stemmer.

abstract class _Stemmer
"""

__all__ = ['_Stemmer']


class _Stemmer(object):
    """Abstract Stemmer class.

    .. versionadded:: 0.3.6
    """

    def stem(self, word):
        """Return stem.

        Parameters
        ----------
        word : str
            The word to stem
        *args
            Variable length argument list
        **kwargs
            Arbitrary keyword arguments

        Returns
        -------
        str
            Word stem


        .. versionadded:: 0.3.6

        """
        pass


if __name__ == '__main__':
    import doctest

    doctest.testmod()
