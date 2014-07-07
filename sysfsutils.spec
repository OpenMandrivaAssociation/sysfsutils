%define	fname	sysfs
%define	major	2
%define	libname	%mklibname %{fname} %{major}
%define	devname	%mklibname %{fname} -d
%define	static	%mklibname %{fname} -d -s

%bcond_without	dietlibc
%bcond_without	uclibc

Summary:	Utility suite to enjoy sysfs
Name:		sysfsutils
Version:	2.1.0
Release:	32
URL:		http://linux-diag.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/linux-diag/%{name}-%{version}.tar.bz2
License:	GPLv2
Group:		System/Kernel and hardware
Patch0:		sysfsutils-2.0.0-class-dup.patch
Patch1:		sysfsutils-2.1.0-get_link.patch
Patch2:		sysfsutils-2.1.0-srcdir-include.patch
Patch3:		sysfsutils-automake-1.13.patch
%if %{with dietlibc}
BuildRequires:	dietlibc-devel
%endif
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-9
%endif

%description
This package's purpose is to provide a set of utilities for interfacing
with sysfs, a virtual filesystem in Linux kernel versions 2.5+ that
provides a tree of system devices. While a filesystem is a very useful
interface, we've decided to provide a stable programming interface
that will hopefully make it easier for applications to query system devices
and their attributes.

This package currently includes:

- lsbus: a small application to query system bus information.
- systool: an application to view system device information by bus, class,
        and topology.

%package -n	%{libname}
Summary:	Main library for %{name}
License:	LGPLv2.1
Group:		System/Libraries

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}. The libsysfs library enables to access system devices.

%package -n	uclibc-%{libname}
Summary:	uClibc linked library for %{name}
License:	LGPLv2.1
Group:		System/Libraries

%description -n	uclibc-%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}. The libsysfs library enables to access system devices.

%package -n	%{devname}
Summary:	Headers for developing programs that will use %{name}
License:	LGPLv2.1
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
%if %{with uclibc}
Requires:	uclibc-%{libname} = %{version}-%{release}
%endif
# for Turbolinux compatibility:
Provides:	sysfsutils-devel = %{version}-%{release}
Obsoletes:	%mklibname %{fname} 2 -d
Conflicts:	%{_lib}sysfs1-devel < 2.1.0

%description -n	%{devname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package -n	%{static}
Summary:	Static library for developing programs that will use %{name}
License:	LGPLv2.1
Group:		Development/C
Requires:	%{libname} = %{version} %devname = %{version} 
Obsoletes:	%mklibname %{fname} 2 -d -s
Provides:	sysfsutils-static-devel = %{version}-%{release}

%description -n	%{static}
This package contains the static library that programmers will need to develop
applications which will use %{name}.


%prep
%setup -q
%apply_patches
autoreconf -fi -Im4

%build
CONFIGURE_TOP=$PWD
%if %{with dietlibc}
mkdir -p diet
pushd diet
%configure	CC="diet gcc" \
		--enable-static \
		--disable-shared
%make V=1 LD="diet ld" CFLAGS="-Os -g"
popd
%endif

%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%configure	CC="%{uclibc_cc}" \
		CFLAGS="%{uclibc_cflags}" \
		--enable-static \
		--enable-shared \
		--libdir=%{uclibc_root}/%{_lib}
%make V=1
popd
%endif

mkdir -p glibc
pushd glibc
%configure	--libdir=/%{_lib} \
		--enable-static
%make
popd

%install
%makeinstall_std -C glibc

install -d %{buildroot}%{_libdir}
mv %{buildroot}/%{_lib}/*.{so,a} %{buildroot}%{_libdir}
ln -rsf %{buildroot}/%{_lib}/libsysfs.so.%{major}.* %{buildroot}%{_libdir}/libsysfs.so

%if %{with dietlibc}
install -m644 ./diet/lib/.libs/libsysfs.a -D %{buildroot}%{_prefix}/lib/dietlibc/lib-%{_arch}/libsysfs.a
%endif

%if %{with uclibc}
%makeinstall_std -C uclibc/lib
install -d %{buildroot}%{uclibc_root}%{_libdir}
mv %{buildroot}%{uclibc_root}/%{_lib}/*.{so,a} %{buildroot}%{uclibc_root}%{_libdir}
ln -rsf %{buildroot}%{uclibc_root}/%{_lib}/libsysfs.so.%{major}.* %{buildroot}%{uclibc_root}%{_libdir}/libsysfs.so
%endif

%files
%doc AUTHORS README NEWS
%{_bindir}/systool
%{_bindir}/dlist_test
%{_bindir}/get_device
%{_bindir}/get_driver
%{_bindir}/get_module
#%{_bindir}/testlibsysfs
%{_mandir}/man1/*

%files -n %{libname}
/%{_lib}/libsysfs.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}/%{_lib}/libsysfs.so.%{major}*
%endif

%files -n %{devname}
%doc docs/libsysfs.txt
%{_libdir}/libsysfs.so
%{_includedir}/sysfs/libsysfs.h
%{_includedir}/sysfs/dlist.h
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libsysfs.so
%endif

%files -n %{static}
%{_libdir}/libsysfs.a
%if %{with dietlibc}
%{_prefix}/lib/dietlibc/lib-%{_arch}/libsysfs.a
%endif
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libsysfs.a
%endif
