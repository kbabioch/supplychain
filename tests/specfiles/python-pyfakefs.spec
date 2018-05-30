#
# spec file for package python-pyfakefs
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%{?!python_module:%define python_module() python-%{**} python3-%{**}}
Name:           python-pyfakefs
Version:        3.4.1
Release:        0
Summary:        Fake file system that mocks the Python file system modules
License:        Apache-2.0
Group:          Development/Languages/Python
URL:            http://pyfakefs.org
Source:         https://github.com/jmcgeheeiv/pyfakefs/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  %{python_module pytest}
BuildRequires:  %{python_module setuptools}
BuildRequires:  fdupes
BuildRequires:  python-rpm-macros
BuildArch:      noarch
%python_subpackages

%description
pyfakefs implements a fake file system that mocks the Python file system
modules. Using pyfakefs, your tests operate on a fake file system in
memory without touching the real disk. The software under test requires
no modification to work with pyfakefs.

%prep
%setup -q -n pyfakefs-%{version}

%build
%python_build

%install
%python_install
%python_expand %fdupes %{buildroot}%{$python_sitelib}

%check
export LANG=C.UTF-8
%python_exec setup.py test

%files %{python_files}
%doc CHANGES* README*
%license COPYING*
%{python_sitelib}/*

%changelog
