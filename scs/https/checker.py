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

# TODO Implement checkContent
# TODO Ignore body? HEAD cannot be used, since it yields different results? http://heise.de -> 30

import requests

def isAvailable(url):
  try:
    request = requests.get(url)
    if request.status_code == requests.status_codes.codes.OK:
      return True
  except requests.exceptions.RequestException:
    pass
  return False

class Checker:

  def __init__(self, url, checkContent = False):
    self.url = url
    self.checkContent = checkContent

  def isAvailableHttp(self):
    return isAvailable(self.url)

  def isAvailableHttps(self):
    return isAvailable(self.url.replace('http://', 'https://', 1))

  def getHttp(self):
    return self.url

  def getHttps(self):
    return self.url.replace('http://', 'https://', 1)

