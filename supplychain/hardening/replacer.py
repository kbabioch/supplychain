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

# TODO Add list of URLs that should not be replaced

import supplychain.check.url
import re

# Replaces http:// by https:// when available
def callbackHttpUrl(match):
  url = match.group(0)
  checker = supplychain.check.url.URL(url)
  availableHttp = checker.isAvailableHttp()
  availableHttps = checker.isAvailableHttps()
  if availableHttp and availableHttps:
    return checker.getHttps()
  return checker.getHttp()

def replaceHttp(input):
  return re.sub('http://[^\s]+', callbackHttpUrl, input)

