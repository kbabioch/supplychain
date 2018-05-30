import supplychain.check.url
import supplychain.hardening.replacer

availableUrlHttp = 'http://babioch.de'
availableUrlHttps = 'https://babioch.de'

unavailableUrl = 'http://nonexisting.babioch.de'

class TestSupplychainCheck:

  def test_isAvailable(self):
    # Implicit check of network connectivity
    assert supplychain.check.url.isAvailable(availableUrlHttp)
 
  def test_isUnavailable(self):
    assert not supplychain.check.url.isAvailable(unavailableUrl)

  def test_checker(self):
    checker = supplychain.check.url.URL(availableUrlHttp)
    assert checker.isAvailableHttp()
    assert checker.isAvailableHttps()
    assert checker.getHttp() == availableUrlHttp
    assert checker.getHttps() == availableUrlHttps

