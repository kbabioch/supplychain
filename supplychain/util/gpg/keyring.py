import subprocess
import sys
import re

class Keyring:

    # TODO Construct homedir on the fly, context manager
    # TODO Create homedir if not specified
    # TODO Use --no-keyring?
    # Initialize homedir for GPG
    def __init__(self, homedir):
        self.__homedir = homedir
        self.__keyids = []

    # Run GPG
    def __run_gpg(self, cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
        # TODO Check whether can be found?
        # TODO Make this configurable?
        gpg = '/usr/bin/gpg'
        cmdline = [gpg, '--homedir', self.__homedir] + cmdline
        return subprocess.run(cmdline, stdout=stdout, stderr=stderr, check=True)

    # Extracts keyids from provided signature file and remembers them
    def add_signature_file(self, signature_file):
        output = self.__run_gpg(['--list-packets', signature_file]).stdout.decode(sys.stdout.encoding)
        regexp = re.compile(r'^:signature packet: algo [0-9]+, keyid (?P<keyid>[0-9A-F]+)$', re.MULTILINE)
        self.__keyids += re.findall(regexp, output)

    # Receive keys for all collected keyids from keyserver
    def receive_keys(self):
        for keyid in self.__keyids:
            self.receive_key(keyid)

    # Receive key for given keyid
    def receive_key(self, keyid):
        self.__run_gpg(['--recv-key', keyid])

    # Minimize all keys for keyids collected beforehand
    def minimize(self):
        for keyid in self.__keyids:
            self.__run_gpg(['--no-tty', '--edit-key', keyid, 'minimize', 'save', 'quit'])

    # Export all keys to file (ASCII armor)
    def export(self, filename):
        with open(filename, 'w') as f:
            self.__run_gpg(['--export', '--armor'], stdout=f)

    # String representation
    def __str__(self):
        return 'homedir: {}, keyids: {}'.format(self.__homedir, self.__verbosity, self.__keyids)

