# Copyright (c) 2018 Karol Babioch <kbabioch@suse.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess
import sys
import re

from supplychain.rpm.exceptions import Error

# TODO Get rid of rpmspec requirement, parse them manually

class parser:

    def __init__(self, rpmfile):

        # TODO Make this configurable
        # Used to expand macros, etc.
        rpmspec = '/usr/bin/rpmspec'

        try:
            self.__output = subprocess.check_output([rpmspec, '-P', rpmfile]).decode(sys.stdout.encoding)

        except FileNotFoundError:
            raise Error('rpmspec binary not found')

        except subprocess.CalledProcessError:
            raise Error('invalid spec file')

    # TODO Define datatype (named tuple?) which will be returned here
    def get_sources(self):

        regexp = re.compile('^Source(?P<index>[0-9]*):\s*(?P<source>\S+)', re.MULTILINE)
        sources = re.findall(regexp, self.__output)

        return sources
