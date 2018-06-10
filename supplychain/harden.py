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

import supplychain.check
import re

class HttpReplacer:

  def __init__(self):
    self.ignoreUrls = []

  def addIgnoreUrl(self, url):
    self.ignoreUrls.append(url)

  def replace(self, input):
    return re.sub('http://[^\s]+', self.callbackHttpUrl, input)

  def callbackHttpUrl(self, match):
    url = match.group(0)
    if url not in self.ignoreUrls:
        checker = supplychain.check.UrlChecker(url)
        availableHttp = checker.isAvailableHttp()
        availableHttps = checker.isAvailableHttps()
        if availableHttp and availableHttps:
          return checker.getHttps()
    return url

