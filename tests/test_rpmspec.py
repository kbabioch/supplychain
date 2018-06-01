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

import mock
import subprocess
from supplychain.rpmspec import Source, Parser, Error
import pytest

class TestParser:

  def test_invalidSpecFile(self):
    with pytest.raises(Error):
      Parser('/dev/null')

  def test_getSources(self):
    p = Parser('tests/specfiles/llvm.spec')
    sources = p.get_sources()
    assert sources[0].index == 0
    assert sources[0].source == 'README.packaging'
    assert sources[1].index == 101
    assert sources[1].source == 'baselibs.conf'

  @mock.patch('subprocess.check_output')
  def test_FileNotFound(self, m):
    m.side_effect = Error()
    with pytest.raises(Error):
      subprocess.check_output()

class TestSource:

	def test_createSourceWithIndex(self):
		s = Source(0, 'file')
		assert s.index == 0
		assert s.source == 'file'

	def test_createSourceWithoutIndex(self):
		s = Source(None, 'file')
		assert s.index == None
		assert s.source == 'file'

	def test_unequalityOfSources(self):
		s1 = Source(1, 'file1')
		s2 = Source(2, 'file2')
		assert s1 != s2

		s1 = Source(1, 'file1')
		s2 = Source(2, 'file1')
		assert s1 != s2

	def test_equalityOfSources(self):
		s1 = Source(1, 'file1')
		s2 = Source(1, 'file1')
		assert s1 == s2

class TestEditor:
	pass
