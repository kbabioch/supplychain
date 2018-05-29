import sch.https

availableUrlHttp = 'http://babioch.de'
availableUrlHttps = 'https://babioch.de'

unavailableUrl = 'http://nonexisting.babioch.de'

def test_isAvailable():
  # Implicit check of network connectivity
  assert sch.https.checker.isAvailable(availableUrlHttp)

def test_isUnavailable():
  assert not sch.https.checker.isAvailable(unavailableUrl)

def test_checker():
  checker = sch.https.Checker(availableUrlHttp)
  assert checker.isAvailableHttp()
  assert checker.isAvailableHttps()
  assert checker.getHttp() == availableUrlHttp
  assert checker.getHttps() == availableUrlHttps

def test_replaceHttp():
  assert sch.https.replaceHttp(availableUrlHttp) == availableUrlHttps

def test_replaceHttpNotAvailable():
  assert sch.https.replaceHttp(unavailableUrl) == unavailableUrl

def test_replaceHttpInText():
  s = 'This is a text containing multiple HTTP URLs: ' + availableUrlHttp + ' , ' + availableUrlHttp + ' . It also contains a HTTPS URL: ' + availableUrlHttps
  assert sch.https.replaceHttp(s) == s.replace('http://', 'https://')

