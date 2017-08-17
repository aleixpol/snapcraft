# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2017 Canonical Ltd
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

import sys
import traceback

from . import echo
import snapcraft.internal.errors


def exception_handler(exception_type, exception, exception_traceback, *,
                      debug=False):
    """Catch all Snapcraft exceptions unless debugging.

    This function is the global excepthook, properly handling uncaught
    exceptions. "Proper" being defined as:

    When debug=False:
        - If exception is a SnapcraftError, just display a nice error and exit
          according to the exit_code in the exception.
        - If exception is NOT a SnapcraftError, raise so traceback is shown.

    When debug=True:
        - If exception is a SnapcraftError, show traceback and exit according
          to the exit_code in the exception.
        - If exception is NOT a SnapcraftError, raise so traceback is shown.
    """

    if issubclass(exception_type, snapcraft.internal.errors.SnapcraftError):
        if not debug:
            echo.error(str(exception))
        else:
            traceback.print_exception(
                exception_type, exception, exception_traceback)
        sys.exit(exception.get_exit_code())
    else:
        raise exception
