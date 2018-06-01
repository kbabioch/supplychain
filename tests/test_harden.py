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

import supplychain.harden

availableUrlHttp = 'http://babioch.de'
availableUrlHttps = 'https://babioch.de'

unavailableUrl = 'http://nonexisting.babioch.de'

# TODO Setup object only once

class TestHttpReplacer:

  def test_replaceHttp(self):
    h = supplychain.harden.HttpReplacer()
    assert h.replace(availableUrlHttp) == availableUrlHttps

  def test_replaceHttpNotAvailable(self):
    h = supplychain.harden.HttpReplacer()
    assert h.replace(unavailableUrl) == unavailableUrl

  def test_replaceHttpInText(self):
    h = supplychain.harden.HttpReplacer()
    s = 'This is a text containing multiple HTTP URLs: ' + availableUrlHttp + ' , ' + availableUrlHttp + ' . It also contains a HTTPS URL: ' + availableUrlHttps
    assert h.replace(s) == s.replace('http://', 'https://')
