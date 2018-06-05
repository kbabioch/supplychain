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

import tempfile
import shutil
import os

class Error(Exception):
    pass

# TODO Get rid of rpmspec requirement, parse them manually
# TODO Consolidate regular expressions (different versions used throughout the file)

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

# TODO Probably this should be implemented as context manager
# TODO Do changes only in memory and implement a save()/write() method
# TODO Don't open files in each function, pass handler, etc.
# TODO Think about race conditions, etc. (file locking?)
# TODO Use functionality provided by Parser?
class Editor:

	def __init__(self, rpmfile):
		self.rpmfile = rpmfile
		self.last_source_line = 0
		self.max_source_index = None
		self.analyze()
		# TODO Raise exception when no sources found? Which line to add sources? -> Invalid spec file?

	# Looks for Source tags in specified rpmfile
	def analyze(self):
		with open(self.rpmfile) as f:

			# Counting the current line that is being processed right now
			current_line = 0

			# Iterate over file on a line by line basis
			for line in f:

				current_line += 1

				# Check line for source tag (with or without index)
				m = re.match('^Source(\d*):', line)

				if m:
					self.last_source_line = current_line
					index = m.group(1)

					# Skip on lines containing no index, i.e. `^Source:`
					if index == '':
						continue

					# Check whether current index is the maximum one
					index = int(index)
					if (not self.max_source_index or index > self.max_source_index):
						self.max_source_index = index

	# Return the next free source index (max + 1)
	# Might lead to fragmentation
	def get_next_source_index(self):
		if not self.max_source_index:
			return 1
		return self.max_source_index + 1

	# Add new source right after the last one
	def add_source(self, source):
		with tempfile.NamedTemporaryFile('w', delete=False) as outfile:
			with open(self.rpmfile) as infile:
				current_line = 0
				for line in infile:
					current_line += 1
					outfile.write(line)
					if current_line == self.last_source_line:
						self.last_source_line += 1
						current_line += 1
						source_index = self.get_next_source_index()
						outfile.write('Source{}: {}'.format(self.max_source_index, source) + os.linesep)
		shutil.move(outfile.name, self.rpmfile) # TODO Using os.replace() would be better (race condition, etc.)

