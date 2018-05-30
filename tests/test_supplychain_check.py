import supplychain.check.url
import supplychain.hardening.replacer
import pytest

# TODO: Start webserver within Python instead of relying outside connectivity

availableUrlHttp = 'http://babioch.de'
availableUrlHttps = 'https://babioch.de'
unavailableUrl = 'http://nonexisting.babioch.de'
fileUrl = 'https://www.gnupg.org/ftp/gcrypt/gnupg/gnupg-2.2.7.tar.bz2'
fileUrlSignature = 'https://www.gnupg.org/ftp/gcrypt/gnupg/gnupg-2.2.7.tar.bz2.asc'

class TestSupplychainCheckURL:

  def test_isAvailable(self):
    # Implicit check of network connectivity
    assert supplychain.check.url.isAvailable(availableUrlHttp)
 
  def test_isUnavailable(self):
    assert not supplychain.check.url.isAvailable(unavailableUrl)

  def test_urlChecker(self):
    checker = supplychain.check.url.URL(availableUrlHttp)
    assert True == checker.isAvailableHttp()
    assert True == checker.isAvailableHttps()
    assert checker.getHttp() == availableUrlHttp
    assert checker.getHttps() == availableUrlHttps

  def test_isHttp(self):
    checker = supplychain.check.url.URL(availableUrlHttp)
    assert True == checker.isHttp()
    assert False == checker.isHttps()

  def test_isHttps(self):
    checker = supplychain.check.url.URL(availableUrlHttps)
    assert False == checker.isHttp()
    assert True == checker.isHttps()

  def test_invalidURL(self):
    with pytest.raises(ValueError):
      supplychain.check.url.URL('http://[')

  def test_invalidURLScheme(self):
    with pytest.raises(ValueError):
      supplychain.check.url.URL('ftp://')

class TestSupplychainCheckSignature:

  def test_isAvailableSig(self):
    checker = supplychain.check.signature.Signature(fileUrl)
    assert True == checker.isAvailableSig()

  def test_isNotAvailableSignature(self):
    checker = supplychain.check.signature.Signature(unavailableUrl)
    assert False == checker.isAvailableSig()

  def test_getSignedUrl(self):
    checker = supplychain.check.signature.Signature(fileUrl)
    assert True == checker.isAvailableSig()
    assert checker.getSignedUrl() == fileUrlSignature

