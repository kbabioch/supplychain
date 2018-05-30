import supplychain.rpm.spec
import pytest

class TestSupplychainRPM:

  def test_invalidSpecFile(self):
    with pytest.raises(supplychain.rpm.exceptions.Error):
      supplychain.rpm.spec.parser('/dev/null')

  def test_getSources(self):
    p = supplychain.rpm.spec.parser('tests/specfiles/llvm.spec')
    assert p.get_sources() == [('0', 'README.packaging'), ('101', 'baselibs.conf')]

