# TODO
# - libwslay for websockets
#
# Conditional build:
%bcond_without	mruby		# using mruby scripting support (Rack-based)

Summary:	H2O - an optimized HTTP server with support for HTTP/1.x and HTTP/2
Name:		h2o
Version:	2.2.2
Release:	0.9
License:	MIT
Group:		Networking/Daemons/HTTP
Source0:	https://github.com/h2o/h2o/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	efc3a98cd21d3b91d66b2a99b1518255
Source1:	index.html
Source2:	%{name}.logrotate
Source3:	%{name}.init
Source4:	%{name}.service
Source5:	%{name}.conf
Patch0:		system-ca.patch
URL:		https://h2o.examp1e.net/
BuildRequires:	cmake >= 2.8.11
BuildRequires:	libstdc++-devel
BuildRequires:	libuv-devel >= 1.0.0
BuildRequires:	openssl-devel >= 1.0.2
BuildRequires:	pkgconfig
BuildRequires:	yaml-devel
BuildRequires:	zlib-devel
%if %{with mruby}
BuildRequires:	bison
BuildRequires:	ruby-devel
%endif
Requires:	ca-certificates
Requires:	perl-Encode
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_bindir %{_sbindir}

%description
H2O is a very fast HTTP server written in C

%package -n libh2o
Summary:	H2O Library compiled with libuv
Group:		Development/Libraries

%description -n libh2o
libh2o package provides H2O library compiled with libuv which allows
you to link your own software to H2O.

%package -n libh2o-evloop
Summary:	H2O Library compiled with its own event loop
Group:		Development/Libraries

%description -n libh2o-evloop
libh2o-evloop package provides H2O library compiled with its own event
loop which allows you to link your own software to H2O.

%package -n libh2o-devel
Summary:	Development interfaces for H2O
Group:		Development/Libraries
Requires:	libh2o = %{version}-%{release}
Requires:	libh2o-evloop = %{version}-%{release}
Requires:	openssl-devel

%description -n libh2o-devel
libh2o-devel package provides H2O header files and helpers which allow
you to build your own software using H2O.

%prep
%setup -q
%patch0 -p1

%build
install -d build
cd build
%cmake \
	-DBUILD_SHARED_LIBS=on \
	-DWITH_MRUBY=%{!?with_mruby:OFF}%{?with_mruby:ON} \
	..
%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install -C build \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},/etc/{rc.d/init.d,logrotate.d},%{systemdunitdir},%{systemdtmpfilesdir},%{_localstatedir}/{log,run}/h2o}

cp -p %{_sourcedir}/h2o.conf $RPM_BUILD_ROOT%{_sysconfdir}/h2o/h2o.conf
cp -p %{_sourcedir}/h2o.service $RPM_BUILD_ROOT%{systemdunitdir}/h2o.service
cp -p %{_sourcedir}/h2o.tmpfiles $RPM_BUILD_ROOT%{systemdtmpfilesdir}/h2o.conf
install -p %{_sourcedir}/h2o.init $RPM_BUILD_ROOT/etc/rc.d/init.d/h2o
cp -p %{_sourcedir}/h2o.logrotate $RPM_BUILD_ROOT/etc/logrotate.d/h2o

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart
%systemd_post %{name}.service

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi
%systemd_preun %{name}.service

%postun
%systemd_reload

%post	-n libh2o -p /sbin/ldconfig
%postun	-n libh2o -p /sbin/ldconfig

%post	-n libh2o-evloop -p /sbin/ldconfig
%postun	-n libh2o-evloop -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md Changes LICENSE
%attr(755,root,root) %{_sbindir}/h2o
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/h2o.conf
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/h2o
%attr(754,root,root) /etc/rc.d/init.d/h2o
%{systemdunitdir}/h2o.service
%{systemdtmpfilesdir}/h2o.conf
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/status
%attr(755,root,root) %{_datadir}/%{name}/annotate-backtrace-symbols
%attr(755,root,root) %{_datadir}/%{name}/fastcgi-cgi
%attr(755,root,root) %{_datadir}/%{name}/fetch-ocsp-response
%attr(755,root,root) %{_datadir}/%{name}/kill-on-close
%attr(755,root,root) %{_datadir}/%{name}/setuidgid
%attr(755,root,root) %{_datadir}/%{name}/start_server

%attr(710,root,nobody) %dir %{_localstatedir}/run/h2o
%attr(700,root,root) %dir %{_localstatedir}/log/h2o

%if %{with mruby}
%{_datadir}/%{name}/mruby
%endif

%files -n libh2o
%defattr(644,root,root,755)
%{_libdir}/libh2o.so.0.13
%attr(755,root,root) %{_libdir}/libh2o.so.*.*.*

%files -n libh2o-evloop
%defattr(644,root,root,755)
%{_libdir}/libh2o-evloop.so.0.13
%attr(755,root,root) %{_libdir}/libh2o-evloop.so.*.*.*

%files -n libh2o-devel
%defattr(644,root,root,755)
%{_includedir}/h2o.h
%{_includedir}/h2o
%{_libdir}/libh2o.so
%{_libdir}/libh2o-evloop.so
%{_pkgconfigdir}/libh2o.pc
%{_pkgconfigdir}/libh2o-evloop.pc
