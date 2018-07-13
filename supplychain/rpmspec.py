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

import re

import tempfile
import shutil
import os

class Parser:

	def __init__(self, rpmfile):
		self.rpmfile = rpmfile
		self.sources = []
		self.name = None
		self.version = None
		self.parse()

	def parse(self):
		with open(self.rpmfile) as f:
			current_line = 0
			for line in f:

				current_line += 1

				# Check for Source tag
				m = re.match(r'^Source(?P<index>[0-9]*):\s*(?P<source>\S+)', line)
				if m:
					index = m.group('index')
					source = m.group('source')
					if index:
						index = int(index)
					else:
						index = None
					self.sources.append({ 'index': index, 'source': source, 'line': current_line })

				# Check for name
				m = re.match(r'^Name:\s*(?P<name>\S+)', line)
				if m:
					self.name = m.group('name')

				# Check for version
				m = re.match(r'^Version:\s*(?P<version>\S+)', line)
				if m:
					self.version = m.group('version')

	# TODO Do this in a more generic way
	def expand(self, string):
		string = re.sub(r'%{name}', self.name, string)
		string = re.sub(r'%{version}', self.version, string)
		return string

# TODO Probably this should be implemented as context manager
# TODO Do changes only in memory and implement a save()/write() method
# TODO Don't open files in each function, pass handler, etc.
# TODO Think about race conditions, etc. (file locking?)
class Editor:

	def __init__(self, rpmfile):
		self.rpmfile = rpmfile
		self.last_source_line = 0
		self.max_source_index = None
		self.sources = []
		self.analyze_sources()
		# TODO Raise exception when no sources found? Which line to add sources? -> Invalid spec file?

	# Analyzes the sources
	def analyze_sources(self):
		self.sources = Parser(self.rpmfile).sources
		for source in self.sources:
			if not self.max_source_index or source['index'] > self.max_source_index:
				self.max_source_index = source['index']
			if source['line'] > self.last_source_line:
				self.last_source_line = source['line']

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

