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
				index = m.group('index')
				source = m.group('source')
				if index:
					index = int(index)
				else:
					index = None
				sources.append(Source(index, source))

		return sources

class Source:

	def __init__(self, index, source):
		self.index = index
		self.source = source

	def __str__(self):
		print('Source{}: {}'.format(self.index, self.source))

	def __eq__(self, other):
		return self.index == other.index and self.source == other.source

# TODO Don't open file in each function, pass handler, etc.
# TODO Probably this should be implemented as context manager
class Editor:

	def __init__(self, rpmfile):
		self.rpmfile = rpmfile

	def get_last_source_line(self):
		with open(self.rpmfile) as f:
			current_line = 0
			last_source_line = 0
			for line in f:
				current_line += 1
				if re.match('^Source\d+:', line):
					last_source_line = current_line
			return last_source_line
		# TODO What to return in the case file could not be opened?

	def add_source(self, source):
		with open(self.rpmfile) as f:
			content = f.readlines()
			content.insert(self.get_last_source_line(), source)
			f.writelines(content)

