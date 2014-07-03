Name:		python-freepy
Version:	0.9.8
Release:	1%{?dist}
Summary:	A thin framework for building communications apps on top of FreeSWITCH.	
Source0:	%{name}-%{version}.tar.gz

License:	Apache 2.0
URL:		https://github.com/thomasquintana/freepy
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: python-pip, python-devel >= 2.6,python-pykka == 1.2.0,python-llist == 0.4,python-twisted == 13.2.0
Requires: python >= 2.6,python-pykka == 1.2.0,python-llist == 0.4,python-twisted == 13.2.0

%description
A Python Actor based application server powered by FreeSWITCH. Freepy enables Python developers to rapidly build complex communications solutions by providing a simple programming model along with primitives to communicate with FreeSWITCH asynchronously over the event socket.

%install
rm -rf %{buildroot}
pip install %{_sourcedir}/%{name}-%{version}.tar.gz --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/usr
