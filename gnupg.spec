Summary:	GNU privacy guard - a free PGP replacement
Name:		gnupg
Version:	1.4.11
Release:	4
License:	GPLv3
Group:		File tools
URL:		http://www.gnupg.org
Source:		ftp://ftp.gnupg.org/gcrypt/gnupg/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.gnupg.org/gcrypt/gnupg/%{name}-%{version}.tar.bz2.sig
Source2:	mdk-keys.tar.bz2
Source3:	mdk-keys.tar.bz2.sig
Patch1:		gnupg-1.4.2.2-use-agent-by-default.diff
Patch4:		gnupg-1.4.5-ppc64.patch
# splitted off from the previous debian patch
Patch6:		gnupg-1.4.7-deb-free_caps.patch
Patch7:		gnupg-1.4.7-deb-manpage.patch
Patch8:		gnupg-1.4.7-deb-min_privileges.patch
#Patch10:	gnupg-1.4.6-dir.patch
BuildRequires:	bzip2-devel
BuildRequires:	docbook-utils
BuildRequires:	gettext
BuildRequires:	libcurl-devel >= 7.10
BuildRequires:	termcap-devel
BuildRequires:	libusb-devel
BuildRequires:	openldap-devel
BuildRequires:	perl
BuildRequires:	readline-devel
BuildRequires:	sendmail-command
BuildRequires:	bison

%description
GnuPG is GNU's tool for secure communication and data storage.
It can be used to encrypt data and to create digital signatures.
It includes an advanced key management facility and is compliant
with the proposed OpenPGP Internet standard as described in RFC2440.

%prep

%setup -q
%patch1 -p0 -b .use_agent
%patch4 -p1 -b .ppc64
%patch6 -p1 -b .free_caps
%patch7 -p1 -b .manpage
%patch8 -p1 -b .min_privileges
#patch10 -p1 -b .dir

%build
%serverbuild
%configure2_5x \
	--without-included-regex \
	--without-included-gettext \
	--without-included-zlib \
	--with-static-rnd=linux \
	--disable-rpath \
	--without-capabilities \
	--enable-noexecstack \
%ifarch %{sunsparc}
	--enable-m-guard
%else
	--disable-m-guard
%endif
%make

%check
# all tests must pass
make check

%install
rm -rf %{buildroot}

%makeinstall_std

sed -e "s#../g10/gpg#gpg#" < tools/lspgpot > %{buildroot}%{_bindir}/lspgpot

perl -pi -e 's|/usr/local|/usr/|' %{buildroot}%{_mandir}/man1/gpg.1

# install some extra man pages by debian
install -m0644 debian/gpgsplit.1 %{buildroot}%{_mandir}/man1/
install -m0644 debian/lspgpot.1 %{buildroot}%{_mandir}/man1/

# installed but not wanted
rm -f %{buildroot}%{_datadir}/gnupg/{FAQ,faq.html}
rm -f %{buildroot}%{_datadir}/locale/locale.alias

mkdir -p %{buildroot}%{_sysconfdir}/RPM-GPG-KEYS
tar xvjf %{SOURCE2} -C %{buildroot}%{_sysconfdir}/RPM-GPG-KEYS

%{find_lang} %{name}


%files -f %{name}.lang
%defattr(-,root,root)
%doc README NEWS THANKS TODO doc/DETAILS doc/FAQ doc/HACKING
%doc doc/OpenPGP doc/samplekeys.asc
%doc doc/gpgv.texi
%attr(0755,root,root) %{_bindir}/gpg
%attr(0755,root,root) %{_bindir}/gpgv
%attr(0755,root,root) %{_bindir}/lspgpot
%attr(0755,root,root) %{_bindir}/gpgsplit
%attr(0755,root,root) %{_bindir}/gpg-zip
%dir %{_libdir}/gnupg
%attr(0755,root,root) %{_libdir}/gnupg/gpgkeys_curl
%attr(0755,root,root) %{_libdir}/gnupg/gpgkeys_finger
%attr(0755,root,root) %{_libdir}/gnupg/gpgkeys_hkp
%attr(0755,root,root) %{_libdir}/gnupg/gpgkeys_ldap
%dir %{_datadir}/gnupg
%{_datadir}/gnupg/options.skel
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_infodir}/gnupg1.info*
%dir %{_sysconfdir}/RPM-GPG-KEYS
%attr(0644,root,root) %{_sysconfdir}/RPM-GPG-KEYS/*.asc


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.11-2mdv2011.0
+ Revision: 664903
- mass rebuild

* Mon Oct 18 2010 Lonyai Gergely <aleph@mandriva.org> 1.4.11-1mdv2011.0
+ Revision: 586621
- 1.4.11

* Mon Feb 01 2010 Pascal Terjan <pterjan@mandriva.org> 1.4.10-2mdv2010.1
+ Revision: 499355
- Do not install gpg setuid root, this is no longer needed since kernel 2.6.9

* Thu Sep 03 2009 Lonyai Gergely <aleph@mandriva.org> 1.4.10-1mdv2010.0
+ Revision: 427739
- update to 1.4.10

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.4.9-9mdv2010.0
+ Revision: 425017
- rebuild

* Wed Feb 25 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4.9-8mdv2009.1
+ Revision: 344701
- rebuilt against new readline

* Sun Jan 04 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4.9-7mdv2009.1
+ Revision: 324380
- disable capabilities, seems unsupported by the build system

* Tue Dec 30 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.9-6mdv2009.1
+ Revision: 321398
- drop the CVE-2006-3082 patch, allready in there... (caught by --fuzz=0)
- rediffed P4
- fix deps (cap-devel)

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 1.4.9-5mdv2009.0
+ Revision: 264604
- rebuild early 2009.0 package (before pixel changes)

* Thu May 22 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.9-4mdv2009.0
+ Revision: 210054
- really fix the install-info error this time

* Thu May 22 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.9-3mdv2009.0
+ Revision: 210014
- fix "install-info: menu item `gpg' already exists, for
  file `gpg'" with a patch from fedora

* Wed May 21 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.9-2mdv2009.0
+ Revision: 209746
- added one gcc43 patch (debian)

* Thu Mar 27 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4.9-1mdv2008.1
+ Revision: 190619
- 1.4.9 (fixes #39429 (vulns in gnupg 1.4.8 and gnupg2 2.0.8))

* Wed Jan 23 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.4.8-2mdv2008.1
+ Revision: 157158
- use system libraries
- nuke rpath
- add missing buildrequires on bison
- provide linux capabilities
- new license policy

* Wed Jan 02 2008 Andreas Hasenack <andreas@mandriva.com> 1.4.8-1mdv2008.1
+ Revision: 140616
- updated to version 1.4.8

* Mon Dec 24 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.7-9mdv2008.1
+ Revision: 137464
- rebuilt against openldap-2.4.7 libs

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Sep 20 2007 Olivier Blin <oblin@mandriva.com> 1.4.7-8mdv2008.0
+ Revision: 91481
- do not package ChangeLog, we already have NEWS
- do not package faq.raw, we already have the text and html versions

* Tue Sep 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.7-7mdv2008.0
+ Revision: 89682
- rebuild

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 1.4.7-6mdv2008.0
+ Revision: 69905
- kill file require on info-install

* Wed Jun 27 2007 Andreas Hasenack <andreas@mandriva.com> 1.4.7-5mdv2008.0
+ Revision: 45083
- using serverbuild macro (-fstack-protector-all)

  + Per Ã˜yvind Karlsen <peroyvind@mandriva.org>
    --enable-m-guard on all sparcs (%%{sunsparc})
    - make it actually work (strip '\')


* Mon Mar 19 2007 Thierry Vignaud <tvignaud@mandriva.com> 1.4.7-4mdv2007.1
+ Revision: 146609
- do not package sources of info pages

* Thu Mar 15 2007 Andreas Hasenack <andreas@mandriva.com> 1.4.7-2mdv2007.1
+ Revision: 144347
- workaround to avoid having to conflict with gnupg2

* Wed Mar 14 2007 Andreas Hasenack <andreas@mandriva.com> 1.4.7-1mdv2007.1
+ Revision: 143694
- updated to version 1.4.7
- removed patches that were already applied
- debian patches were splitted: taking them from the
  MDV 2007.0 official update

* Tue Jan 02 2007 Andreas Hasenack <andreas@mandriva.com> 1.4.5-5mdv2007.1
+ Revision: 103132
- added security patch for CVE-2006-6235

  + Gwenole Beauchesne <gbeauchesne@mandriva.com>
    - use parallel build
    - add ppc64 support

* Fri Dec 01 2006 Andreas Hasenack <andreas@mandriva.com> 1.4.5-3mdv2007.1
+ Revision: 89664
- require default libcurl-devel
- get rid of svn warning
- bump release for rebuild
- fix overflow (upstream bug 728)

  + JÃ©rÃ´me Soyer <saispo@mandriva.org>
    - Rebuild with the new curl

* Wed Aug 02 2006 Andreas Hasenack <andreas@mandriva.com> 1.4.5-1mdv2007.0
+ Revision: 42918
- removed 23_getkey_utf8_userid and 25_de.po_fixes from debian
  patches, already applied/fixed upstream
- updated to version 1.4.5 (doesn't build yet, hang on)
- fixed svn warning (/me testing srpm2svn.sh)
- import gnupg-1.4.3-1mdv2007.0

* Thu Jun 22 2006 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-1mdv2007.0
- 1.4.3
- added debian patches (P0)
- rediffed P1
- added a security fix for CVE-2006-3082 (P2)
- fix deps

* Mon May 01 2006 Stefan van der Eijk <stefan@eijk.nu> 1.4.2.2-2mdk
- rebuild for sparc

* Tue Mar 14 2006 Oden Eriksson <oeriksson@mandriva.com> 1.4.2.2-1mdk
- package was taken from updates:
  - 1.4.2.2; fixes CVE-2006-0049
  - drop P2; fixed upstream

* Wed Feb 22 2006 Stew Benedict <sbenedict@mandriva.com> 1.4.2.1-1mdk
- 1.4.2.1, drop P2 (merged upstream)

* Fri Feb 17 2006 Stew Benedict <sbenedict@mandriva.com> 1.4.2-4mdk
- P2: security fix for CVE-2006-0455

* Sun Nov 20 2005 Oden Eriksson <oeriksson@mandriva.com> 1.4.2-3mdk
- drop P0 as mandrakesecure.net is no more (#18587)

* Wed Aug 31 2005 Oden Eriksson <oeriksson@mandriva.com> 1.4.2-2mdk
- rebuilt against new openldap-2.3.6 libs
- fix deps

* Wed Aug 24 2005 Abel Cheung <deaddog@mandriva.org> 1.4.2-1mdk
- New release 1.4.2
- cosmetic fixes
- Drop patch2 (upstream)

* Sat Jul 23 2005 Nicolas Lécureuil <neoclust@mandriva.org> 1.4.0-5mdk
- Rebuild
- Fix File Section
- Fix smtpdaemon

* Tue Apr 05 2005 Vincent Danen <vdanen@mandrakesoft.com> 1.4.0-4mdk
- P2: security patch for CAN-2005-0366

* Wed Mar 23 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.4.0-3mdk
- Add patch1: use-agent by default to allow to crypt/uncrypt mail into kmail
	thanks to Plouf <plouf@montpelliertux.org>  and Neoclust <neoclust@mandrake.org> to point me it

* Fri Feb 04 2005 Buchan Milne <bgmilne@linux-mandrake.com> 1.4.0-2mdk
- rebuild for ldap2.2_7

* Wed Dec 22 2004 Stew Benedict <sbenedict@mandrakesoft.com> 1.4.0-1mdk
- 1.4.0

* Wed Nov 10 2004 Stew Benedict <sbenedict@mandrakesoft.com> 1.2.6-1mdk
- 1.2.6

