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

import logging
import shutil
import subprocess
import sys
import tempfile
import re

logger = logging.getLogger(__name__)

class Keyring:

    # TODO Make use of this error class
    class GpgError(Exception):
        pass

    # https://git.gnupg.org/cgi-bin/gitweb.cgi?p=gnupg.git;a=blob_plain;f=doc/DETAILS
    RE_PUB = re.compile(r'^pub:(?P<validity>.):(?P<key_length>\d+)+:(?P<key_algo>\d+):(?P<key_id>[A-Z0-9]+):')
    RE_SIG = re.compile(r'^:signature packet: algo [0-9]+, keyid (?P<key_id>[0-9A-F]+)$')

    # Run GPG
    def gpg(self, cmdline, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
        # TODO Check whether can be found?
        # TODO Make this configurable?
        gpg = '/usr/bin/gpg'
        cmdline = [gpg, '--homedir', self.homedir, '--quiet', '--batch', '--yes', '--no-tty', '--no-greeting', '--with-colons', '--status-fd', '1', '--keyid-format', 'long'] + cmdline
        logger.debug('Running gpg: %s', cmdline)
        return subprocess.Popen(cmdline, stdin=stdin, stdout=stdout, stderr=stderr, encoding=sys.getdefaultencoding())

    # Extracts keyids from provided signature file and adds them to keyring
    def add_key_from_signature_file(self, signature_file):
        logger.info('Adding keys from signed file: %s', signature_file)
        gpg = self.gpg(['--list-packets', signature_file])
        for line in gpg.stdout:
            m = re.match(self.RE_SIG, line)
            if m:
                logger.info('Found key in signed file: %s', m.group('key_id'))
                self.receive_key(m.group('key_id'))

    # Receive key for given keyid
    def receive_key(self, keyid):
        logger.info('Receiving key: %s', keyid)
        self.gpg(['--recv-keys', keyid]).wait()

    # Minimize all keys in keyring
    def minimize(self):
        logger.info('Minimizing keyring')
        for key in self.list_keys():
            logger.info('Minimizing key: %s', key)
            gpg = self.gpg(['--edit-key', key, 'minimize', 'save', 'quit']).wait()

    # Load keyring from file
    def load(self, filename):
        logger.info('Loading keyring from file: %s', filename)
        self.gpg(['--import', filename]).wait()

    # Export all keys to file (ASCII armor)
    def export(self, filename):
        logger.info('Exporting keyring to file: %s', filename)
        with open(filename, 'w') as f:
            self.gpg(['--status-fd', '2', '--export', '--armor'], stdout=f).wait()

    # List keys from keyring
    def list_keys(self):
        keys = []
        gpg = self.gpg(['--list-keys'])
        for line in gpg.stdout:
            m = re.match(self.RE_PUB, line)
            if m:
                keys.append(m.group('key_id'))
        logger.info('Listing keys from keyring: %s', keys)
        return keys

    def __enter__(self):
        homedir = tempfile.mkdtemp()
        logger.info('Creating temporary GnuPG home directory: %s', homedir)
        self.homedir = homedir
        return self

    def __exit__(self, type, value, traceback):
        logger.info('Removing GnuPG homedir: %s', self.homedir)
        shutil.rmtree(self.homedir)
