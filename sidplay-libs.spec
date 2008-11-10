# SPEC file for sidplay-libs, primary target is the Fedora 
# RPM repository. Uses portion of the RPM for Mandriva by
# Goetz Waschk and Simon White.

Name:           sidplay-libs
Version:        2.1.1
Release:        6%{?dist}
Summary:        A software library for playing back C64 SID files
URL:            http://sidplay2.sourceforge.net/
Group:          System Environment/Libraries
Source0:        http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# This patch is just lifted from Debian, here:
# http://packages.debian.org/etch/libsidplay2
Patch0:         sidplay-libs_2.1.1-5.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
License:        GPLv2+
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool

%description
This package provides a software library for controlling emulation on the low 
machine-level of a MOS Technology SID chip and a MOS Technology 6510 processor.
Physical emulation internally utilize the resid library or alternatively use 
a hardware SID chip if the apropriate hardware ("hardsid") is installed. The
resid library is included with sidplay-libs.

%package devel
Summary:        Development files for sidplay-libs
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
# We require libsidplay, since that version owns the subdirectory
# "sidplay" in %{_includedir}.
Requires:       libsidplay-devel
Requires:	pkgconfig

%description devel
This package contains development files for the MOS Techology SID and
6510 chip emulator layer sidplay-libs.

%package static
Summary:        Static libraries and libtool archives for sidplay-libs
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-devel = %{version}-%{release}

%description static
This package contains some static libraries from sidplay-libs, which are
needed at compile-time by e.g. sidplay2, since it makes use of the
libtool archives.

%prep
%setup -q
%patch0 -p1
# Update to recent GNU autotools.
mkdir -p resid/unix
for i in libsidplay builders/{resid-builder,hardsid-builder} resid . ; do
    pushd $i
    aclocal -I unix
    libtoolize --copy --force
    automake
    autoconf
    popd
done

# Fix spurious permission problem (it's not installed
# with this permission, but anyway...)
chmod -x libsidutils/include/sidplay/utils/SidUsage.h

%build
# Cannot use --disable-static here, the builder need static
# libraries to work at all.
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

# Hack to prevent relinking, from Mandriva package.
# sed s/relink_command.*// < libsidutils/src/libsidutils.la > tmp.la
# mv tmp.la libsidutils/src/libsidutils.la
make install DESTDIR=$RPM_BUILD_ROOT

# Move stuff around - making install from the build
# tree for some reason put all files in all the wrong
# places.
mkdir $RPM_BUILD_ROOT%{_libdir}/sidplay
mkdir $RPM_BUILD_ROOT%{_libdir}/sidplay/builders
mv $RPM_BUILD_ROOT%{_libdir}/libhardsid-builder* \
   $RPM_BUILD_ROOT%{_libdir}/sidplay/builders
mv $RPM_BUILD_ROOT%{_libdir}/libresid-builder* \
   $RPM_BUILD_ROOT%{_libdir}/sidplay/builders

# Needed in Mandrake spec?
# chrpath -d %buildroot%{_libdir}/libsidutils.so

# This stuff cannot be removed as of now: it is referenced
# internally and used by the library configuration.
# Remove static libraries
# rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
# Remove libtool archive remnants
# rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc libsidplay/AUTHORS libsidplay/ChangeLog libsidplay/README libsidplay/TODO libsidplay/COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root)
# The "libsidplay" package owns %{_includedir}/sidplay
%dir %{_includedir}/sidplay/builders
%dir %{_includedir}/sidplay/utils
%dir %{_libdir}/sidplay
%{_libdir}/*.so
%{_includedir}/sidplay/*.h
%{_includedir}/sidplay/builders/*.h
%{_includedir}/sidplay/utils/*.h
# pkgconfig owns this dir
%{_libdir}/pkgconfig/*.pc

%files static
%dir %{_libdir}/sidplay/builders
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/sidplay/builders/*.a
%{_libdir}/sidplay/builders/*.la

%changelog
* Mon Dec 10 2007 Linus Walleij <triad@df.lth.se> 2.1.1-6
- Fixup issues found during review by Ian Chapman

* Mon Dec 3 2007 Linus Walleij <triad@df.lth.se> 2.1.1-5
- Fixup issues found during pre-review by Dribble Admin

* Mon Nov 19 2007 Linus Walleij <triad@df.lth.se> 2.1.1-4
- Rebased on the Debian package, which WORKS.

* Sun Sep 18 2005 Linus Walleij <triad@df.lth.se> 2.1.1-3
- Fixed the optimization problem...

* Thu Sep 15 2005 Linus Walleij <triad@df.lth.se> 2.1.1-2
- Fixed dependency on libsidplay.

* Sat Sep 10 2005 Linus Walleij <triad@df.lth.se> 2.1.1-1
- First try at a sidplay-libraries RPM.
