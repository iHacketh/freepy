Name:		python-llist
Version:	0.4
Release:	1%{?dist}
Summary:	Linked list data structures for Python

License:	MIT
URL:		https://github.com/ajakubek/python-llist
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: python-pip
Requires: python >= 2.6

%description
llist is an extension module for CPython providing basic linked list data structures. Collections implemented in the llist module perform well in problems which rely on fast insertions and/or deletions of elements in the middle of a sequence. For this kind of workload, they can be significantly faster than collections.deque or standard Python lists.

%install
rm -rf %{buildroot}
pip install llist --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/usr
