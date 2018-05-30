import supplychain.check.url
import supplychain.hardening.replacer

availableUrlHttp = 'http://babioch.de'
availableUrlHttps = 'https://babioch.de'

unavailableUrl = 'http://nonexisting.babioch.de'

class TestSupplychainHardening:

  def test_replaceHttp(self):
    assert supplychain.hardening.replacer.replaceHttp(availableUrlHttp) == availableUrlHttps

  def test_replaceHttpNotAvailable(self):
    assert supplychain.hardening.replacer.replaceHttp(unavailableUrl) == unavailableUrl

  def test_replaceHttpInText(self):
    s = 'This is a text containing multiple HTTP URLs: ' + availableUrlHttp + ' , ' + availableUrlHttp + ' . It also contains a HTTPS URL: ' + availableUrlHttps
    assert supplychain.hardening.replacer.replaceHttp(s) == s.replace('http://', 'https://')

