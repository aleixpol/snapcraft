# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2015-2017 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from snapcraft.internal.common import get_os_release_info
from ._platform import _is_deb_based
from snapcraft.internal import errors


class RepoError(errors.SnapcraftError):
    pass


class BuildPackageNotFoundError(RepoError):

    fmt = "Could not find a required package in 'build-packages': {package}"

    def __init__(self, package):
        super().__init__(package=package)


class PackageNotFoundError(RepoError):

    @property
    def message(self):
        message = 'The package {!r} was not found.'.format(
            self.package_name)
        # If the package was multiarch, try to help.
        distro = get_os_release_info()['ID']
        if _is_deb_based(distro) and ':' in self.package_name:
            (name, arch) = self.package_name.split(':', 2)
            if arch:
                message += (
                    '\nYou may need to add support for this architecture with '
                    "'dpkg --add-architecture {}'.".format(arch))
        return message

    def __init__(self, package_name):
        self.package_name = package_name

    def __str__(self):
        return self.message


class UnpackError(RepoError):

    fmt = 'Error while provisioning {package!r}'

    def __init__(self, package):
        super().__init__(package=package)


class SnapInstallError(RepoError):

    fmt = ('Error while installing snap {snap_name!r} from channel '
           '{snap_channel!r}')

    def __init__(self, *, snap_name, snap_channel):
        super().__init__(snap_name=snap_name, snap_channel=snap_channel)


class SnapRefreshError(RepoError):

    fmt = ('Error while refreshing snap {snap_name!r} to channel '
           '{snap_channel!r}')

    def __init__(self, *, snap_name, snap_channel):
        super().__init__(snap_name=snap_name, snap_channel=snap_channel)
