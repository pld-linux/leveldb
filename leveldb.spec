#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	tcmalloc	# tcmalloc usage
%bcond_without	tests		# unit tests

%ifarch x32
%undefine	with_tcmalloc
%endif
Summary:	LevelDB - key-value store library
Summary(pl.UTF-8):	LevelDB - biblioteka bazy danych klucz-wartość
Name:		leveldb
Version:	1.23
Release:	2
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/google/leveldb/releases
Source0:	https://github.com/google/leveldb/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	afbde776fb8760312009963f09a586c7
Patch0:		%{name}-system-libs.patch
Patch1:		%{name}-rtti.patch
URL:		https://github.com/google/leveldb
BuildRequires:	cmake >= 3.9
%{?with_tests:BuildRequires:	gmock-devel}
%{?with_tests:BuildRequires:	google-benchmark-devel}
%{?with_tests:BuildRequires:	gtest-devel}
BuildRequires:	libstdc++-devel >= 6:4.7
%{?with_tcmalloc:BuildRequires:	libtcmalloc-devel}
BuildRequires:	snappy-devel
# sqlite3-devel kyotocabinet-devel for benchmarks
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LevelDB is a fast key-value storage library written at Google that
provides an ordered mapping from string keys to string values.

%description -l pl.UTF-8
LevelDB to napisana w Google szybka biblioteka do przechowywania par
klucz-wartość, udostępniająca uporządkowane odwzorowanie z kluczy
będących łańcuchami znaków do wartości tego samego typu.

%package devel
Summary:	Header files for LevelDB library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LevelDB
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:4.7
%{?with_tcmalloc:Requires: libtcmalloc-devel}
Requires:	snappy-devel

%description devel
Header files for LevelDB library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LevelDB.

%package static
Summary:	Static LevelDB library
Summary(pl.UTF-8):	Statyczna biblioteka LevelDB
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LevelDB library.

%description static -l pl.UTF-8
Statyczna biblioteka LevelDB.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%if %{with static_libs}
install -d build-static
cd build-static
%cmake .. \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	%{!?with_tests:-DLEVELDB_BUILD_TESTS:BOOL=OFF} \
	-DLEVELDB_BUILD_BENCHMARKS:BOOL=OFF

%{__make}
cd ..
%endif

install -d build
cd build
%cmake .. \
	%{!?with_tests:-DLEVELDB_BUILD_TESTS:BOOL=OFF} \
	-DLEVELDB_BUILD_BENCHMARKS:BOOL=OFF

%{__make}

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE NEWS README.md TODO
%attr(755,root,root) %{_libdir}/libleveldb.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libleveldb.so.1

%files devel
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_libdir}/libleveldb.so
%{_includedir}/leveldb
%{_libdir}/cmake/leveldb

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libleveldb.a
%endif
