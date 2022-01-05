# Copyright 2014-2022 by Christopher C. Little.
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

"""abydos.util.

The util module defines various utility functions not for other modules within
Abydos (and not intended for use by users), including:

    - _prod -- computes the product of a collection of numbers (akin to sum)
    - _ncr -- computes n Choose r


The util module also contains data downloading facilities. Currently, Abydos
data includes corpora and keymaps. Corpora are used for some distance measures,
such as SoftTF-IDF. The corpora available for Abydos are Q-Gram corpora based
on large datasets, such as Google Books N-Grams and WikiText.

Keymaps are used by the TypoAdvanced distance measure to represent different
international keyboards for different platforms.

The four functions in this module are:

- package_path
- list_available_packages
- list_installed_packages
- download_package

``package_path`` identifies where a given package is located on the system.

``list_available_packages`` lists all packages available in the package
repository (on GitHub). It requires an active internet connection.

``list_installed_packages`` lists all packages currently installed on the
system.

``download_package`` downloads a single package or a collection of packages
from the package repository. It requires an active internet connection.

To install all corpora, you can call ``download_package('qgram_corpora')``. To
install all keymaps, you can call ``download_package('keymaps')``. And to
install all packages, you can call ``download_package('all')``.


----

"""

from ._data import (
    data_path,
    download_package,
    list_available_packages,
    list_installed_packages,
    package_path,
)

__all__ = [
    'data_path',
    'download_package',
    'list_available_packages',
    'list_installed_packages',
    'package_path',
]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
