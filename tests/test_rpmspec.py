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

from supplychain.rpmspec import Parser, Editor

SPECFILE = 'tests/specfiles/dkgpg.spec'

class TestParser:

    def test_parse_rpmfile(self):
        parser = Parser(SPECFILE)
        assert parser.rpmfile == SPECFILE
        assert parser.name == 'dkgpg'
        assert parser.version == '1.0.6'
        assert parser.sources == [{'index': None, 'source': 'https://download.savannah.gnu.org/releases/dkgpg/%{name}-%{version}.tar.gz', 'line': 26}, {'index': 2, 'source': 'https://download.savannah.gnu.org/releases/dkgpg/%{name}-%{version}.tar.gz.sig', 'line': 27}, {'index': 3, 'source': '%{name}.keyring', 'line': 28}]

    def test_expand(self):
        parser = Parser(SPECFILE)
        assert parser.expand('%{name}') == 'dkgpg'
        assert parser.expand('%{version}') == '1.0.6'
        assert parser.expand('%{name}-%{version}') == 'dkgpg-1.0.6'

class TestEditor:
	pass
