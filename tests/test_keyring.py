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

KEYRING = 'tests/keyrings/keyring.asc'
SIGFILE = 'tests/signed/COPYING.sig'
KEYS = ['749A65CD479F3215']

class TestKeyring:

    def test_emptyKeyring(self):
        with Keyring() as keyring:
            assert len(keyring.list_keys()) == 0

    def test_importKeyring(self):
        with Keyring() as keyring:
            keyring.load(KEYRING)
            assert keyring.list_keys() == KEYS

    def test_importSignatureFromFile(self):
        # with Keyring() as keyring:
        #     keyring.add_key_from_signature_file(SIGFILE)
        #     assert keyring.list_keys() == KEYS
        pass
