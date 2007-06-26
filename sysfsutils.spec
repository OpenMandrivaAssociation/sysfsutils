%define fname sysfs
%define lib_name_orig lib%{fname}
%define lib_major 2
%define lib_name %mklibname %{fname} %{lib_major}
%define develname %mklibname %{fname} -d
%define staticdevelname %mklibname %{fname} -d -s

Name: 		sysfsutils
Version: 	2.1.0
Release: 	%mkrel 4
URL:		http://linux-diag.sourceforge.net/
Source0: 	http://prdownloads.sourceforge.net/linux-diag/%{name}-%{version}.tar.bz2
License: 	GPL
Group: 		System/Kernel and hardware
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Summary: 	Utility suite to enjoy sysfs

%description
This package's purpose is to provide a set of utilities for interfacing
with sysfs, a virtual filesystem in Linux kernel versions 2.5+ that
provides a tree of system devices. While a filesystem is a very useful
interface, we've decided to provide a stable programming interface
that will hopefully make it easier for applications to query system devices
and their attributes.

This package currently includes:

- libsysfs: a library for accessing system devices.
- lsbus: a small application to query system bus information.
- systool: an application to view system device information by bus, class,
        and topology.

%package -n	%{lib_name}
Summary:	Main library for %{name}
Group:		System/Libraries
Provides:	%{lib_name_orig} = %{version}-%{release}

%description -n	%{lib_name}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%develname
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{lib_name} = %{version}
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	%{lib_name_orig}%{lib_major}-devel = %{version}-%{release}
Obsoletes:  %mklibname %{fname} 2 -d

%description -n	%develname
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package -n	%staticdevelname
Summary:	Static library for developing programs that will use %{name}
Group:		Development/C
Requires:	%{lib_name} = %{version} %develname = %{version} 
Provides:	%{lib_name_orig}-static-devel = %{version}-%{release}
Provides:	%{lib_name_orig}%{lib_major}-static-devel = %{version}-%{release}
Obsoletes:  %mklibname %{fname} 2 -d -s

%description -n	%staticdevelname
This package contains the static library that programmers will need to develop
applications which will use %{name}.


%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall_std}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS README NEWS 
%{_bindir}/systool
%{_bindir}/dlist_test
%{_bindir}/get_device
%{_bindir}/get_driver
%{_bindir}/get_module
#%{_bindir}/testlibsysfs
%{_mandir}/man1/*

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/libsysfs.so.%{lib_major}*

%files -n %develname
%defattr(-,root,root)
%doc docs/libsysfs.txt
%{_libdir}/libsysfs.so
%{_includedir}/sysfs/libsysfs.h
%{_includedir}/sysfs/dlist.h

%files -n %staticdevelname
%defattr(-,root,root)
%{_libdir}/libsysfs.a
%{_libdir}/libsysfs.la
