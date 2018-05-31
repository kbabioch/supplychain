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

# TODO Re-factor into sc.checker.sig (along with sc.checker.http)
# TODO Re-use sc.https?
# TODO Check whether URL is a signature itself, so looking for sig makes no sense

import requests
import supplychain.check.url

class Signature:

  def __init__(self, url):
    self.url = url
    self.signatureFileURL = ''

  def isSignatureFileAvailable(self):
    exts = ['asc', 'sig']
    for ext in exts:
      signatureFileURL = self.url + '.' + ext
      if supplychain.check.url.isAvailable(signatureFileURL):
        self.signatureFileURL = signatureFileURL
        return True
    return False

  def getSignatureFileURL(self):
    return self.signatureFileURL

