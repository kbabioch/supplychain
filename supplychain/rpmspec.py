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

class Error(Exception):
    pass

# TODO Get rid of rpmspec requirement, parse them manually

class Parser:

	def __init__(self, rpmfile):

		# TODO Make this configurable
		# Used to expand macros, etc.
		rpmspec = '/usr/bin/rpmspec'

		try:
			# TODO Exception handling in decode
			self.__output = subprocess.check_output([rpmspec, '-P', rpmfile]).decode(sys.stdout.encoding)
		
		except FileNotFoundError:
			raise Error('rpmspec binary not found')

		except subprocess.CalledProcessError:
			raise Error('invalid spec file')

	def get_sources(self):

		sources = []
		regexp = re.compile('^Source(?P<index>[0-9]*):\s*(?P<source>\S+)', re.MULTILINE)

		for line in self.__output.splitlines():
			m = re.match(regexp, line)
			if m:
				sources.append(Source(m.group(1), m.group(2)))
		return sources

class Source:

	def __init__(self, index, source):
		self.index = index
		self.source = source

	def __str__(self):
		print('Source{}: {}'.format(self.index, self.source))

	def __eq__(self, other):
		return self.index == other.index and self.source == other.source

class Editor:

	def __init__(self, rpmfile):
		self.rpmfile = rpmfile

	def add_source(self, source):
		pass # TODO Implement
