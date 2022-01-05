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

"""abydos.tests.util.test_prod.

This module contains unit tests for abydos.util._prod
"""

import shutil
import tempfile
import unittest

from abydos.util._data import (
    download_package,
    list_available_packages,
    list_installed_packages,
    package_path,
)


class DataTestCases(unittest.TestCase):
    """Test cases for abydos.util._prod."""

    DEFAULT_URL = 'https://raw.githubusercontent.com/chrislit/'
    DEFAULT_URL += 'abydos-data/master/index.xml'

    def test_data(self):
        """Test abydos.util._data."""
        self.assertTrue(isinstance(list_installed_packages(), list))
        self.assertTrue(isinstance(list_available_packages(), tuple))
        self.assertTrue(
            isinstance(list_available_packages(url=self.DEFAULT_URL), tuple)
        )

        download_package('all')
        self.assertEqual(
            package_path('wikitext_qgram')[-14:], 'wikitext_qgram'
        )
        with self.assertRaises(FileNotFoundError):
            package_path('not_a_real_package')

        temppath = tempfile.mkdtemp()
        download_package('wikitext_qgram', data_path=temppath, force=True)
        download_package('wikitext_qgram', data_path=temppath)
        shutil.rmtree(temppath)

        with self.assertRaises(ValueError):
            list_available_packages(url='file:///etc/passwd')


if __name__ == '__main__':
    unittest.main()
