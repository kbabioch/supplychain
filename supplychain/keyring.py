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

import subprocess
import sys
import re

class Keyring:

    # TODO Make use of this error class
    class GpgError(Exception):
        pass

    # https://git.gnupg.org/cgi-bin/gitweb.cgi?p=gnupg.git;a=blob_plain;f=doc/DETAILS
    RE_PUB = re.compile(r'^pub:(?P<validity>.):(?P<key_length>\d+)+:(?P<key_algo>\d+):(?P<key_id>[A-Z0-9]+):')
    RE_SIG = re.compile(r'^:signature packet: algo [0-9]+, keyid (?P<key_id>[0-9A-F]+)$')

    # TODO Construct homedir on the fly, context manager
    # TODO Create homedir if not specified
    # TODO Use --no-keyring?
    # Initialize homedir for GPG
    def __init__(self, homedir):
        self.homedir = homedir

    # Run GPG
    def gpg(self, cmdline, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
        # TODO Check whether can be found?
        # TODO Make this configurable?
        gpg = '/usr/bin/gpg'
        cmdline = [gpg, '--homedir', self.homedir, '--quiet', '--batch', '--yes', '--no-tty', '--no-greeting', '--with-colons', '--status-fd', '1', '--keyid-format', 'long'] + cmdline
        return subprocess.Popen(cmdline, stdin=stdin, stdout=stdout, stderr=stderr, encoding=sys.getdefaultencoding())

    # Extracts keyids from provided signature file and adds them to keyring
    def add_key_from_signature_file(self, signature_file):
        gpg = self.gpg(['--list-packets', signature_file])
        for line in gpg.stdout:
            m = re.match(self.RE_SIG, line)
            if m:
                self.receive_key(m.group('key_id'))

    # Receive key for given keyid
    def receive_key(self, keyid):
        self.gpg(['--recv-key', keyid])

    # Minimize all keys in keyring
    def minimize(self):
        for key in self.list_keys():
            gpg = self.gpg(['--edit-key', key, 'minimize', 'save', 'quit'])

    # Import keys from file
    def import_keyring(self, filename):
        self.gpg(['--import', filename])

    # Export all keys to file (ASCII armor)
    def export(self, filename):
        with open(filename, 'w') as f:
            self.gpg(['--status-fd', '2', '--export', '--armor'], stdout=f)

    # Load keyring from file
    def load(self, filename):
        self.gpg(['--import', filename])

    # List keys from keyring
    def list_keys(self):
        keys = []
        gpg = self.gpg(['--list-keys'])
        for line in gpg.stdout:
            m = re.match(self.RE_PUB, line)
            if m:
                keys.append(m.group('key_id'))
        return keys

