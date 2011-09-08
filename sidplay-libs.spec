# SPEC file for sidplay-libs. Uses portion of the RPM for Mandriva by
# Goetz Waschk and Simon White. Developed for Fedora, imported to
# Dribble, migrated to RPMFusion.

Name:           sidplay-libs
Version:        2.1.1
Release:        11%{?dist}
Summary:        A software library for playing back C64 SID files
URL:            http://sidplay2.sourceforge.net/
Group:          System Environment/Libraries
Source0:        http://downloads.sourceforge.net/sidplay2/%{name}-%{version}.tar.gz
# This patch is just lifted from Debian, here:
# http://packages.debian.org/unstable/oldlibs/libsidplay2
Patch0:         sidplay-libs_2.1.1-7.diff.gz
# Build the builders as .so files please
Patch1:         sidplay-libs-2.1.1-dynamic-builders.patch
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
Obsoletes:      %{name}-static < %{version}-%{release}

%description devel
This package contains development files for the MOS Techology SID and
6510 chip emulator layer sidplay-libs.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
# Update to recent GNU autotools.
mkdir -p resid/unix
for i in libsidplay libsidutils builders/{resid-builder,hardsid-builder} resid . ; do
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
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc libsidplay/AUTHORS libsidplay/ChangeLog libsidplay/README libsidplay/TODO libsidplay/COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/sidplay

%changelog
* Thu Sep  8 2011 Hans de Goede <j.w.r.degoede@gmail.com> - 2.1.1-11
- Build builders as shared objects rather then as static libs
- Drop -static package
- Stop requiring libsidplay-devel for /usr/include/sidplay dir ownership,
  instead just co-own it

* Wed Aug 26 2009 Linus Walleij <triad@df.lth.se> 2.1.1-10
- Make the library position independent with -fPIC at the
  request of Orcan Ogetbil for XMMS2

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1-9
- rebuild for new F11 features

* Tue Nov 11 2008 Linus Walleij <triad@df.lth.se> 2.1.1-8
- CVS checkin mangles the patch so I have to add it as
  a .gz file instead!

* Tue Nov 11 2008 Linus Walleij <triad@df.lth.se> 2.1.1-7
- Update patch from Debian so we compile again.
- Import to RPMFusion and try to build it there.

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
