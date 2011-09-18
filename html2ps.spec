Name:           html2ps
Version:        1.0
Release:        0.4.b5%{?dist}
Summary:        HTML to PostScript converter

Group:          Applications/Publishing
License:        GPLv2+
URL:            http://user.it.uu.se/~jan/html2ps.html
Source0:        http://user.it.uu.se/~jan/html2ps-1.0b5.tar.gz
Source1:        xhtml2ps.desktop
Patch0:         http://ftp.de.debian.org/debian/pool/main/h/html2ps/html2ps_1.0b5-5.diff.gz
# use xdg-open in xhtml2ps
Patch1:         html2ps-1.0b5-xdg-open.patch
# patch config file from debian to use dvips, avoid using weblint 
# don't set letter as default page type, paperconf will set the default
Patch2:         html2ps-1.0b5-config.patch
# Backport security fix from 1.0b6 but do not inhibit SSI (#526513)
Patch3:         html2ps-1.0b5-ssi_traversal.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  desktop-file-utils
# Depend on paperconf directly (instead of libpaper package) for rpmlint sake
Requires:       tex(tex) tex(dvips) ghostscript /usr/bin/paperconf
# not autodetected since they are called by require not at the beginning of 
# line
Requires:       perl(LWP::UserAgent) perl(HTTP::Cookies) perl(HTTP::Request)

%description
An HTML to PostScript converter written in Perl.
* Many possibilities to control the appearance. 
* Support for processing multiple documents.
* A table of contents can be generated.
* Configurable page headers/footers.
* Automatic hyphenation and text justification can be selected. 


%package -n xhtml2ps
Summary:     GUI front-end for html2ps
Group:       User Interface/X
Requires:    html2ps = %{version}-%{release}
Requires:    xdg-utils

%description -n xhtml2ps
X-html2ps is freely-available GUI front-end for html2ps, a HTML-to-PostScript
converter.


%prep
%setup -q -n %{name}-1.0b5
%patch0 -p1
%patch1 -p1 -b .xdg-open
%patch2 -p1 -b .config
%patch3 -p1 -b .ssi_traversal

# convert README to utf8
iconv -f latin1 -t utf8 < README > README.utf8
touch -c -r README README.utf8
mv README.utf8 README

patch -p1 < debian/patches/01_manpages.dpatch
patch -p1 < debian/patches/03_html2ps.dpatch

%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man{1,5}

sed -e 's;/etc/html2psrc;%{_sysconfdir}/html2psrc;' \
    -e 's;/usr/share/doc/html2ps;%{_docdir}/%{name}-%{version};' \
        html2ps > $RPM_BUILD_ROOT%{_bindir}/html2ps
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/html2ps
install -p -m0644 html2ps.1 $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m0644 html2psrc.5 $RPM_BUILD_ROOT%{_mandir}/man5
sed -e 's;/usr/bin;%{_bindir};' \
    -e 's;/usr/share/texmf-texlive;%{_datadir}/texmf;' \
    debian/config/html2psrc > $RPM_BUILD_ROOT%{_sysconfdir}/html2psrc

install -m0755 -p contrib/xhtml2ps/xhtml2ps $RPM_BUILD_ROOT%{_bindir}
desktop-file-install --vendor="fedora"               \
  --dir=${RPM_BUILD_ROOT}%{_datadir}/applications         \
  %{SOURCE1}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README sample html2ps.html
%config(noreplace) %{_sysconfdir}/html2psrc
%{_bindir}/html2ps
%{_mandir}/man1/html2ps.1*
%{_mandir}/man5/html2psrc.5*

%files -n xhtml2ps
%defattr(-,root,root,-)
%doc contrib/xhtml2ps/README contrib/xhtml2ps/LICENSE
%{_bindir}/xhtml2ps
%{_datadir}/applications/*xhtml2ps.desktop

%changelog
* Mon Apr 27 2010 Petr Pisar <ppisar@redhat.com> - 1.0-0.4.b5
- Fix spelling
- Default attributes for xhtml2ps %%files
- Backport SSI traversal fix from 1.0b6 upstream version (#586356)
- Replace libpaper dependency with paperconf binary to make rpmlint happy

* Mon Apr 26 2010 Dennis Gregorovic <dgregor@redhat.com> - 1.0-0.3.b5.1
- Rebuilt for RHEL 6
Related: rhbz#566527

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.3.b5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.2.b5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Apr 18 2008 Patrice Dumas <pertusus@free.fr> 1.0-0.1.b5
- initial release
