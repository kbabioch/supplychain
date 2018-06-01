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
# TODO Ignore body? HEAD cannot be used, since it yields different results? http://heise.de -> 301
# TODO Take 301 redirection,etc. into consideration

import requests
from urllib.parse import urlparse, urlunparse

class URLCheck:

  @staticmethod
  def isAvailable(url):
    try:
      request = requests.get(url)
      if request.status_code == requests.status_codes.codes.OK:
        return True
    except requests.exceptions.RequestException:
      pass
    return False

  def __init__(self, url, checkContent = False):
    try:
      self.url = urlparse(url)
    except ValueError:
      raise ValueError('Invalid URL')
    if self.url.scheme not in ['http', 'https']:
      raise ValueError('Invalid URL scheme')
    self.checkContent = checkContent

  def isHttp(self):
    return self.url.scheme == 'http'

  def isHttps(self):
    return self.url.scheme == 'https'

  def isAvailableHttp(self):
    return URLCheck.isAvailable(self.getHttp())

  def isAvailableHttps(self):
    return URLCheck.isAvailable(self.getHttps())

  def getHttp(self):
    u = list(self.url)
    u[0] = 'http'
    return urlunparse(u)

  def getHttps(self):
    u = list(self.url)
    u[0] = 'https'
    return urlunparse(u)

class SignatureCheck:

  EXTENSIONS = ['asc', 'sig']

  def __init__(self, url):
    self.url = url
    self.signatureFileURL = False

  def isSignatureFileAvailable(self):
    for ext in self.EXTENSIONS:
      signatureFileURL = '{}.{}'.format(self.url, ext)
      if URLCheck.isAvailable(signatureFileURL):
        self.signatureFileURL = signatureFileURL
        return True
    return False

  def getSignatureFileURL(self):
    return self.signatureFileURL

