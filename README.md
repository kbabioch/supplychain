# SUPPLY CHAIN HARDENING

[![Build status](https://travis-ci.org/kbabioch/supply-chain-security.svg?branch=master)](https://travis-ci.org/kbabioch/supply-chain-security)
[![Code coverage](https://codecov.io/gh/kbabioch/supply-chain-security/branch/master/graph/badge.svg)](https://codecov.io/gh/kbabioch/supply-chain-security)
[![Coverity scan](https://scan.coverity.com/projects/15865/badge.svg)](https://scan.coverity.com/projects/kbabioch-supply-chain-security)

This repository contains a set of tools and scripts to improve the supply chain
security around RPM files and the Open Build Service (OBS). This can be helpful
in identifying potential improvement when retrieving sources, e.g.:

- Scan for unused signature files, that are available upstream, but not used
  during the build process to verify the authenticity of the sources
- Use of unencrypted transfer channels, e.g. using `http://`,
  although `https://` is available

It also contains tools to quickly create keyrings, required for verification of
signed source files.

## TOOLS

### sch-keyring

This script will extract the OpenPGP key IDs that were used to sign the
provided files and will try to retrieve them using public keyservers.
It minimizes these keys and exports the whole keyring to a file. The
resulting keyring file can be used to verify all available sources, e.g.
within a RPM spec file.

### sch-https-replace

This script scans the input for any `http://` URLs, and checks whether the
appropriate `https://` URL is also available. It replaces these URLs, if
applicable. Optionally, it can also check whether the returned resource is
actually the same.

## LICENSE

[![GNU GPLv3](http://www.gnu.org/graphics/gplv3-127x51.png "GNU GPLv3")](http://www.gnu.org/licenses/gpl.html)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

