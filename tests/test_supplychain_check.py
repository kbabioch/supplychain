import supplychain.check.url
import supplychain.hardening.replacer
import pytest

availableUrlHttp = 'http://babioch.de'
availableUrlHttps = 'https://babioch.de'

unavailableUrl = 'http://nonexisting.babioch.de'

class TestSupplychainCheck:

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

