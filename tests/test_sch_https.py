import scs.https

availableUrlHttp = 'http://babioch.de'
availableUrlHttps = 'https://babioch.de'

unavailableUrl = 'http://nonexisting.babioch.de'

class TestHttpChecker:

  def test_isAvailable(self):
    # Implicit check of network connectivity
    assert scs.https.checker.isAvailable(availableUrlHttp)
 
  def test_isUnavailable(self):
    assert not scs.https.checker.isAvailable(unavailableUrl)

  def test_checker(self):
    checker = scs.https.Checker(availableUrlHttp)
    assert checker.isAvailableHttp()
    assert checker.isAvailableHttps()
    assert checker.getHttp() == availableUrlHttp
    assert checker.getHttps() == availableUrlHttps

class TestHttpReplacer:

  def test_replaceHttp(self):
    assert scs.https.replaceHttp(availableUrlHttp) == availableUrlHttps

  def test_replaceHttpNotAvailable(self):
    assert scs.https.replaceHttp(unavailableUrl) == unavailableUrl

  def test_replaceHttpInText(self):
    s = 'This is a text containing multiple HTTP URLs: ' + availableUrlHttp + ' , ' + availableUrlHttp + ' . It also contains a HTTPS URL: ' + availableUrlHttps
    assert scs.https.replaceHttp(s) == s.replace('http://', 'https://')

