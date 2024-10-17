%global optflags %{optflags} -Oz

%define fname sysfs
%define major 2
%define libname %mklibname %{fname} %{major}
%define devname %mklibname %{fname} -d
%define static %mklibname %{fname} -d -s

Summary:	Utility suite to enjoy sysfs
Name:		sysfsutils
Version:	2.1.0
Release:	44
URL:		https://linux-diag.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/linux-diag/%{name}-%{version}.tar.bz2
Source1:	%{name}.rpmlintrc
License:	GPLv2
Group:		System/Kernel and hardware
Patch0:		sysfsutils-2.0.0-class-dup.patch
Patch1:		sysfsutils-2.1.0-get_link.patch
Patch2:		sysfsutils-2.1.0-srcdir-include.patch
Patch3:		sysfsutils-automake-1.13.patch
BuildRequires:	glibc-devel

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

%package -n %{libname}
Summary:	Main library for %{name}
License:	LGPLv2.1
Group:		System/Libraries

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with %{name}. The libsysfs library enables to access system devices.

%package -n %{devname}
Summary:	Headers for developing programs that will use %{name}
License:	LGPLv2.1
Group:		Development/C
Requires:	%{libname} = %{EVRD}
# for Turbolinux compatibility:
Provides:	sysfsutils-devel = %{EVRD}
Obsoletes:	%{mklibname %{fname} 2 -d} < 2.1.0-42
Conflicts:	%{_lib}sysfs1-devel < 2.1.0

%description -n %{devname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package -n %{static}
Summary:	Static library for developing programs that will use %{name}
License:	LGPLv2.1
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	%{devname} = %{version}
Obsoletes:	%{mklibname %{fname} 2 -d -s} < 2.1.0-42
Provides:	sysfsutils-static-devel = %{EVRD}

%description -n %{static}
This package contains the static library that programmers will need to develop
applications which will use %{name}.

%prep
%autosetup -p1
autoreconf -fi -Im4

%build
%configure \
	--enable-static

%make_build

%install
%make_install

%files
%doc AUTHORS README NEWS
%{_bindir}/systool
%{_bindir}/dlist_test
%{_bindir}/get_device
%{_bindir}/get_driver
%{_bindir}/get_module
%doc %{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libsysfs.so.%{major}*

%files -n %{devname}
%doc docs/libsysfs.txt
%{_libdir}/libsysfs.so
%{_includedir}/sysfs/libsysfs.h
%{_includedir}/sysfs/dlist.h

%files -n %{static}
%{_libdir}/libsysfs.a
