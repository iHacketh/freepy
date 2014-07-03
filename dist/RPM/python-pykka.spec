Name:		python-pykka
Version:	1.2.0
Release:	1%{?dist}
Summary:	Pykka is a Python implementation of the actor model

License:	MIT
URL:		http://www.pykka.org
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: python-pip
Requires: python >= 2.6

%description
Pykka is a Python implementation of the actor model. The actor model introduces some simple rules to control the sharing of state and cooperation between execution units, which makes it easier to build concurrent applications.

%install
rm -rf %{buildroot}
pip install pykka --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/usr
