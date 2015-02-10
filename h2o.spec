Summary:	H2O - an optimized HTTP server with support for HTTP/1.x and HTTP/2
Name:		h2o
Version:	0.9.1
Release:	0.1
License:	MIT
Group:		Networking/Daemons/HTTP
Source0:	https://github.com/h2o/h2o/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	6e60db62200b95e0fee372887bf8a4e3
URL:		https://github.com/h2o/h2o
BuildRequires:	cmake
BuildRequires:	yaml-devel
# 1.0.2+ recommended
BuildRequires:	openssl-devel
# conflicting headers
BuildConflicts:	libuv-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
H2O is a very fast HTTP server written in C. It can also be used as a
library.

%prep
%setup -q

%build
%cmake .
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md Changes LICENSE
%attr(755,root,root) %{_bindir}/h2o
%dir %{_datadir}/%{name}
%attr(755,root,root) %{_datadir}/%{name}/fetch-ocsp-response
