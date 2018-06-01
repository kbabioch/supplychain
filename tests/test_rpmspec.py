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
import supplychain.rpmspec
import pytest

class TestParser:

  def test_invalidSpecFile(self):
    with pytest.raises(supplychain.rpmspec.Error):
      supplychain.rpmspec.Parser('/dev/null')

  def test_getSources(self):
    p = supplychain.rpmspec.Parser('tests/specfiles/llvm.spec')
    assert p.get_sources() == [('0', 'README.packaging'), ('101', 'baselibs.conf')]

  @mock.patch('subprocess.check_output')
  def test_FileNotFound(self, m):
    m.side_effect = supplychain.rpmspec.Error()
    with pytest.raises(supplychain.rpmspec.Error):
      subprocess.check_output()

class TestSource:
  pass

