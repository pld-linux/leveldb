#
# Conditional build:
%bcond_without	tcmalloc	# don't use tcmalloc
%bcond_without	tests		# build without tests

%ifarch x32
%undefine	with_tcmalloc
%endif

Summary:	LevelDB - key-value store library
Summary(pl.UTF-8):	LevelDB - biblioteka bazy danych klucz-wartość
Name:		leveldb
Version:	1.18
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://github.com/google/leveldb/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	73770de34a2a5ab34498d2e05b2b7fa0
URL:		https://github.com/google/leveldb
BuildRequires:	libstdc++-devel
%{?with_tcmalloc:BuildRequires:	libtcmalloc-devel}
BuildRequires:	snappy-devel
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
Requires:	libstdc++-devel
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

%build
%{__make} \
	CXX="%{__cxx}" \
	OPT="%{rpmcflags} %{!?debug:-DNDEBUG}"

%if %{with tests}
%{__make} check \
	CXX="%{__cxx}" \
	OPT="%{rpmcflags} %{!?debug:-DNDEBUG}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}

cp -dp libleveldb.so* libleveldb.a $RPM_BUILD_ROOT%{_libdir}
cp -a include/leveldb $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE NEWS README TODO
%attr(755,root,root) %{_libdir}/libleveldb.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libleveldb.so.1

%files devel
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_libdir}/libleveldb.so
%{_includedir}/leveldb

%files static
%defattr(644,root,root,755)
%{_libdir}/libleveldb.a
