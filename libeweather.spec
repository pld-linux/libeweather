#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Enlightenment weather library
Summary(pl.UTF-8):	Biblioteka informacji pogodowych dla środowiska Enlightenment
Name:		libeweather
Version:	0.2.0
%define	snap	20130810
Release:	0.%{snap}.2
License:	LGPL v2.1
Group:		Libraries
# git clone http://git.enlightenment.org/libs/libeweather.git
Source0:	%{name}.tar.xz
# Source0-md5:	4a653fdab6b297781a3a80abae560623
Patch0:		%{name}-dirs.patch
URL:		http://git.enlightenment.org/libs/libeweather.git/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1.6
BuildRequires:	ecore-devel >= 1.0.0
BuildRequires:	ecore-con-devel >= 1.0.0
BuildRequires:	ecore-evas-devel >= 1.0.0
BuildRequires:	ecore-file-devel >= 1.0.0
BuildRequires:	edje-devel >= 1.0.0
BuildRequires:	eina-devel >= 1.0.0
BuildRequires:	evas-devel >= 1.0.0
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 1:0.22
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	ecore >= 1.0.0
Requires:	ecore-con >= 1.0.0
Requires:	ecore-evas >= 1.0.0
Requires:	ecore-file >= 1.0.0
Requires:	edje-libs >= 1.0.0
Requires:	eina >= 1.0.0
Requires:	evas >= 1.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Enlightenment weather library.

%description -l pl.UTF-8
Biblioteka informacji pogodowych dla środowiska Enlightenment.

%package devel
Summary:	Header files for Eweather library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Eweather
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ecore-devel >= 1.0.0
Requires:	ecore-con-devel >= 1.0.0
Requires:	ecore-evas-devel >= 1.0.0
Requires:	ecore-file-devel >= 1.0.0
Requires:	edje-devel >= 1.0.0
Requires:	eina-devel >= 1.0.0
Requires:	evas-devel >= 1.0.0

%description devel
Header files for Eweather library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Eweather.

%package static
Summary:	Static Eweather library
Summary(pl.UTF-8):	Statyczna biblioteka Eweather
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Eweather library.

%description static -l pl.UTF-8
Statyczna biblioteka Eweather.

%prep
%setup -q -n %{name}
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# loadable modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/eweather/plugins/*.la
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libeweather.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING-PLAIN README
%attr(755,root,root) %{_bindir}/eweather_test
%attr(755,root,root) %{_libdir}/libeweather.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libeweather.so.0
%dir %{_libdir}/eweather
%dir %{_libdir}/eweather/plugins
%attr(755,root,root) %{_libdir}/eweather/plugins/test.so
%attr(755,root,root) %{_libdir}/eweather/plugins/yahoo.so
%{_datadir}/eweather

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libeweather.so
%{_includedir}/EWeather*.h
%{_pkgconfigdir}/eweather.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libeweather.a
%endif
