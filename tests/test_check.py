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

from supplychain.check import UrlChecker, SignatureFileChecker
import pytest

# TODO: Start webserver within Python instead of relying outside connectivity, since currently these tests require an active Internet connection

availableUrlHttp = 'http://babioch.de'
availableUrlHttps = 'https://babioch.de'
unavailableUrl = 'http://nonexisting.babioch.de'
fileUrl = 'https://www.gnupg.org/ftp/gcrypt/gnupg/gnupg-2.2.7.tar.bz2'
fileUrlSignature = 'https://www.gnupg.org/ftp/gcrypt/gnupg/gnupg-2.2.7.tar.bz2.sig'

class TestUrlChecker:

  def test_isAvailable(self):
    assert UrlChecker.isAvailable(availableUrlHttp)
 
  def test_isUnavailable(self):
    assert not UrlChecker.isAvailable(unavailableUrl)

  def test_HttpAndHttpsAvailable(self):
    checker = UrlChecker(availableUrlHttp)
    assert checker.isAvailableHttp()
    assert checker.isAvailableHttps()
    assert checker.getHttp() == availableUrlHttp
    assert checker.getHttps() == availableUrlHttps

  def test_isHttp(self):
    checker = UrlChecker(availableUrlHttp)
    assert checker.isHttp()
    assert not checker.isHttps()

  def test_isHttps(self):
    checker = UrlChecker(availableUrlHttps)
    assert not checker.isHttp()
    assert checker.isHttps()

  def test_invalidUrl(self):
    with pytest.raises(ValueError):
      UrlChecker('http://[')

  def test_invalidUrlScheme(self):
    with pytest.raises(ValueError):
      UrlChecker('ftp://')

  def test_emptyUrlScheme(self):
    with pytest.raises(ValueError):
      UrlChecker('file')

class TestSignatureFileChecker:

  def test_signatureFileAvailable(self):
    checker = SignatureFileChecker(fileUrl)
    assert checker.getSignatureFileUrls()

  def test_signatureFileNotAvailable(self):
    checker = SignatureFileChecker(unavailableUrl)
    assert not checker.getSignatureFileUrls()

  def test_getSignatureFileUrls(self):
    checker = SignatureFileChecker(fileUrl)
    assert fileUrlSignature in checker.getSignatureFileUrls()

