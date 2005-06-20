Name: R
Version: 2.1.1
Release: 1%{?dist}
Summary: A language for data analysis and graphics
URL: http://www.r-project.org
Source0: ftp://cran.r-project.org/pub/R/src/base/R-2/R-%{version}.tar.gz
License: GPL
Group: Applications/Engineering
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gcc-g77
BuildRequires: gcc-c++, tetex-latex, texinfo 
BuildRequires: libpng-devel, libjpeg-devel, readline-devel, libtermcap-devel
BuildRequires: XFree86-devel
BuildRequires: tcl-devel, tk-devel
BuildRequires: blas >= 3.0, pcre-devel, zlib-devel
Requires: ggv, cups, firefox

# These are the submodules that R provides. Sometimes R modules say they
# depend on one of these submodules rather than just R. These are 
# provided for packager convenience. 
Provides: R-base = %{version}
Provides: R-boot = %{version}
Provides: R-class = %{version}
Provides: R-cluster = %{version}
Provides: R-datasets = %{version}
Provides: R-foreign = %{version}
Provides: R-graphics = %{version}
Provides: R-grDevices = %{version}
Provides: R-grid = %{version}
Provides: R-KernSmooth = %{version}
Provides: R-lattice = %{version}
Provides: R-MASS = %{version}
Provides: R-methods = %{version}
Provides: R-mgcv = %{version}
Provides: R-nlme = %{version}
Provides: R-nnet = %{version}
Provides: R-rpart = %{version}
Provides: R-spatial = %{version}
Provides: R-splines = %{version}
Provides: R-stats = %{version}
Provides: R-stats4 = %{version}
Provides: R-survival = %{version}
Provides: R-tcltk = %{version}
Provides: R-tools = %{version}
Provides: R-utils = %{version}
Provides: R-VR = %{version}

# Temporary fix to avoid the SNAFU of the 0.fdr.2.* release
Conflicts: R-devel < %{version}-%{release}

%description
A language and environment for statistical computing and graphics. 
R is similar to the award-winning S system, which was developed at 
Bell Laboratories by John Chambers et al. It provides a wide 
variety of statistical and graphical techniques (linear and
nonlinear modelling, statistical tests, time series analysis,
classification, clustering, ...).

R is designed as a true computer language with control-flow
constructions for iteration and alternation, and it allows users to
add additional functionality by defining new functions. For
computationally intensive tasks, C, C++ and Fortran code can be linked
and called at run time.

%package devel
Summary: files for development of R packages.
Group: Applications/Engineering
Requires: R = %{version}
# You need all the BuildRequires for the development version
Requires: gcc-c++, gcc-g77, tetex-latex, texinfo 
Requires: libpng-devel, libjpeg-devel, readline-devel, libtermcap-devel
Requires: XFree86-devel
Requires: tcl-devel, tk-devel

%description devel
Install R-devel if you are going to develop or compile R packages.

%package -n libRmath
Summary: standalone math library from the R project
Group: Development/Libraries

%description -n libRmath
A standalone library of mathematical and statistical functions derived
from the R project.  This packages provides the shared libRmath library.

%package -n libRmath-devel
Summary: standalone math library from the R project
Group: Development/Libraries
Requires: libRmath = %{version}

%description -n libRmath-devel
A standalone library of mathematical and statistical functions derived
from the R project.  This packages provides the static libRmath library
and header files.

%prep
%setup -q 

%build
export R_PDFVIEWER="%{_bindir}/ggv"
export R_PRINTCMD="lpr"
export R_BROWSER="%{_bindir}/firefox"
export F77="g77"
( %configure \
    --with-tcl-config=%{_libdir}/tclConfig.sh \
    --with-tk-config=%{_libdir}/tkConfig.sh \
    --enable-R-shlib )\
 | egrep '^R is now|^ |^$' - > CAPABILITIES
make 
(cd src/nmath/standalone; make)
#make check-all
make pdf
make info

%install

%makeinstall rhome=${RPM_BUILD_ROOT}%{_libdir}/R install-info
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir.old

#Install libRmath files
(cd src/nmath/standalone; make install \
    includedir=${RPM_BUILD_ROOT}%{_includedir} \
    libdir=${RPM_BUILD_ROOT}%{_libdir})

#Fix location of R_HOME_DIR in shell wrapper.
#
sed -e "s@R_HOME_DIR=.*@R_HOME_DIR=%{_libdir}/R@" < bin/R \
  > ${RPM_BUILD_ROOT}%{_libdir}/R/bin/R
sed -e "s@R_HOME_DIR=.*@R_HOME_DIR=%{_libdir}/R@" < bin/R \
   > ${RPM_BUILD_ROOT}%{_bindir}/R
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/R/bin/R 
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/R

# Remove package indices. They are rebuilt by the postinstall script.
#
rm -f ${RPM_BUILD_ROOT}%{_libdir}/R/doc/html/function.html
rm -f ${RPM_BUILD_ROOT}%{_libdir}/R/doc/html/packages.html
rm -f ${RPM_BUILD_ROOT}%{_libdir}/R/doc/html/search/index.txt

# Some doc files are also installed. We don't need them
(cd %{buildroot}%{_libdir}/R;
 rm -f AUTHORS COPYING COPYING.LIB COPYRIGHTS FAQ NEWS ONEWS RESOURCES THANKS)

mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo "%{_libdir}/R/lib" > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}-%{_arch}.conf

%files
%defattr(-, root, root)
%{_bindir}/R
%{_libdir}/R
%{_infodir}/R-*.info*
%{_mandir}/man1/*
/etc/ld.so.conf.d/*
%doc AUTHORS CAPABILITIES COPYING COPYING.LIB COPYRIGHTS FAQ NEWS
%doc ONEWS README RESOURCES THANKS VERSION Y2K
%doc doc/manual/R-admin.pdf
%doc doc/manual/R-FAQ.pdf
%doc doc/manual/R-lang.pdf
%doc doc/manual/R-data.pdf
%doc doc/manual/R-intro.pdf

%files devel
%defattr(-, root, root)
%doc doc/manual/R-exts.pdf

%files -n libRmath
%defattr(-, root, root)
%{_libdir}/libRmath.so

%files -n libRmath-devel
%defattr(-, root, root)
%{_libdir}/libRmath.a
%{_includedir}/Rmath.h

%clean
rm -rf ${RPM_BUILD_ROOT};

%post 
# Create directory entries for info files
# (optional doc files, so we must check that they are installed)
for doc in admin exts FAQ intro lang; do
   file=%{_infodir}/R-${doc}.info.gz
   if [ -e $file ]; then
      /sbin/install-info ${file} %{_infodir}/dir 2>/dev/null
   fi
done
/sbin/ldconfig

%postun
/sbin/ldconfig

# Update package indices
%{_bindir}/R CMD perl %{_libdir}/R/share/perl/build-help.pl --htmllists > /dev/null 2>/dev/null
%__cat %{_libdir}/R/library/*/CONTENTS > %{_libdir}/R/doc/html/search/index.txt 2>/dev/null

%preun 
if [ $1 = 0 ]; then
   # Delete directory entries for info files (if they were installed)
   for doc in admin exts FAQ intro lang; do
      file=%{_infodir}/R-${doc}.info.gz
      if [ -e ${file} ]; then
         /sbin/install-info --delete R-${doc} %{_infodir}/dir 2>/dev/null
      fi
   done
   # Remove package indices
   %__rm -f %{_libdir}/R/doc/html/function.html
   %__rm -f %{_libdir}/R/doc/html/packages.html
   %__rm -f %{_libdir}/R/doc/html/search/index.txt
fi

%post -n libRmath
/sbin/ldconfig

%postun -n libRmath
/sbin/ldconfig

%changelog
* Mon Jun 20 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.1-1
- bugfix update

* Mon Apr 18 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.0-2
- fix library handling

* Mon Apr 18 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.0-1
- 2.1.0, fc3 package
- The GNOME GUI is unbundled, now provided as a package on CRAN

* Sun Apr 17 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.0.1-12
- enable gnome gui (--with-gnome)

* Thu Apr 14 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-11
- little bump. This is the fc3 package.
- callout to ggv (fc3) instead of evince (fc4)
- BuildRequires: gcc-g77 instead of gcc-gfortran

* Thu Apr 14 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-10
- bump for cvs errors

* Mon Apr 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-9
- fix URL for Source0

* Mon Apr 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-8
- spec file cleanup

* Fri Apr  1 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-7
- use evince instead of ggv
- make custom provides for R subfunctions

* Wed Mar 30 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-6
- configure now calls --enable-R-shlib

* Thu Mar 24 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-5
- cleaned up package for Fedora Extras

* Mon Feb 28 2005 Martyn Plummer <plummer@iarc.fr> 0:2.0.1-0.fdr.4
- Fixed file ownership in R-devel and libRmath packages

* Wed Feb 16 2005 Martyn Plummer <plummer@iarc.fr> 0:2.0.1-0.fdr.3
- R-devel package is now a stub package with no files, except a documentation
  file (RPM won't accept sub-packages with no files). R now conflicts
  with earlier (i.e 0:2.0.1-0.fdr.2) versions of R-devel.
- Created libRmath subpackage with shared library.

* Mon Jan 31 2005 Martyn Plummer <plummer@iarc.fr> 0:2.0.1-0.fdr.2
- Created R-devel and libRmath-devel subpackages

* Mon Nov 15 2004 Martyn Plummer <plummer@iarc.fr> 0:2.0.1-0.fdr.1
- Built R 2.0.1

* Wed Nov 10 2004 Martyn Plummer <plummer@iarc.fr> 0:2.0.0-0.fdr.3
- Set R_PRINTCMD at configure times so that by default getOption(printcmd)
  gives "lpr".
- Define macro fcx for all Fedora distributions. This replaces Rinfo

* Tue Oct 12 2004 Martyn Plummer <plummer@iarc.fr> 0:2.0.0-0.fdr.2
- Info support is now conditional on the macro Rinfo, which is only
  defined for Fedora 1 and 2. 

* Thu Oct 7 2004 Martyn Plummer <plummer@iarc.fr> 0:2.0.0-0.fdr.1
- Built R 2.0.0
- There is no longer a BUGS file, so this is not installed as a 
  documentation file.

* Mon Aug  9 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.1-0.fdr.4
- Added gcc-g++ to the list of BuildRequires for all platforms.
  Although a C++ compiler is not necessary to build R, it must
  be present at configure time or R will not be correctly configured
  to build packages containing C++ code.

* Thu Jul  1 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.1-0.fdr.3
- Modified BuildRequires so we can support older Red Hat versions without
  defining any macros.

* Mon Jun 23 2004 Martyn Plummer <plummner@iarc.fr> 0:1.9.1-0.fdr.2
- Added libtermcap-devel as BuildRequires for RH 8.0 and 9. Without
  this we get no readline support.

* Mon Jun 21 2004 Martyn Plummer <plummner@iarc.fr> 0:1.9.1-0.fdr.1
- Build R 1.9.1
- Removed Xorg patch since fix is now in R sources

* Mon Jun 14 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.0-0.fdr.4
- Added XFree86-devel as conditional BuildRequires for rh9, rh80

* Wed Jun 08 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.0-0.fdr.3
- Corrected names for fc1/fc2/el3 when using conditional BuildRequires
- Configure searches for C++ preprocessor and fails if we don't have
  gcc-c++ installed. Added to BuildRequires for FC2.

* Tue Jun 08 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.0-0.fdr.2
- Added patch to overcome problems with X.org headers (backported
  from R 1.9.1; patch supplied by Graeme Ambler)
- Changed permissions of source files to 644 to please rpmlint

* Tue May 03 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.0-0.fdr.1
- R.spec file now has mode 644. Previously it was unreadable by other
  users and this was causing a crash building under mach.
- Changed version number to conform to Fedora conventions. 
- Removed Provides: and Obsoletes: R-base, R-recommended, which are
  now several years old. Nobody should have a copy of R-base on a 
  supported platform.
- Changed buildroot to Fedora standard
- Added Requires(post,preun): info
- Redirect output from postinstall/uninstall scripts to /dev/null
- Added BuildRequires tags necessary to install R with full 
  capabilities on a clean mach buildroot. Conditional buildrequires
  for tcl-devel and tk-devel which were not present on RH9 or earlier.

* Thu Apr 01 2004 Martyn Plummer <plummer@iarc.fr>
- Added patch to set environment variable LANG to C in shell wrapper,
  avoiding warnings about UTF-8 locale not being supported

* Mon Mar 15 2004 Martyn Plummer <plummer@iarc.fr>
- No need to export optimization flags. This is done by %configure
- Folded info installation into %makeinstall 
- Check that RPM_BASE_ROOT is not set to "/" before cleaning up

* Thu Feb 03 2004 Martyn Plummer <plummer@iarc.fr>
- Removed tcl-devel from BuildRequires

* Tue Feb 03 2004 Martyn Plummer <plummer@iarc.fr>
- Changes from James Henstridge <james@daa.com.au> to allow building on IA64:
- Added BuildRequires for tcl-devel tk-devel tetex-latex
- Use the %configure macro to call the configure script
- Pass --with-tcl-config and --with-tk-config arguments to configure
- Set rhome to point to the build root during "make install"

* Wed Jan 07 2004 Martyn Plummer <plummer@iarc.fr>
- Changed obsolete "copyright" field to "license"

* Fri Nov 21 2003 Martyn Plummer <plummer@iarc.fr>
- Built 1.8.1
