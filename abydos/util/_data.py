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
import shutil
import sys
import urllib.request
import zipfile

from typing import List, Match, Optional, Tuple, cast
from xml.etree import ElementTree  # noqa: S405

__all__ = [
    'data_path',
    'download_package',
    'list_available_packages',
    'list_installed_packages',
    'package_path',
]


DATA_SUBDIRS = ['corpora', 'keymaps']
INDEX_URL = (
    'https://raw.githubusercontent.com/chrislit/abydos-data/master/index.xml'
)

data_path = []  # type: List[str]
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


def package_path(resource_name: str) -> str:
    """Given a resource name, returns the path to the package.

    Parameters
    ----------
    resource_name : str
        The resource name being queried

    Returns
    -------
    The local path to the resource

    Raises
    ------
    FileNotFoundError
        The specified resource could not be found


    .. versionadded:: 0.5.0

    """
    for path in data_path:
        for subdir in DATA_SUBDIRS:
            check_path = os.path.join(path, subdir, resource_name)
            if os.path.isdir(check_path):
                return check_path
    msg = 'Data package not found. You may need to install or re-install it.'
    raise FileNotFoundError(msg)


def list_installed_packages(
    path: Optional[str] = None,
) -> List[Tuple[str, str, float]]:
    """List all installed data packages.

    Parameters
    ----------
    path : str or None
        The path to your installed packages. If None is used, the default
        installation locations will be checked.

    Returns
    -------
    list of tuples of (str, str, float)
        Each tuple of the list represents the package name, description, and
        version number.


    .. versionadded:: 0.5.0

    """
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
                            os.path.join(check_path, f"{package}.xml")
                        ) as xml:
                            file = xml.read()
                            name = cast(
                                Match[str], re.search(r'name="([^"]+)"', file)
                            ).group(1)
                            version = cast(
                                Match[str],
                                re.search(r'version="([^"]+)"', file),
                            ).group(1)
                        packages.append((package, name, float(version)))
    return packages


def list_available_packages(
    url: Optional[str] = None,
) -> Tuple[
    List[Tuple[str, str, float, str, str, str]],
    List[Tuple[str, str, List[str]]],
]:
    """List all data packages available for install.

    Parameters
    ----------
    url : str or None
        The URL of the package repository. If None is supplied, the default
        package repository is used.

    Returns
    -------
    tuple of lists of tuples
        The first tuple lists each individual package available in the
        repository, while the second lists collections available in the
        repository.


    .. versionadded:: 0.5.0

    """
    installed_packages = {_[0]: _[2] for _ in list_installed_packages()}

    if url is None:
        url = INDEX_URL
    if url[:8] != 'https://':
        raise ValueError('url should begin with "https://"')
    with urllib.request.urlopen(url) as ix:  # noqa: S310
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


def _default_download_dir() -> Optional[str]:
    """Return the directory to which packages will be downloaded by default.

    This is mostly copied from NLTK's
    nltk.downloader.Downloader.default_download_dir

    Returns
    -------
    str or None
        The default download directory for the current platform


    .. versionadded:: 0.5.0

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
    resource_name: str,
    url: Optional[str] = None,
    data_path: Optional[str] = None,
    force: bool = False,
    silent: bool = False,
) -> None:
    """Download and install a package or collection.

    Parameters
    ----------
    resource_name : str
        The resource (package or collection) name to download
    url : str or None
        The repository URL to use (or None for default)
    data_path : str or None
        The data path to install to (or None for platform default)
    force : bool
        Set to True to force overwriting data
    silent : bool
        Set to True to perform silent installation (without any prints)


    .. versionadded:: 0.5.0

    """
    packages, collections = list_available_packages(url)
    installed = list_installed_packages(data_path)
    if data_path is None:
        data_path = _default_download_dir()
    os.makedirs(cast(str, data_path), mode=0o775, exist_ok=True)

    for coll in collections:
        if resource_name == coll[0]:
            if not silent:  # pragma: no branch
                print(f'Installing {coll[1]} collection')  # noqa: T001
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
                                    f'{pack[1]} package already up-to-date'
                                )
                            return
                if not silent:  # pragma: no branch
                    print(f'Installing {pack[1]} package')  # noqa: T001
                zip_fn = os.path.join(
                    cast(str, data_path), pack[4], f"{pack[0]}.zip"
                )
                shutil.rmtree(
                    os.path.join(cast(str, data_path), pack[4], pack[0]),
                    ignore_errors=True,
                )
                os.makedirs(
                    os.path.join(cast(str, data_path), pack[4]),
                    mode=0o775,
                    exist_ok=True,
                )
                urllib.request.urlretrieve(  # noqa: S310
                    f"{pack[3][:-3]}xml", f"{zip_fn[:-3]}xml"
                )
                urllib.request.urlretrieve(pack[3], zip_fn)  # noqa: S310
                zip_pkg = zipfile.ZipFile(zip_fn)
                zip_pkg.extractall(os.path.join(cast(str, data_path), pack[4]))
                zip_pkg.close()
                os.remove(zip_fn)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
