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

# TODO Implement

from supplychain.keyring import Keyring

import shutil
import subprocess
import tempfile
import pytest

class TestKeyring:

	@pytest.fixture()
	def init_keyring_homedir(self):
		homedir = tempfile.mkdtemp()
		keyring = Keyring(homedir)
		yield keyring
		try:
			shutil.rmtree(homedir)
		except OSError as e:
			if e.errno != errno.ENOENT:
				raise

	def test_add_signature_file(self, init_keyring_homedir):
		keyring = init_keyring_homedir
		# Add file with valid OpenPGP signature
		keyring.add_signature_file('tests/signed/COPYING.sig')
		# Add file without signature
		with pytest.raises(subprocess.CalledProcessError):
			keyring.add_signature_file('COPYING')
