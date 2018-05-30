import rpm.spec
import pytest

class TestRPMSpecParser:

  def test_invalidSpecFile(self):
    with pytest.raises(rpm.exceptions.Error):
      rpm.spec.parser('/dev/null')

  def test_getSources(self):
    p = rpm.spec.parser('tests/llvm.spec')
    assert p.get_sources() == [('0', 'http://llvm.org/releases/3.8.0/llvm-3.8.0.src.tar.xz'), ('100', 'llvm-config.h')]

