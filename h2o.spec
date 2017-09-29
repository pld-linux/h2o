# TODO
# - libwslay for websockets
Summary:	H2O - an optimized HTTP server with support for HTTP/1.x and HTTP/2
Name:		h2o
Version:	2.2.2
Release:	0.1
License:	MIT
Group:		Networking/Daemons/HTTP
Source0:	https://github.com/h2o/h2o/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	efc3a98cd21d3b91d66b2a99b1518255
URL:		https://github.com/h2o/h2o
BuildRequires:	cmake >= 2.8.11
BuildRequires:	libstdc++-devel
BuildRequires:	libuv-devel >= 1.0.0
BuildRequires:	openssl-devel >= 1.0.2
BuildRequires:	pkgconfig
BuildRequires:	yaml-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
H2O is a very fast HTTP server written in C. It can also be used as a
library.

%package devel
Summary:	Header files for h2o library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki h2o
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for h2o library.

%prep
%setup -q

%build
install -d build
cd build
%cmake ..
%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install -C build \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md Changes LICENSE
%attr(755,root,root) %{_bindir}/h2o
%{_libdir}/libh2o.so.0.13
%attr(755,root,root) %{_libdir}/libh2o.so.*.*.*
%{_libdir}/libh2o-evloop.so.0.13
%attr(755,root,root) %{_libdir}/libh2o-evloop.so.*.*.*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/mruby
%{_datadir}/%{name}/status
%attr(755,root,root) %{_datadir}/%{name}/annotate-backtrace-symbols
%attr(755,root,root) %{_datadir}/%{name}/fastcgi-cgi
%attr(755,root,root) %{_datadir}/%{name}/fetch-ocsp-response
%attr(755,root,root) %{_datadir}/%{name}/kill-on-close
%attr(755,root,root) %{_datadir}/%{name}/setuidgid
%attr(755,root,root) %{_datadir}/%{name}/start_server
# TODO: use ca-certificates package
%{_datadir}/%{name}/ca-bundle.crt

%files devel
%defattr(644,root,root,755)
%{_includedir}/h2o.h
%{_includedir}/h2o
%{_libdir}/libh2o.so
%{_libdir}/libh2o-evloop.so
%{_pkgconfigdir}/libh2o.pc
%{_pkgconfigdir}/libh2o-evloop.pc
