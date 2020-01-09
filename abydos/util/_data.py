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

"""abydos.util._data.

The util._data module manages datasets from
https://github.com/chrislit/abydos-data, including downloading them,
decompressing them, and locating them once installed.

Much of this is copied from NLTK's similar facility in
http://www.nltk.org/_modules/nltk/data.html, because they seem to have the
issues figured out, because I don't want to expend the effort to re-invent a
solution, and because their license (Apache) allows for it.
"""

import os
import re
import sys

try:
    import urllib.request as urllib
except ImportError:  # pragma: no cover
    import urllib
import zipfile

from xml.etree import ElementTree  # noqa: S405

__all__ = [
    'data_path',
    'download_package',
    'list_available_packages',
    'list_installed_packages',
    'package_path',
]


DATA_SUBDIRS = ['corpora']
INDEX_URL = (
    'https://raw.githubusercontent.com/chrislit/abydos-data/master/index.xml'
)

data_path = []
"""A list of directories where the Abydos data package might reside.
   These directories will be checked in order when looking for a
   resource in the data package.  Note that this allows users to
   substitute in their own versions of resources, if they have them
   (e.g., in their home directory under ~/abydos_data)."""

# User-specified locations:
_paths_from_env = os.environ.get('ABYDOS_DATA', str('')).split(
    os.pathsep
)  # pragma: no cover
data_path += [d for d in _paths_from_env if d]
if 'APPENGINE_RUNTIME' not in os.environ and os.path.expanduser('~/') != '~/':
    data_path.append(os.path.expanduser(str('~/abydos_data')))

if sys.platform.startswith('win'):  # pragma: no cover
    # Common locations on Windows:
    data_path += [
        os.path.join(sys.prefix, str('abydos_data')),
        os.path.join(sys.prefix, str('share'), str('abydos_data')),
        os.path.join(sys.prefix, str('lib'), str('abydos_data')),
        os.path.join(
            os.environ.get(str('APPDATA'), str('C:\\')), str('abydos_data')
        ),
        str(r'C:\abydos_data'),
        str(r'D:\abydos_data'),
        str(r'E:\abydos_data'),
    ]
else:
    # Common locations on UNIX & OS X:
    data_path += [
        os.path.join(sys.prefix, str('abydos_data')),
        os.path.join(sys.prefix, str('share'), str('abydos_data')),
        os.path.join(sys.prefix, str('lib'), str('abydos_data')),
        str('/usr/share/abydos_data'),
        str('/usr/local/share/abydos_data'),
        str('/usr/lib/abydos_data'),
        str('/usr/local/lib/abydos_data'),
    ]


def package_path(resource_name):
    """Given a resource name, returns the path to the package."""
    for path in data_path:
        for subdir in DATA_SUBDIRS:
            check_path = os.path.join(path, subdir, resource_name)
            if os.path.isdir(check_path):
                return check_path
    msg = 'Data package not found. You may need to install or re-install it.'
    raise FileNotFoundError(msg)


def list_installed_packages(path=None):
    """List all installed data packages."""
    if path:
        paths = [path]
    else:
        paths = data_path
    packages = []
    for path in paths:
        for subdir in DATA_SUBDIRS:
            check_path = os.path.join(path, subdir)
            if os.path.isdir(check_path):
                possible_packages = os.listdir(check_path)
                for package in possible_packages:
                    if os.path.isdir(os.path.join(check_path, package)):
                        with open(
                            os.path.join(check_path, package + '.xml')
                        ) as xml:
                            file = xml.read()
                            name = re.search(r'name="([^"]+)"', file).group(1)
                            version = re.search(
                                r'version="([^"]+)"', file
                            ).group(1)
                        packages.append((package, name, float(version)))
    return packages


def list_available_packages(url=None):
    """List all data packages available for install."""
    installed_packages = {_[0]: _[2] for _ in list_installed_packages()}

    if url is None:
        url = INDEX_URL
    if url[:8] != 'https://':
        raise ValueError('url should begin with "https://"')
    with urllib.urlopen(url) as ix:  # noqa: S310
        xml = ElementTree.fromstring(ix.read())  # noqa: S314

    packages = [
        (
            _.attrib['id'],
            _.attrib['name'],
            float(_.attrib['version']),
            _.attrib['url'],
            _.attrib['subdir'],
            'not-installed'
            if _.attrib['id'] not in installed_packages
            else (
                'up-to-date'
                if installed_packages[_.attrib['id']]
                >= float(_.attrib['version'])
                else 'update available'
            ),
        )
        for _ in xml.findall('packages/package')
    ]
    collections = [
        (
            _.attrib['id'],
            _.attrib['name'],
            [__.attrib['ref'] for __ in _.findall('item')],
        )
        for _ in xml.findall('collections/collection')
    ]
    return packages, collections


def _default_download_dir():
    """Return the directory to which packages will be downloaded by default.

    This is mostly copied from NLTK's
    nltk.downloader.Downloader.default_download_dir

    """
    # Check if we are on GAE where we cannot write into filesystem.
    if 'APPENGINE_RUNTIME' in os.environ:  # pragma: no cover
        return None

    # Check if we have sufficient permissions to install in a
    # variety of system-wide locations.
    for abydos_data in data_path:
        if os.path.exists(abydos_data) and os.access(
            abydos_data, os.W_OK
        ):  # pragma: no cover
            return abydos_data

    # On Windows, use %APPDATA%
    if sys.platform == 'win32' and 'APPDATA' in os.environ:  # pragma: no cover
        homedir = os.environ['APPDATA']

    # Otherwise, install in the user's home directory.
    else:  # pragma: no cover
        homedir = os.path.expanduser('~/')
        if homedir == '~/':
            raise ValueError('Could not find a default download directory')

    # append "abydos_data" to the home directory
    return os.path.join(homedir, 'abydos_data')  # pragma: no cover


def download_package(
    resource_name, url=None, data_path=None, force=False, silent=False
):
    """Download and install a package or collection."""
    packages, collections = list_available_packages(url)
    installed = list_installed_packages(data_path)
    if data_path is None:
        data_path = _default_download_dir()
    os.makedirs(data_path, mode=0o775, exist_ok=True)

    for coll in collections:
        if resource_name == coll[0]:
            if not silent:  # pragma: no branch
                print('Installing {} collection'.format(coll[1]))  # noqa: T001
            for resource_name in coll[2]:
                download_package(resource_name, url, data_path)
            return
    else:
        for pack in packages:
            if resource_name == pack[0]:
                if not force:
                    for inst in installed:  # pragma: no branch
                        if pack[0] == inst[0] and pack[2] <= inst[2]:
                            if not silent:
                                print(  # pragma: no cover  # noqa: T001
                                    '{} package already up-to-date'.format(
                                        pack[1]
                                    )
                                )
                            return
                if not silent:  # pragma: no branch
                    print(  # noqa: T001
                        'Installing {} package'.format(pack[1])
                    )
                zip_fn = os.path.join(data_path, pack[4], pack[0] + '.zip')
                os.makedirs(
                    os.path.join(data_path, pack[4]), mode=0o775, exist_ok=True
                )
                urllib.urlretrieve(  # noqa: S310
                    pack[3][:-3] + 'xml', zip_fn[:-3] + 'xml'
                )
                urllib.urlretrieve(pack[3], zip_fn)  # noqa: S310
                zip_pkg = zipfile.ZipFile(zip_fn)
                zip_pkg.extractall(os.path.join(data_path, pack[4]))
                zip_pkg.close()
                os.remove(zip_fn)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
